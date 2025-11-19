"""
📧 SEND BETA UPDATE EMAIL - October 27, 2025
Sends beta update to all 9 testers
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from pathlib import Path

# Beta tester email list (9 total)
BETA_TESTERS = [
    "joshua.serrano2022@gmail.com",
    "tobyburrowes@hotmail.com",
    "wdbrotherton@gmail.com",
    "deansabrwork@gmail.com",
    "varniwilliam@gmail.com",
    "ruuutherford@gmail.com",
    "angeline.realm@gmail.com",
    "information.crypt@pm.me",
    "HAWAIILIVESTOCK@GMAIL.COM"
]

# Email content
SUBJECT = "🎉 Beta Update: Bug System Live + Major Progress"

# Read email body from file
email_body_file = Path("C:/Users/dwrek/100X_DEPLOYMENT/BETA_UPDATE_OCT_27_2025_BUG_SYSTEM_LIVE.md")
with open(email_body_file, 'r', encoding='utf-8') as f:
    EMAIL_BODY = f.read()

def send_email():
    """Send beta update email to all testers"""

    print("\n" + "="*70)
    print("📧 SENDING BETA UPDATE EMAIL")
    print("="*70)

    # Get email credentials from environment
    sender_email = os.getenv('GMAIL_ADDRESS')
    sender_password = os.getenv('GMAIL_APP_PASSWORD')

    if not sender_email or not sender_password:
        print("\n⚠️  Email credentials not found in environment variables")
        print("\nTo send emails, set these environment variables:")
        print("  GMAIL_ADDRESS = your.email@gmail.com")
        print("  GMAIL_APP_PASSWORD = your_app_password")
        print("\nAlternatively, you can:")
        print("1. Copy the email content from BETA_UPDATE_OCT_27_2025_BUG_SYSTEM_LIVE.md")
        print("2. Manually send via Gmail with BCC to all 9 testers")
        print("\n📋 BCC Email List:")
        print(", ".join(BETA_TESTERS))
        print("\n" + "="*70)
        return

    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = sender_email
        msg['To'] = sender_email  # Send to self
        msg['Bcc'] = ", ".join(BETA_TESTERS)  # BCC all beta testers
        msg['Subject'] = SUBJECT

        # Attach email body (plain text)
        part = MIMEText(EMAIL_BODY, 'plain')
        msg.attach(part)

        # Connect to Gmail SMTP server
        print("\n📡 Connecting to Gmail SMTP server...")
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, sender_password)

        # Send email
        print(f"\n📤 Sending to {len(BETA_TESTERS)} beta testers...")
        server.send_message(msg)
        server.quit()

        print("\n✅ EMAIL SENT SUCCESSFULLY!")
        print(f"   Recipients: {len(BETA_TESTERS)} beta testers")
        print(f"   Subject: {SUBJECT}")
        print("\n" + "="*70)

        # Log sent email
        log_file = Path("C:/Users/dwrek/100X_DEPLOYMENT/BETA_EMAILS_SENT_LOG.txt")
        with open(log_file, 'a') as f:
            from datetime import datetime
            f.write(f"\n[{datetime.now()}] Beta update sent to {len(BETA_TESTERS)} testers")
            f.write(f"\nSubject: {SUBJECT}\n")

    except Exception as e:
        print(f"\n❌ Error sending email: {e}")
        print("\n📋 Manual Send Instructions:")
        print(f"1. Open Gmail")
        print(f"2. Compose new email")
        print(f"3. Subject: {SUBJECT}")
        print(f"4. BCC: {', '.join(BETA_TESTERS)}")
        print(f"5. Copy content from: BETA_UPDATE_OCT_27_2025_BUG_SYSTEM_LIVE.md")
        print(f"6. Send")
        print("\n" + "="*70)

if __name__ == '__main__':
    send_email()
