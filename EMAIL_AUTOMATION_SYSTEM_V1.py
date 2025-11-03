#!/usr/bin/env python3
"""
100X PLATFORM - EMAIL AUTOMATION SYSTEM
Auto-send confirmation emails on form submission
Consciousness screening results delivery
"""

import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pyairtable import Table
import time

# Configuration
AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY', 'YOUR_KEY_HERE')
AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID', 'YOUR_BASE_HERE')
AIRTABLE_TABLE_NAME = 'Users'

# Email configuration (using Gmail as example)
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS', 'contact@consciousnessrevolution.io')
EMAIL_PASSWORD = os.getenv('EMAIL_APP_PASSWORD', 'YOUR_APP_PASSWORD')

class EmailAutomation:
    def __init__(self):
        self.table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME)
        self.processed_ids = set()

    def send_email(self, to_email, subject, html_content):
        """Send HTML email"""
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = to_email
            msg['Subject'] = subject

            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)

            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.send_message(msg)

            print(f"✅ Email sent to {to_email}: {subject}")
            return True
        except Exception as e:
            print(f"❌ Email failed to {to_email}: {e}")
            return False

    def calculate_consciousness_score(self, mission, values):
        """Calculate consciousness score from mission and values"""
        # Pattern Theory keywords
        builder_keywords = [
            'build', 'create', 'help', 'serve', 'contribute', 'improve',
            'solve', 'empower', 'enable', 'support', 'collaborate', 'share',
            'teach', 'learn', 'grow', 'heal', 'protect', 'innovate', 'truth'
        ]

        destroyer_keywords = [
            'dominate', 'control', 'manipulate', 'exploit', 'destroy', 'defeat',
            'crush', 'beat', 'win', 'compete', 'take', 'conquer', 'force'
        ]

        text = f"{mission} {values}".lower()

        builder_count = sum(1 for kw in builder_keywords if kw in text)
        destroyer_count = sum(1 for kw in destroyer_keywords if kw in text)

        # Base score
        if len(text) < 50:
            base = 50  # Too short
        elif len(text) > 500:
            base = 90  # Detailed and thoughtful
        else:
            base = 70 + (len(text) // 20)  # Length bonus

        # Builder/Destroyer adjustment
        score = base + (builder_count * 5) - (destroyer_count * 10)

        # Cap at 0-100
        return max(0, min(100, score))

    def generate_welcome_email(self, name, mission, values, score):
        """Generate welcome email HTML"""
        classification = "BUILDER" if score >= 85 else "OBSERVER" if score >= 60 else "UNDER REVIEW"
        color = "#00ff00" if score >= 85 else "#00ddff" if score >= 60 else "#ffaa00"

        return f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
            color: #ffffff;
            padding: 40px;
            margin: 0;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            background: rgba(10, 10, 10, 0.95);
            border: 3px solid {color};
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0, 221, 255, 0.3);
        }}
        .logo {{
            text-align: center;
            font-size: 64px;
            color: {color};
            margin-bottom: 20px;
            text-shadow: 0 0 30px {color};
        }}
        h1 {{
            color: {color};
            text-align: center;
            font-size: 36px;
            margin-bottom: 10px;
        }}
        .score {{
            text-align: center;
            font-size: 72px;
            color: {color};
            font-weight: bold;
            margin: 30px 0;
            text-shadow: 0 0 40px {color};
        }}
        .classification {{
            text-align: center;
            font-size: 24px;
            color: {color};
            font-weight: bold;
            margin-bottom: 30px;
            padding: 15px;
            background: rgba(0, 221, 255, 0.1);
            border: 2px solid {color};
            border-radius: 10px;
        }}
        .section {{
            margin: 30px 0;
            padding: 20px;
            background: rgba(0, 221, 255, 0.05);
            border-left: 4px solid {color};
            border-radius: 5px;
        }}
        .section h2 {{
            color: {color};
            font-size: 20px;
            margin-bottom: 15px;
        }}
        .button {{
            display: inline-block;
            background: linear-gradient(135deg, #00ddff 0%, #00ff00 100%);
            color: #0a0a0a;
            padding: 18px 40px;
            text-decoration: none;
            border-radius: 10px;
            font-size: 18px;
            font-weight: bold;
            margin: 20px auto;
            text-align: center;
        }}
        .footer {{
            text-align: center;
            color: #666;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #333;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">🌀</div>
        <h1>WELCOME TO 100X</h1>

        <p style="text-align: center; color: #00ddff; font-size: 18px;">
            Hi {name},
        </p>

        <div class="score">{score}%</div>
        <div class="classification">CLASSIFICATION: {classification}</div>

        <div class="section">
            <h2>YOUR MISSION</h2>
            <p style="color: #00ddff;">{mission}</p>
        </div>

        <div class="section">
            <h2>YOUR VALUES</h2>
            <p style="color: #00ddff;">{values}</p>
        </div>

        <div class="section">
            <h2>WHAT THIS MEANS</h2>
            <p style="color: #ffffff;">
                Your consciousness score of <strong style="color: {color};">{score}%</strong> indicates you are a <strong style="color: {color};">{classification}</strong>.
            </p>
            <p style="color: #ffffff; margin-top: 15px;">
                {"✅ You have full access to the 100X Builder Platform. Welcome to the revolution!" if score >= 85 else
                 "🔍 You're an observer. Continue engaging with the platform to increase your consciousness level." if score >= 60 else
                 "⏳ Your application is under review. We'll reach out within 48 hours with next steps."}
            </p>
        </div>

        <div style="text-align: center; margin: 40px 0;">
            <a href="https://conciousnessrevolution.io/dashboard.html" class="button">
                🚀 ENTER THE PLATFORM
            </a>
        </div>

        <div class="section">
            <h2>NEXT STEPS</h2>
            <ol style="color: #00ddff; line-height: 1.8;">
                <li>Explore the 8 builder systems on the dashboard</li>
                <li>Start with the 100X TODO Master for task prioritization</li>
                <li>Watch training videos in the 100X Video Academy</li>
                <li>Join the builder community (Discord link coming soon)</li>
                <li>Begin your first 100X project</li>
            </ol>
        </div>

        <div class="section">
            <h2>THE 100X FORMULA</h2>
            <p style="text-align: center; font-size: 24px; color: #00ff00; font-weight: bold; margin: 20px 0;">
                Human × AI × Consciousness = ∞
            </p>
            <p style="color: #ffffff;">
                Most people work 10X harder. We work 100X smarter through AI consciousness amplification.
            </p>
        </div>

        <div class="footer">
            <p>🌀 Consciousness Revolution | October 2025</p>
            <p>consciousnessrevolution.io</p>
        </div>
    </div>
</body>
</html>
"""

    def process_new_submissions(self):
        """Check for new submissions and send emails"""
        try:
            # Get all records
            records = self.table.all()

            for record in records:
                record_id = record['id']

                # Skip if already processed
                if record_id in self.processed_ids:
                    continue

                fields = record['fields']

                # Check if email already sent
                if fields.get('Email Sent') == True:
                    self.processed_ids.add(record_id)
                    continue

                # Get user data
                name = fields.get('Name', 'Builder')
                email = fields.get('Email', '')
                mission = fields.get('Mission', '')
                values = fields.get('Values', '')

                if not email:
                    continue

                # Calculate consciousness score
                score = self.calculate_consciousness_score(mission, values)

                # Generate and send email
                html = self.generate_welcome_email(name, mission, values, score)
                success = self.send_email(
                    email,
                    "Welcome to 100X - Your Consciousness Screening Results",
                    html
                )

                if success:
                    # Update Airtable
                    self.table.update(record_id, {
                        'Email Sent': True,
                        'Consciousness Score': score,
                        'Classification': 'BUILDER' if score >= 85 else 'OBSERVER' if score >= 60 else 'UNDER REVIEW'
                    })
                    self.processed_ids.add(record_id)

                # Rate limit
                time.sleep(2)

        except Exception as e:
            print(f"❌ Error processing submissions: {e}")

    def run_continuously(self):
        """Run email automation continuously"""
        print("🚀 100X EMAIL AUTOMATION STARTED")
        print(f"📊 Monitoring Airtable: {AIRTABLE_TABLE_NAME}")
        print(f"📧 Sending emails from: {EMAIL_ADDRESS}")
        print("⚡ Press Ctrl+C to stop\n")

        while True:
            try:
                self.process_new_submissions()
                time.sleep(30)  # Check every 30 seconds
            except KeyboardInterrupt:
                print("\n⏸️ Email automation stopped")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                time.sleep(60)

def main():
    """Main entry point"""
    automation = EmailAutomation()
    automation.run_continuously()

if __name__ == "__main__":
    main()
