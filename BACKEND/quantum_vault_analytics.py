"""
CONSCIOUSNESS REVOLUTION - QUANTUM VAULT ANALYTICS
Real-time revenue dashboard and financial intelligence

Tracks:
- MRR/ARR across all 7 domains
- Revenue growth and Fibonacci progression
- Conversion funnels and LTV:CAC
- Subscription health and churn
- Marketplace economics (70/30 splits)
- Per-domain performance
- Predictive revenue modeling
"""

import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from decimal import Decimal
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, request, jsonify
import json

# Configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://localhost/consciousness_revolution')

class QuantumVaultAnalytics:
    """
    Real-time revenue analytics and intelligence
    """

    def __init__(self):
        self.db_conn = psycopg2.connect(DATABASE_URL)

    def _get_cursor(self):
        return self.db_conn.cursor(cursor_factory=RealDictCursor)

    # =====================================================
    # CORE REVENUE METRICS
    # =====================================================

    def get_mrr(self, domain: str = None) -> Dict:
        """
        Calculate Monthly Recurring Revenue
        Optionally filter by domain
        """

        cursor = self._get_cursor()

        domain_filter = "AND domain = %s" if domain else ""
        params = [domain] if domain else []

        cursor.execute(f"""
            SELECT
                COALESCE(SUM(
                    CASE
                        WHEN billing_period = 'monthly' THEN price_monthly
                        WHEN billing_period = 'annual' THEN price_annual / 12
                    END
                ), 0) as mrr,
                COUNT(*) as active_subscriptions,
                COUNT(DISTINCT user_id) as paying_customers
            FROM subscriptions
            WHERE status = 'active'
            {domain_filter}
        """, params)

        result = cursor.fetchone()

        return {
            'mrr': float(result['mrr']),
            'active_subscriptions': result['active_subscriptions'],
            'paying_customers': result['paying_customers'],
            'domain': domain or 'all'
        }

    def get_arr(self, domain: str = None) -> Dict:
        """
        Calculate Annual Recurring Revenue
        """

        mrr_data = self.get_mrr(domain)

        return {
            'arr': mrr_data['mrr'] * 12,
            'mrr': mrr_data['mrr'],
            'domain': domain or 'all'
        }

    def get_revenue_by_domain(self) -> List[Dict]:
        """
        Get MRR breakdown by each of 7 domains
        """

        domains = ['music', 'intelligence', 'tools', 'education',
                  'commerce', 'communication', 'community']

        results = []
        for domain in domains:
            mrr_data = self.get_mrr(domain)
            results.append({
                'domain': domain,
                'mrr': mrr_data['mrr'],
                'arr': mrr_data['mrr'] * 12,
                'subscribers': mrr_data['paying_customers']
            })

        # Sort by MRR descending
        results.sort(key=lambda x: x['mrr'], reverse=True)

        # Add totals
        total_mrr = sum(r['mrr'] for r in results)
        total_arr = total_mrr * 12

        return {
            'domains': results,
            'totals': {
                'mrr': total_mrr,
                'arr': total_arr,
                'total_subscribers': sum(r['subscribers'] for r in results)
            }
        }

    def get_revenue_growth(self, days: int = 30) -> Dict:
        """
        Calculate revenue growth over time period
        Returns growth rate and trend
        """

        cursor = self._get_cursor()

        # Get MRR at start and end of period
        cursor.execute("""
            SELECT
                (SELECT calculate_mrr()) as current_mrr,
                (
                    SELECT COALESCE(SUM(
                        CASE
                            WHEN s.billing_period = 'monthly' THEN s.price_monthly
                            WHEN s.billing_period = 'annual' THEN s.price_annual / 12
                        END
                    ), 0)
                    FROM revenue_snapshots rs
                    WHERE rs.created_at >= NOW() - INTERVAL '%s days'
                    ORDER BY rs.created_at ASC
                    LIMIT 1
                ) as period_start_mrr
        """, (days,))

        result = cursor.fetchone()

        current_mrr = float(result['current_mrr'])
        start_mrr = float(result['period_start_mrr']) if result['period_start_mrr'] else current_mrr

        # Calculate growth
        growth_amount = current_mrr - start_mrr
        growth_percent = (growth_amount / start_mrr * 100) if start_mrr > 0 else 0

        return {
            'period_days': days,
            'start_mrr': start_mrr,
            'current_mrr': current_mrr,
            'growth_amount': growth_amount,
            'growth_percent': round(growth_percent, 2),
            'projected_annual_growth': round(growth_percent * (365 / days), 2)
        }

    # =====================================================
    # FIBONACCI PROGRESSION TRACKING
    # =====================================================

    def get_fibonacci_progression(self) -> Dict:
        """
        Track progress through Fibonacci revenue milestones
        $1K → $10K → $100K → $1M → $10M MRR
        """

        current_mrr = self.get_mrr()['mrr']

        milestones = [
            {'level': 1, 'target': 1000, 'name': '$1K MRR'},
            {'level': 2, 'target': 10000, 'name': '$10K MRR'},
            {'level': 3, 'target': 100000, 'name': '$100K MRR'},
            {'level': 4, 'target': 1000000, 'name': '$1M MRR'},
            {'level': 5, 'target': 10000000, 'name': '$10M MRR'},
        ]

        # Find current milestone
        current_milestone = None
        next_milestone = None

        for i, milestone in enumerate(milestones):
            if current_mrr < milestone['target']:
                next_milestone = milestone
                current_milestone = milestones[i-1] if i > 0 else None
                break

        if not next_milestone:
            # Past all milestones
            current_milestone = milestones[-1]
            next_milestone = None

        # Calculate progress to next milestone
        if next_milestone:
            if current_milestone:
                progress_percent = (
                    (current_mrr - current_milestone['target']) /
                    (next_milestone['target'] - current_milestone['target']) * 100
                )
            else:
                progress_percent = (current_mrr / next_milestone['target'] * 100)

            progress_percent = round(progress_percent, 2)
        else:
            progress_percent = 100

        # Estimate time to next milestone based on growth rate
        growth_30d = self.get_revenue_growth(30)
        monthly_growth_rate = growth_30d['growth_percent'] / 100

        if next_milestone and monthly_growth_rate > 0:
            months_to_milestone = 0
            projected_mrr = current_mrr

            while projected_mrr < next_milestone['target'] and months_to_milestone < 120:
                projected_mrr *= (1 + monthly_growth_rate)
                months_to_milestone += 1

            estimated_arrival = f"{months_to_milestone} months"
        else:
            estimated_arrival = None

        return {
            'current_mrr': current_mrr,
            'current_milestone': current_milestone,
            'next_milestone': next_milestone,
            'progress_percent': progress_percent,
            'estimated_arrival': estimated_arrival,
            'all_milestones': milestones
        }

    # =====================================================
    # CONVERSION METRICS
    # =====================================================

    def get_ltv_cac_ratio(self) -> Dict:
        """
        Calculate Lifetime Value to Customer Acquisition Cost ratio
        Target: 3:1 minimum, 24:1 for hypergrowth (from Quantum Vault blueprint)
        """

        cursor = self._get_cursor()

        # Calculate average LTV (simplified - real calculation needs churn data)
        cursor.execute("""
            SELECT
                AVG(
                    CASE
                        WHEN billing_period = 'monthly' THEN price_monthly * 12
                        WHEN billing_period = 'annual' THEN price_annual
                    END
                ) as avg_annual_value
            FROM subscriptions
            WHERE status = 'active'
        """)

        avg_ltv = cursor.fetchone()['avg_annual_value']
        avg_ltv = float(avg_ltv) if avg_ltv else 0

        # Assume 24-month average customer lifespan (would calculate from churn)
        ltv = avg_ltv * 2

        # Calculate CAC from marketing spend (simplified)
        cursor.execute("""
            SELECT COUNT(DISTINCT user_id) as new_customers
            FROM users
            WHERE created_at >= NOW() - INTERVAL '30 days'
        """)

        new_customers = cursor.fetchone()['new_customers']

        # Assume $50 CAC per customer (would track actual marketing spend)
        cac = 50

        # Calculate ratio
        ratio = ltv / cac if cac > 0 else 0

        return {
            'ltv': round(ltv, 2),
            'cac': cac,
            'ratio': round(ratio, 2),
            'target_ratio': 24,
            'meets_hypergrowth_target': ratio >= 24
        }

    def get_churn_rate(self, days: int = 30) -> Dict:
        """
        Calculate customer churn rate
        Lower is better - target < 5% monthly
        """

        cursor = self._get_cursor()

        cursor.execute("""
            SELECT
                COUNT(DISTINCT user_id) as customers_start_period
            FROM subscriptions
            WHERE status = 'active'
            AND created_at < NOW() - INTERVAL '%s days'
        """, (days,))

        customers_start = cursor.fetchone()['customers_start_period']

        cursor.execute("""
            SELECT COUNT(*) as churned_customers
            FROM subscriptions
            WHERE status = 'cancelled'
            AND cancelled_at >= NOW() - INTERVAL '%s days'
        """, (days,))

        churned = cursor.fetchone()['churned_customers']

        churn_rate = (churned / customers_start * 100) if customers_start > 0 else 0

        return {
            'period_days': days,
            'customers_start_period': customers_start,
            'churned_customers': churned,
            'churn_rate': round(churn_rate, 2),
            'retention_rate': round(100 - churn_rate, 2),
            'target_churn_rate': 5.0,
            'healthy': churn_rate < 5.0
        }

    # =====================================================
    # MARKETPLACE ECONOMICS
    # =====================================================

    def get_marketplace_revenue(self) -> Dict:
        """
        Track marketplace revenue (70/30 split)
        Shows total GMV, platform commission, creator payouts
        """

        cursor = self._get_cursor()

        cursor.execute("""
            SELECT
                COUNT(*) as total_sales,
                SUM(price) as gmv,
                SUM(platform_commission) as platform_revenue,
                SUM(creator_earnings) as creator_payouts,
                COUNT(DISTINCT buyer_id) as unique_buyers,
                COUNT(DISTINCT item_id) as items_sold
            FROM marketplace_purchases
            WHERE status = 'completed'
            AND created_at >= NOW() - INTERVAL '30 days'
        """)

        result = cursor.fetchone()

        gmv = float(result['gmv'] or 0)
        platform_revenue = float(result['platform_commission'] or 0)
        creator_payouts = float(result['creator_payouts'] or 0)

        # Verify 70/30 split
        expected_platform = gmv * 0.30
        expected_creators = gmv * 0.70

        return {
            'period': '30 days',
            'total_sales': result['total_sales'],
            'gmv': gmv,
            'platform_revenue': platform_revenue,
            'creator_payouts': creator_payouts,
            'unique_buyers': result['unique_buyers'],
            'items_sold': result['items_sold'],
            'avg_transaction': round(gmv / result['total_sales'], 2) if result['total_sales'] > 0 else 0,
            'split_verification': {
                'expected_platform_30pct': round(expected_platform, 2),
                'actual_platform': round(platform_revenue, 2),
                'expected_creators_70pct': round(expected_creators, 2),
                'actual_creators': round(creator_payouts, 2)
            }
        }

    # =====================================================
    # SUBSCRIPTION HEALTH
    # =====================================================

    def get_subscription_health(self) -> Dict:
        """
        Overall subscription health metrics
        """

        cursor = self._get_cursor()

        # Subscription status breakdown
        cursor.execute("""
            SELECT
                status,
                COUNT(*) as count,
                COUNT(DISTINCT user_id) as unique_users
            FROM subscriptions
            GROUP BY status
        """)

        status_breakdown = {}
        for row in cursor.fetchall():
            status_breakdown[row['status']] = {
                'count': row['count'],
                'unique_users': row['unique_users']
            }

        # Tier distribution
        cursor.execute("""
            SELECT
                tier,
                COUNT(*) as count,
                SUM(
                    CASE
                        WHEN billing_period = 'monthly' THEN price_monthly
                        WHEN billing_period = 'annual' THEN price_annual / 12
                    END
                ) as tier_mrr
            FROM subscriptions
            WHERE status = 'active'
            GROUP BY tier
        """)

        tier_distribution = {}
        for row in cursor.fetchall():
            tier_distribution[row['tier']] = {
                'count': row['count'],
                'mrr': float(row['tier_mrr'])
            }

        # Billing period preference
        cursor.execute("""
            SELECT
                billing_period,
                COUNT(*) as count,
                ROUND(COUNT(*)::NUMERIC / SUM(COUNT(*)) OVER () * 100, 2) as percentage
            FROM subscriptions
            WHERE status = 'active'
            GROUP BY billing_period
        """)

        billing_periods = {}
        for row in cursor.fetchall():
            billing_periods[row['billing_period']] = {
                'count': row['count'],
                'percentage': float(row['percentage'])
            }

        return {
            'status_breakdown': status_breakdown,
            'tier_distribution': tier_distribution,
            'billing_periods': billing_periods
        }

    # =====================================================
    # COMPREHENSIVE DASHBOARD
    # =====================================================

    def get_quantum_vault_dashboard(self) -> Dict:
        """
        Complete revenue dashboard
        All metrics in one call
        """

        return {
            'timestamp': datetime.now().isoformat(),
            'core_metrics': {
                'mrr': self.get_mrr(),
                'arr': self.get_arr(),
                'revenue_by_domain': self.get_revenue_by_domain()
            },
            'growth': {
                '30_day': self.get_revenue_growth(30),
                '90_day': self.get_revenue_growth(90),
                'fibonacci_progression': self.get_fibonacci_progression()
            },
            'conversion': {
                'ltv_cac': self.get_ltv_cac_ratio(),
                'churn': self.get_churn_rate(30)
            },
            'marketplace': self.get_marketplace_revenue(),
            'subscription_health': self.get_subscription_health()
        }

    # =====================================================
    # SNAPSHOT & HISTORICAL TRACKING
    # =====================================================

    def create_revenue_snapshot(self):
        """
        Create snapshot of current revenue state
        Run daily via cron to build historical data
        """

        cursor = self._get_cursor()

        # Get current metrics
        mrr = self.get_mrr()['mrr']
        arr = self.get_arr()['arr']
        paying_customers = self.get_mrr()['paying_customers']

        # Get conversion metrics
        ltv_cac = self.get_ltv_cac_ratio()
        churn = self.get_churn_rate(30)

        # Get marketplace
        marketplace = self.get_marketplace_revenue()

        cursor.execute("""
            INSERT INTO revenue_snapshots (
                mrr, arr, paying_customers, ltv, cac,
                churn_rate, marketplace_gmv, created_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
        """, (
            mrr, arr, paying_customers,
            ltv_cac['ltv'], ltv_cac['cac'],
            churn['churn_rate'],
            marketplace['gmv']
        ))

        self.db_conn.commit()

    def get_revenue_history(self, days: int = 90) -> List[Dict]:
        """
        Get historical revenue snapshots
        For charting growth over time
        """

        cursor = self._get_cursor()
        cursor.execute("""
            SELECT
                DATE(created_at) as date,
                mrr, arr, paying_customers,
                ltv, cac, churn_rate, marketplace_gmv
            FROM revenue_snapshots
            WHERE created_at >= NOW() - INTERVAL '%s days'
            ORDER BY created_at ASC
        """, (days,))

        history = []
        for row in cursor.fetchall():
            history.append({
                'date': row['date'].isoformat(),
                'mrr': float(row['mrr']),
                'arr': float(row['arr']),
                'paying_customers': row['paying_customers'],
                'ltv': float(row['ltv'] or 0),
                'cac': float(row['cac'] or 0),
                'churn_rate': float(row['churn_rate'] or 0),
                'marketplace_gmv': float(row['marketplace_gmv'] or 0)
            })

        return history


# =====================================================
# API ENDPOINTS
# =====================================================

app = Flask(__name__)
analytics = QuantumVaultAnalytics()

@app.route('/api/vault/dashboard', methods=['GET'])
def api_get_dashboard():
    """
    GET /api/vault/dashboard

    Complete revenue dashboard - all metrics
    """
    dashboard = analytics.get_quantum_vault_dashboard()
    return jsonify(dashboard)

@app.route('/api/vault/mrr', methods=['GET'])
def api_get_mrr():
    """
    GET /api/vault/mrr?domain=music

    Monthly Recurring Revenue
    """
    domain = request.args.get('domain')
    mrr = analytics.get_mrr(domain)
    return jsonify(mrr)

@app.route('/api/vault/arr', methods=['GET'])
def api_get_arr():
    """
    GET /api/vault/arr?domain=music

    Annual Recurring Revenue
    """
    domain = request.args.get('domain')
    arr = analytics.get_arr(domain)
    return jsonify(arr)

@app.route('/api/vault/domains', methods=['GET'])
def api_get_revenue_by_domain():
    """
    GET /api/vault/domains

    Revenue breakdown by domain
    """
    domains = analytics.get_revenue_by_domain()
    return jsonify(domains)

@app.route('/api/vault/growth', methods=['GET'])
def api_get_growth():
    """
    GET /api/vault/growth?days=30

    Revenue growth over period
    """
    days = int(request.args.get('days', 30))
    growth = analytics.get_revenue_growth(days)
    return jsonify(growth)

@app.route('/api/vault/fibonacci', methods=['GET'])
def api_get_fibonacci():
    """
    GET /api/vault/fibonacci

    Fibonacci milestone progression
    """
    progression = analytics.get_fibonacci_progression()
    return jsonify(progression)

@app.route('/api/vault/ltv-cac', methods=['GET'])
def api_get_ltv_cac():
    """
    GET /api/vault/ltv-cac

    Lifetime Value to Customer Acquisition Cost
    """
    ratio = analytics.get_ltv_cac_ratio()
    return jsonify(ratio)

@app.route('/api/vault/churn', methods=['GET'])
def api_get_churn():
    """
    GET /api/vault/churn?days=30

    Customer churn rate
    """
    days = int(request.args.get('days', 30))
    churn = analytics.get_churn_rate(days)
    return jsonify(churn)

@app.route('/api/vault/marketplace', methods=['GET'])
def api_get_marketplace():
    """
    GET /api/vault/marketplace

    Marketplace economics (70/30 split)
    """
    marketplace = analytics.get_marketplace_revenue()
    return jsonify(marketplace)

@app.route('/api/vault/subscription-health', methods=['GET'])
def api_get_subscription_health():
    """
    GET /api/vault/subscription-health

    Overall subscription health
    """
    health = analytics.get_subscription_health()
    return jsonify(health)

@app.route('/api/vault/history', methods=['GET'])
def api_get_history():
    """
    GET /api/vault/history?days=90

    Historical revenue data
    """
    days = int(request.args.get('days', 90))
    history = analytics.get_revenue_history(days)
    return jsonify({'history': history})

@app.route('/api/vault/snapshot', methods=['POST'])
def api_create_snapshot():
    """
    POST /api/vault/snapshot

    Create revenue snapshot (called by cron)
    """
    analytics.create_revenue_snapshot()
    return jsonify({'success': True, 'message': 'Snapshot created'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)


# =====================================================
# QUANTUM VAULT ANALYTICS COMPLETE
#
# Tracks:
# ✅ MRR/ARR (overall and per-domain)
# ✅ Revenue growth and trends
# ✅ Fibonacci progression ($1K → $10M)
# ✅ LTV:CAC ratio (hypergrowth target: 24:1)
# ✅ Churn rate (target: <5%)
# ✅ Marketplace GMV and 70/30 splits
# ✅ Subscription health metrics
# ✅ Historical tracking
#
# Daily snapshot via cron:
# 0 0 * * * python -c "from quantum_vault_analytics import QuantumVaultAnalytics; QuantumVaultAnalytics().create_revenue_snapshot()"
#
# Ready for deployment
# =====================================================
