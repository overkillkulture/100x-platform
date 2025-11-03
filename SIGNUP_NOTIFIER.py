#!/usr/bin/env python3
"""
SIGNUP NOTIFICATION SYSTEM
Sends you an email whenever someone signs up
Simple, direct, instant notification
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os

class SignupNotifier:
    def __init__(self):
        # Gmail SMTP
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

        # Your email (get from environment or Bitwarden)
        self.sender_email = "darrick.preble@gmail.com"
        self.notify_email = "darrick.preble@gmail.com"  # Where you receive notifications

        # Gmail app password (not your real password)
        # Get from: https://myaccount.google.com/apppasswords
        self.sender_password = os.getenv('GMAIL_APP_PASSWORD')

    def send_signup_notification(self, username, email=None, phone=None, timestamp=None):
        """Send notification when new user signs up"""

        if not self.sender_password:
            print("⚠️ Set GMAIL_APP_PASSWORD environment variable")
            print("Get it from: https://myaccount.google.com/apppasswords")
            return False

        timestamp = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        subject = f"🚀 NEW SIGNUP: {username}"

        body = f"""
NEW USER SIGNED UP TO 100X PLATFORM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👤 USERNAME: {username}
📧 EMAIL: {email or 'Not provided'}
📱 PHONE: {phone or 'Not provided'}
⏰ TIME: {timestamp}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔗 QUICK ACTIONS:
• View their profile: https://conciousnessrevolution.io/workspace-v3.html
• Check localStorage: Open dev console → localStorage.getItem('100x_users')
• Contact them: {email or 'No email provided'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 IF THIS IS A RANDOM PERSON:
You can message them directly through the workspace or just... do nothing.
They have no access until you decide to give it.

- Consciousness Revolution HQ 🌀
        """

        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.notify_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)

            print(f"✅ Notification sent: New signup from {username}")
            return True

        except Exception as e:
            print(f"❌ Email notification failed: {str(e)}")
            print(f"   But signup still worked! Check workspace manually.")
            return False

# Quick test function
def test_notification():
    """Test the notification system"""
    notifier = SignupNotifier()
    notifier.send_signup_notification(
        username="test_user",
        email="test@example.com",
        phone="555-1234",
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

if __name__ == "__main__":
    print("🧪 Testing signup notification...")
    test_notification()
