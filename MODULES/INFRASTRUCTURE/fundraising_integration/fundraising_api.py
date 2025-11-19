#!/usr/bin/env python3
"""
FUNDRAISING API - Backend for donations, investor portal, and donor management
Integrates with Stripe, sends thank-you emails, tracks equity
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

try:
    from flask import Flask, request, jsonify, redirect
    from flask_cors import CORS
    import stripe
    from dotenv import load_dotenv
except ImportError:
    print("❌ Required packages missing")
    print("   pip install flask flask-cors stripe python-dotenv")
    exit(1)

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_...")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_EMAIL = os.getenv("SMTP_EMAIL", "fundraising@conciousnessrevolution.io")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")

# Database (simplified - would use real database in production)
DATA_DIR = Path.home() / ".fundraising_data"
DATA_DIR.mkdir(exist_ok=True)
DONORS_FILE = DATA_DIR / "donors.json"
STATS_FILE = DATA_DIR / "stats.json"


class FundraisingDB:
    """Simple JSON-based database for donors and stats"""

    @staticmethod
    def load_donors() -> List[Dict]:
        if DONORS_FILE.exists():
            with open(DONORS_FILE, 'r') as f:
                return json.load(f)
        return []

    @staticmethod
    def save_donors(donors: List[Dict]):
        with open(DONORS_FILE, 'w') as f:
            json.dump(donors, f, indent=2)

    @staticmethod
    def add_donor(donor: Dict):
        donors = FundraisingDB.load_donors()
        donors.append(donor)
        FundraisingDB.save_donors(donors)

        # Update stats
        FundraisingDB.update_stats()

    @staticmethod
    def load_stats() -> Dict:
        if STATS_FILE.exists():
            with open(STATS_FILE, 'r') as f:
                return json.load(f)
        return {
            'total_raised': 0,
            'donor_count': 0,
            'avg_donation': 0,
            'goal': 10000000
        }

    @staticmethod
    def update_stats():
        donors = FundraisingDB.load_donors()
        total_raised = sum(d['amount'] for d in donors)
        donor_count = len(donors)
        avg_donation = total_raised / donor_count if donor_count > 0 else 0

        stats = {
            'total_raised': total_raised,
            'donor_count': donor_count,
            'avg_donation': avg_donation,
            'goal': 10000000,
            'last_updated': datetime.now().isoformat()
        }

        with open(STATS_FILE, 'w') as f:
            json.dump(stats, f, indent=2)


def send_thank_you_email(email: str, name: str, amount: float, tier: str):
    """Send automated thank-you email to donor"""

    subject = f"Welcome to the Consciousness Revolution! 🚀"

    body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <h1 style="color: #667eea;">Thank You, {name}!</h1>

        <p>Your <strong>${amount:.2f}</strong> contribution as a <strong>{tier}</strong> means the world to us.</p>

        <p>You're now part of something bigger than all of us - a movement to make manipulation impossible through AI and consciousness elevation.</p>

        <h2 style="color: #764ba2;">What Your Money Is Building:</h2>
        <ul>
            <li>✅ 8 modules live ($190M ARR potential)</li>
            <li>🚀 27 modules in roadmap ($1T vision)</li>
            <li>🧠 Manipulation immunity for humanity</li>
            <li>⚖️ Access to justice through AI legal tools</li>
            <li>🎵 Consciousness-infused music production</li>
            <li>🔍 Private investigation & corruption mapping</li>
        </ul>

        <h2 style="color: #764ba2;">Your Donor Portal:</h2>
        <p>Access exclusive updates, metrics, and community features:</p>
        <p><a href="https://conciousnessrevolution.io/donor-portal?email={email}" style="background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">Access Donor Portal</a></p>

        <h2 style="color: #764ba2;">What Happens Next:</h2>
        <ol>
            <li>Monthly updates on new modules launched</li>
            <li>Revenue milestones and user growth</li>
            <li>Path to $1T visualization</li>
            <li>Early access to new features</li>
        </ol>

        <p style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
            Thank you for believing in the mission.<br>
            <strong>- DWREK, Commander</strong><br>
            Consciousness Revolution
        </p>

        <p style="font-size: 12px; color: #999;">
            Questions? Reply to this email or contact <a href="mailto:support@conciousnessrevolution.io">support@conciousnessrevolution.io</a>
        </p>
    </body>
    </html>
    """

    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = SMTP_EMAIL
        msg['To'] = email

        msg.attach(MIMEText(body, 'html'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            if SMTP_PASSWORD:
                server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)

        print(f"✅ Thank-you email sent to {email}")
        return True

    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False


@app.route('/api/fundraising/stats', methods=['GET'])
def get_stats():
    """Get current fundraising statistics"""
    stats = FundraisingDB.load_stats()
    return jsonify(stats)


@app.route('/api/donate', methods=['POST'])
def process_donation():
    """Process Stripe donation"""
    data = request.json

    amount = float(data.get('amount', 0))
    email = data.get('email')
    name = data.get('name')
    tier = data.get('tier', 'Believer')

    if amount <= 0 or not email or not name:
        return jsonify({'error': 'Invalid donation data'}), 400

    try:
        # Create Stripe payment intent
        payment_intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),  # Convert to cents
            currency='usd',
            receipt_email=email,
            description=f'Consciousness Revolution - {tier} Tier',
            metadata={
                'name': name,
                'tier': tier
            }
        )

        # Save donor to database
        donor = {
            'name': name,
            'email': email,
            'amount': amount,
            'tier': tier,
            'date': datetime.now().isoformat(),
            'payment_id': payment_intent.id,
            'status': 'pending'
        }

        FundraisingDB.add_donor(donor)

        # Send thank-you email
        send_thank_you_email(email, name, amount, tier)

        return jsonify({
            'success': True,
            'client_secret': payment_intent.client_secret,
            'donor_id': payment_intent.id
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/invest', methods=['GET', 'POST'])
def investor_portal():
    """Investor portal for equity investments"""

    if request.method == 'POST':
        data = request.json
        investment = float(data.get('investment', 0))
        email = data.get('email')
        name = data.get('name')

        if investment < 10000:
            return jsonify({'error': 'Minimum investment is $10,000'}), 400

        # Calculate equity
        valuation = 10_000_000_000  # $10B valuation
        equity_percent = (investment / valuation) * 100

        # Save investor
        investor = {
            'name': name,
            'email': email,
            'investment': investment,
            'equity_percent': equity_percent,
            'date': datetime.now().isoformat(),
            'status': 'pending_agreement'
        }

        FundraisingDB.add_donor({**investor, 'amount': investment, 'tier': 'Investor'})

        # Send investor onboarding email
        send_investor_email(email, name, investment, equity_percent)

        return jsonify({
            'success': True,
            'equity_percent': equity_percent,
            'next_steps': 'Check your email for SAFE agreement'
        })

    # GET request - show calculator
    return jsonify({
        'valuation': 10_000_000_000,
        'calculator': 'investment / valuation = equity %',
        'examples': {
            '10K': 0.1,
            '50K': 0.5,
            '100K': 1.0,
            '1M': 10.0
        }
    })


def send_investor_email(email: str, name: str, investment: float, equity: float):
    """Send investor onboarding email with SAFE agreement"""

    subject = "Welcome, Investor! Your Equity in Consciousness Revolution"

    body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <h1 style="color: #667eea;">Welcome, {name}!</h1>

        <p>Thank you for your <strong>${investment:,.2f}</strong> investment in Consciousness Revolution.</p>

        <h2 style="color: #764ba2;">Your Investment:</h2>
        <ul>
            <li>Investment Amount: <strong>${investment:,.2f}</strong></li>
            <li>Equity Percentage: <strong>{equity:.4f}%</strong></li>
            <li>Current Valuation: <strong>$10 Billion</strong></li>
            <li>Potential Value at Exit: <strong>${investment * 100:,.2f}</strong> (100x)</li>
        </ul>

        <h2 style="color: #764ba2;">Next Steps:</h2>
        <ol>
            <li>Review SAFE agreement (attached)</li>
            <li>Sign electronically via DocuSign</li>
            <li>Wire transfer instructions will be provided</li>
            <li>Access investor dashboard</li>
        </ol>

        <p><a href="https://conciousnessrevolution.io/investor-dashboard?email={email}" style="background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">Access Investor Dashboard</a></p>

        <p style="margin-top: 30px;">
            You're not just investing in software - you're investing in the future of human consciousness.
        </p>

        <p>
            <strong>- DWREK, Commander</strong><br>
            Consciousness Revolution
        </p>
    </body>
    </html>
    """

    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = SMTP_EMAIL
        msg['To'] = email

        msg.attach(MIMEText(body, 'html'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            if SMTP_PASSWORD:
                server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)

        print(f"✅ Investor email sent to {email}")
        return True

    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False


@app.route('/api/donor-portal', methods=['GET'])
def donor_portal():
    """Donor portal access"""
    email = request.args.get('email')

    if not email:
        return jsonify({'error': 'Email required'}), 400

    # Find donor
    donors = FundraisingDB.load_donors()
    donor_data = [d for d in donors if d.get('email') == email]

    if not donor_data:
        return jsonify({'error': 'Donor not found'}), 404

    total_contributed = sum(d['amount'] for d in donor_data)

    # Load current stats
    stats = FundraisingDB.load_stats()

    return jsonify({
        'donor': {
            'email': email,
            'name': donor_data[0].get('name'),
            'total_contributed': total_contributed,
            'contribution_count': len(donor_data),
            'tier': donor_data[-1].get('tier'),
            'first_contribution': donor_data[0].get('date'),
            'latest_contribution': donor_data[-1].get('date')
        },
        'platform_stats': stats,
        'modules': {
            'live': 8,
            'total': 27,
            'revenue_potential': '190M ARR'
        }
    })


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'fundraising-api',
        'timestamp': datetime.now().isoformat()
    })


def main():
    """Run Flask app"""
    print("=" * 70)
    print("💰 FUNDRAISING API SERVER")
    print("=" * 70)
    print(f"\nStarting server on http://localhost:5000")
    print(f"Endpoints:")
    print(f"  GET  /api/fundraising/stats")
    print(f"  POST /api/donate")
    print(f"  GET  /api/invest")
    print(f"  POST /api/invest")
    print(f"  GET  /api/donor-portal")
    print(f"  GET  /health")
    print("\n" + "=" * 70)

    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == "__main__":
    main()
