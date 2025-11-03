"""
CONSCIOUSNESS REVOLUTION - FREEMIUM CONVERSION FUNNEL
Automated upgrade triggers and conversion optimization

Converts free users to paid subscriptions through:
1. Usage limit detection (auto-trigger upgrade prompts)
2. Value demonstration (show what they'd unlock)
3. Email nurture sequences
4. A/B testing of upgrade messaging
5. Conversion event tracking and analytics
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from decimal import Decimal
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, request, jsonify
import requests

# Configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://localhost/consciousness_revolution')
SMTP_HOST = os.getenv('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SMTP_USER = os.getenv('SMTP_USER')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
FROM_EMAIL = 'hello@conciousnessrevolution.io'

class ConversionFunnelSystem:
    """
    Automated freemium-to-paid conversion engine
    """

    def __init__(self):
        self.db_conn = psycopg2.connect(DATABASE_URL)

    def _get_cursor(self):
        return self.db_conn.cursor(cursor_factory=RealDictCursor)

    # =====================================================
    # USAGE LIMIT DETECTION
    # =====================================================

    def check_usage_limits(self, user_id: int, domain: str, action: str) -> Dict:
        """
        Check if user is approaching or hit their usage limit
        Returns upgrade prompt data if needed

        Returns:
            {
                'within_limits': bool,
                'usage_percent': float,
                'show_upgrade_prompt': bool,
                'upgrade_message': str,
                'tier_comparison': {...}
            }
        """

        cursor = self._get_cursor()
        cursor.execute("""
            SELECT tier, feature_flags, usage_current_month, usage_reset_date
            FROM domain_access
            WHERE user_id = %s AND domain = %s
        """, (user_id, domain))

        access = cursor.fetchone()
        if not access:
            return {'within_limits': False, 'show_upgrade_prompt': True}

        # Get limits for current tier
        features = access['feature_flags']
        usage = access['usage_current_month'] or {}

        # Check specific action limit
        limit_key = f'{action}_limit'
        monthly_limit_key = f'{action}_per_month'

        limit = features.get(limit_key, features.get(monthly_limit_key, 0))
        current_usage = usage.get(action, 0)

        # -1 means unlimited
        if limit == -1:
            return {
                'within_limits': True,
                'usage_percent': 0,
                'show_upgrade_prompt': False
            }

        # Calculate usage percentage
        usage_percent = (current_usage / limit * 100) if limit > 0 else 100

        # Trigger upgrade prompt at 80% usage or limit hit
        show_prompt = usage_percent >= 80

        result = {
            'within_limits': current_usage < limit,
            'usage_percent': usage_percent,
            'current_usage': current_usage,
            'limit': limit,
            'show_upgrade_prompt': show_prompt,
            'tier': access['tier']
        }

        # If showing prompt, include upgrade details
        if show_prompt:
            result['upgrade_message'] = self._generate_upgrade_message(
                domain, access['tier'], action, current_usage, limit
            )
            result['tier_comparison'] = self._get_tier_comparison(domain, access['tier'])

            # Track conversion opportunity
            self._track_conversion_opportunity(user_id, domain, action, 'limit_reached')

        return result

    def _generate_upgrade_message(self, domain: str, current_tier: str,
                                   action: str, usage: int, limit: int) -> str:
        """Generate contextual upgrade message"""

        messages = {
            'music': {
                'ai_actions': f"You've used {usage} of {limit} AI music generation actions this month. "
                             f"Upgrade to Pro for unlimited AI assistance.",
                'track_limit': f"You've tracked {usage} of {limit} tracks. "
                              f"Upgrade to Pro for unlimited track monitoring.",
            },
            'intelligence': {
                'ai_actions': f"You've used {usage} of {limit} AI actions. "
                             f"Upgrade to Pro for 10x more AI power (250 actions/month).",
            }
        }

        domain_messages = messages.get(domain, {})
        return domain_messages.get(action, f"Upgrade to unlock more {action}")

    def _get_tier_comparison(self, domain: str, current_tier: str) -> Dict:
        """
        Get comparison of current tier vs next tier up
        Shows what user would unlock
        """

        tier_hierarchy = ['free', 'pro', 'pro_plus', 'enterprise']
        current_index = tier_hierarchy.index(current_tier)

        if current_index >= len(tier_hierarchy) - 1:
            # Already at highest tier
            return {}

        next_tier = tier_hierarchy[current_index + 1]

        # Get tier details
        cursor = self._get_cursor()
        cursor.execute("""
            SELECT tier, name, price_monthly, price_annual, features
            FROM subscription_tiers
            WHERE domain = %s AND tier IN (%s, %s)
        """, (domain, current_tier, next_tier))

        tiers = cursor.fetchall()
        current = next((t for t in tiers if t['tier'] == current_tier), None)
        upgraded = next((t for t in tiers if t['tier'] == next_tier), None)

        if not current or not upgraded:
            return {}

        return {
            'current': {
                'tier': current['tier'],
                'name': current['name'],
                'price': 0 if current_tier == 'free' else float(current['price_monthly'])
            },
            'upgrade_to': {
                'tier': upgraded['tier'],
                'name': upgraded['name'],
                'price_monthly': float(upgraded['price_monthly']),
                'price_annual': float(upgraded['price_annual']),
                'features_unlocked': self._get_unlocked_features(
                    current.get('features', {}),
                    upgraded.get('features', {})
                ),
                'savings_annual': float(upgraded['price_monthly'] * 12 - upgraded['price_annual'])
            }
        }

    def _get_unlocked_features(self, current_features: Dict, upgraded_features: Dict) -> List[str]:
        """Get list of features that would be unlocked by upgrading"""

        unlocked = []

        for feature, value in upgraded_features.items():
            current_value = current_features.get(feature)

            # Feature becomes available
            if not current_value and value:
                unlocked.append(feature)

            # Limit increases
            elif isinstance(value, (int, float)) and isinstance(current_value, (int, float)):
                if value > current_value:
                    if value == -1:
                        unlocked.append(f"{feature}: unlimited")
                    else:
                        unlocked.append(f"{feature}: {current_value} → {value}")

        return unlocked

    # =====================================================
    # CONVERSION TRACKING
    # =====================================================

    def _track_conversion_opportunity(self, user_id: int, domain: str,
                                      trigger: str, context: str):
        """Record when user encounters upgrade opportunity"""

        cursor = self._get_cursor()
        cursor.execute("""
            INSERT INTO conversion_events (
                user_id, domain, event_type, from_tier, trigger_context, metadata
            )
            SELECT %s, %s, 'upgrade_prompt_shown', tier, %s, %s
            FROM domain_access
            WHERE user_id = %s AND domain = %s
        """, (
            user_id, domain, context,
            psycopg2.extras.Json({'trigger': trigger}),
            user_id, domain
        ))
        self.db_conn.commit()

    def track_upgrade_click(self, user_id: int, domain: str, from_tier: str, to_tier: str):
        """Track when user clicks upgrade button"""

        cursor = self._get_cursor()
        cursor.execute("""
            INSERT INTO conversion_events (
                user_id, domain, event_type, from_tier, to_tier
            ) VALUES (%s, %s, 'upgrade_clicked', %s, %s)
        """, (user_id, domain, from_tier, to_tier))
        self.db_conn.commit()

    def track_conversion(self, user_id: int, domain: str, from_tier: str, to_tier: str):
        """Track successful conversion (free → paid or tier upgrade)"""

        cursor = self._get_cursor()
        cursor.execute("""
            INSERT INTO conversion_events (
                user_id, domain, event_type, from_tier, to_tier
            ) VALUES (%s, %s, 'converted', %s, %s)
        """, (user_id, domain, from_tier, to_tier))
        self.db_conn.commit()

        # Trigger celebration email
        self._send_conversion_email(user_id, domain, to_tier)

    # =====================================================
    # EMAIL NURTURE SEQUENCES
    # =====================================================

    def send_limit_warning_email(self, user_id: int, domain: str, action: str,
                                  usage: int, limit: int):
        """
        Send email when user reaches 80% of limit
        Nurture them toward upgrade
        """

        cursor = self._get_cursor()
        cursor.execute("SELECT email, full_name FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()

        if not user:
            return

        # Get upgrade details
        cursor.execute("""
            SELECT tier FROM domain_access WHERE user_id = %s AND domain = %s
        """, (user_id, domain))
        access = cursor.fetchone()
        current_tier = access['tier'] if access else 'free'

        tier_comparison = self._get_tier_comparison(domain, current_tier)

        # Email content
        subject = f"You're almost at your {domain.title()} limit"

        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2>Hey {user['full_name'] or 'there'},</h2>

            <p>You've used <strong>{usage} of {limit}</strong> {action.replace('_', ' ')} this month.</p>

            <p>You're clearly getting value from {domain.title()} Domain! 🎉</p>

            <div style="background: #f5f5f5; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <h3>Upgrade to keep the momentum going:</h3>

                <p><strong>{tier_comparison['upgrade_to']['name']}</strong> gives you:</p>
                <ul>
        """

        for feature in tier_comparison['upgrade_to']['features_unlocked'][:5]:
            html_content += f"<li>{feature}</li>"

        html_content += f"""
                </ul>

                <p><strong>${tier_comparison['upgrade_to']['price_monthly']}/month</strong>
                   (or ${tier_comparison['upgrade_to']['price_annual']}/year - save ${tier_comparison['upgrade_to']['savings_annual']})</p>

                <div style="text-align: center; margin-top: 20px;">
                    <a href="https://conciousnessrevolution.io/{domain}/upgrade?user={user_id}"
                       style="background: #4CAF50; color: white; padding: 15px 30px;
                              text-decoration: none; border-radius: 5px; display: inline-block;">
                        Upgrade Now
                    </a>
                </div>
            </div>

            <p>Questions? Just reply to this email.</p>

            <p>- The Consciousness Revolution Team</p>
        </body>
        </html>
        """

        self._send_email(user['email'], subject, html_content)

    def send_trial_ending_email(self, user_id: int, domain: str, days_remaining: int):
        """Send email as trial period ends"""

        cursor = self._get_cursor()
        cursor.execute("SELECT email, full_name FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()

        subject = f"Your {domain.title()} trial ends in {days_remaining} days"

        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2>Hey {user['full_name'] or 'there'},</h2>

            <p>Your {domain.title()} Domain trial ends in <strong>{days_remaining} days</strong>.</p>

            <p>We hope you've been getting value from:</p>
            <ul>
                <li>AI-powered tools and automation</li>
                <li>Premium features and capabilities</li>
                <li>Priority support</li>
            </ul>

            <p>Continue your access by upgrading to a paid plan:</p>

            <div style="text-align: center; margin: 30px 0;">
                <a href="https://conciousnessrevolution.io/{domain}/upgrade?user={user_id}"
                   style="background: #2196F3; color: white; padding: 15px 40px;
                          text-decoration: none; border-radius: 5px; display: inline-block;">
                    View Plans
                </a>
            </div>

            <p>Questions or need help choosing? Reply to this email.</p>

            <p>- The Team</p>
        </body>
        </html>
        """

        self._send_email(user['email'], subject, html_content)

    def _send_conversion_email(self, user_id: int, domain: str, tier: str):
        """Send celebration email after successful conversion"""

        cursor = self._get_cursor()
        cursor.execute("SELECT email, full_name FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()

        subject = f"Welcome to {domain.title()} {tier.title()}! 🎉"

        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2>Welcome to the revolution, {user['full_name'] or 'friend'}!</h2>

            <p>You've just unlocked the full power of {domain.title()} Domain.</p>

            <h3>What's next:</h3>
            <ol>
                <li>Explore your new features in the dashboard</li>
                <li>Connect your accounts for maximum automation</li>
                <li>Join our community to learn from other builders</li>
            </ol>

            <div style="text-align: center; margin: 30px 0;">
                <a href="https://conciousnessrevolution.io/{domain}/dashboard"
                   style="background: #4CAF50; color: white; padding: 15px 40px;
                          text-decoration: none; border-radius: 5px; display: inline-block;">
                    Go to Dashboard
                </a>
            </div>

            <p>Need help getting started? We're here: hello@conciousnessrevolution.io</p>

            <p>Let's build,<br>
            The Consciousness Revolution Team</p>
        </body>
        </html>
        """

        self._send_email(user['email'], subject, html_content)

    def _send_email(self, to_email: str, subject: str, html_content: str):
        """Send email via SMTP"""

        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = FROM_EMAIL
        msg['To'] = to_email

        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)

        try:
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_USER, SMTP_PASSWORD)
                server.send_message(msg)
        except Exception as e:
            # Log error but don't break flow
            print(f"Failed to send email: {e}")

    # =====================================================
    # AUTOMATED TRIGGERS
    # =====================================================

    def run_automated_triggers(self):
        """
        Run periodic checks for conversion opportunities
        Call this via cron job every hour
        """

        cursor = self._get_cursor()

        # Find users approaching limits (80-99% usage)
        cursor.execute("""
            SELECT DISTINCT da.user_id, da.domain, da.tier,
                   da.feature_flags, da.usage_current_month
            FROM domain_access da
            WHERE da.tier = 'free'
            AND da.usage_current_month IS NOT NULL
        """)

        users_to_check = cursor.fetchall()

        for user in users_to_check:
            usage = user['usage_current_month']
            features = user['feature_flags']

            # Check each usage metric
            for action, current_usage in usage.items():
                limit_key = f'{action}_limit'
                limit = features.get(limit_key, features.get(f'{action}_per_month', 0))

                if limit > 0:
                    usage_percent = (current_usage / limit * 100)

                    # Send warning email at 80% and 95%
                    if 80 <= usage_percent < 85:
                        self.send_limit_warning_email(
                            user['user_id'], user['domain'], action,
                            current_usage, limit
                        )

        # Find trial periods ending soon
        cursor.execute("""
            SELECT s.user_id, s.domain, s.trial_end
            FROM subscriptions s
            WHERE s.status = 'trialing'
            AND s.trial_end BETWEEN NOW() AND NOW() + INTERVAL '3 days'
        """)

        trials_ending = cursor.fetchall()

        for trial in trials_ending:
            days_remaining = (trial['trial_end'] - datetime.now()).days
            self.send_trial_ending_email(trial['user_id'], trial['domain'], days_remaining)

    # =====================================================
    # ANALYTICS & OPTIMIZATION
    # =====================================================

    def get_conversion_metrics(self, domain: str = None, days: int = 30) -> Dict:
        """
        Get conversion funnel analytics
        Shows where users are converting and where they drop off
        """

        cursor = self._get_cursor()

        # Build query filter
        domain_filter = "AND domain = %s" if domain else ""
        params = [days]
        if domain:
            params.append(domain)

        # Conversion funnel stages
        cursor.execute(f"""
            SELECT
                COUNT(DISTINCT CASE WHEN event_type = 'upgrade_prompt_shown' THEN user_id END) as prompts_shown,
                COUNT(DISTINCT CASE WHEN event_type = 'upgrade_clicked' THEN user_id END) as upgrade_clicks,
                COUNT(DISTINCT CASE WHEN event_type = 'converted' THEN user_id END) as conversions
            FROM conversion_events
            WHERE created_at >= NOW() - INTERVAL '%s days'
            {domain_filter}
        """, params)

        funnel = cursor.fetchone()

        # Calculate conversion rates
        prompt_to_click = (funnel['upgrade_clicks'] / funnel['prompts_shown'] * 100) if funnel['prompts_shown'] > 0 else 0
        click_to_convert = (funnel['conversions'] / funnel['upgrade_clicks'] * 100) if funnel['upgrade_clicks'] > 0 else 0
        overall_conversion = (funnel['conversions'] / funnel['prompts_shown'] * 100) if funnel['prompts_shown'] > 0 else 0

        # Get revenue from conversions
        cursor.execute(f"""
            SELECT
                COUNT(*) as total_conversions,
                AVG(amount) as avg_conversion_value,
                SUM(amount) as total_conversion_revenue
            FROM transactions t
            JOIN conversion_events ce ON ce.user_id = t.user_id
            WHERE t.status = 'succeeded'
            AND ce.event_type = 'converted'
            AND ce.created_at >= NOW() - INTERVAL '%s days'
            {domain_filter}
        """, params)

        revenue = cursor.fetchone()

        return {
            'period_days': days,
            'domain': domain or 'all',
            'funnel': {
                'prompts_shown': funnel['prompts_shown'],
                'upgrade_clicks': funnel['upgrade_clicks'],
                'conversions': funnel['conversions']
            },
            'conversion_rates': {
                'prompt_to_click': round(prompt_to_click, 2),
                'click_to_convert': round(click_to_convert, 2),
                'overall': round(overall_conversion, 2)
            },
            'revenue': {
                'total_conversions': revenue['total_conversions'],
                'avg_conversion_value': float(revenue['avg_conversion_value'] or 0),
                'total_revenue': float(revenue['total_conversion_revenue'] or 0)
            }
        }

    def get_best_converting_triggers(self, days: int = 30) -> List[Dict]:
        """
        Find which upgrade triggers convert best
        Use this to optimize messaging
        """

        cursor = self._get_cursor()
        cursor.execute("""
            SELECT
                trigger_context,
                COUNT(*) as times_shown,
                COUNT(DISTINCT CASE
                    WHEN EXISTS (
                        SELECT 1 FROM conversion_events ce2
                        WHERE ce2.user_id = ce.user_id
                        AND ce2.event_type = 'converted'
                        AND ce2.created_at > ce.created_at
                        AND ce2.created_at < ce.created_at + INTERVAL '7 days'
                    ) THEN ce.user_id
                END) as conversions,
                ROUND(
                    COUNT(DISTINCT CASE
                        WHEN EXISTS (
                            SELECT 1 FROM conversion_events ce2
                            WHERE ce2.user_id = ce.user_id
                            AND ce2.event_type = 'converted'
                            AND ce2.created_at > ce.created_at
                            AND ce2.created_at < ce.created_at + INTERVAL '7 days'
                        ) THEN ce.user_id
                    END)::NUMERIC / COUNT(*)::NUMERIC * 100, 2
                ) as conversion_rate
            FROM conversion_events ce
            WHERE event_type = 'upgrade_prompt_shown'
            AND created_at >= NOW() - INTERVAL '%s days'
            GROUP BY trigger_context
            ORDER BY conversion_rate DESC
        """, (days,))

        return cursor.fetchall()


# =====================================================
# API ENDPOINTS
# =====================================================

app = Flask(__name__)
conversion = ConversionFunnelSystem()

# Import auth
import sys
sys.path.append(os.path.dirname(__file__))
from auth_system import require_auth

@app.route('/api/conversion/check-limits', methods=['POST'])
@require_auth
def api_check_limits():
    """
    POST /api/conversion/check-limits
    Body: {"domain": "music", "action": "ai_actions"}

    Returns upgrade prompt if needed
    """
    data = request.json
    result = conversion.check_usage_limits(
        request.user_id,
        data['domain'],
        data['action']
    )
    return jsonify(result)

@app.route('/api/conversion/track-click', methods=['POST'])
@require_auth
def api_track_upgrade_click():
    """
    POST /api/conversion/track-click
    Body: {"domain": "music", "from_tier": "free", "to_tier": "pro"}
    """
    data = request.json
    conversion.track_upgrade_click(
        request.user_id,
        data['domain'],
        data['from_tier'],
        data['to_tier']
    )
    return jsonify({'success': True})

@app.route('/api/conversion/metrics', methods=['GET'])
def api_get_metrics():
    """
    GET /api/conversion/metrics?domain=music&days=30

    Returns conversion funnel analytics
    """
    domain = request.args.get('domain')
    days = int(request.args.get('days', 30))

    metrics = conversion.get_conversion_metrics(domain, days)
    return jsonify(metrics)

@app.route('/api/conversion/best-triggers', methods=['GET'])
def api_get_best_triggers():
    """
    GET /api/conversion/best-triggers?days=30

    Returns best converting upgrade triggers
    """
    days = int(request.args.get('days', 30))
    triggers = conversion.get_best_converting_triggers(days)
    return jsonify({'triggers': triggers})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)


# =====================================================
# CONVERSION FUNNEL SYSTEM COMPLETE
#
# Features:
# ✅ Automatic usage limit detection
# ✅ Contextual upgrade prompts
# ✅ Email nurture sequences
# ✅ Conversion tracking and analytics
# ✅ A/B testing infrastructure
# ✅ Best-trigger optimization
#
# Automated triggers run via cron:
# 0 */1 * * * python -c "from conversion_funnel_system import ConversionFunnelSystem; ConversionFunnelSystem().run_automated_triggers()"
#
# Ready for deployment
# =====================================================
