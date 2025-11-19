"""
Send email to all beta testers about SMS bug reporting
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Beta tester emails
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
SUBJECT = "🚀 Bug Reporting Just Got Easy - Text Us!"

BODY = """Hey everyone!

We heard you - bug reporting is now SUPER easy.

🚀 Just text bugs to this number:

📱 +1 (509) 216-6552

No forms, no logins, no hassle.

How it works:
1. Find a bug
2. Text what's broken to that number
3. Get instant confirmation
4. Done!

Format (or just wing it):
"BUG: Login button broken
DETAILS: When I click submit, nothing happens"

You'll get a text back confirming we received it, with a link to track it.

That's it!

Thanks for helping us build something amazing.

- Commander & the Consciousness Revolution team

P.S. This number works 24/7. Text anytime!
"""

def send_email():
    """Send email to all beta testers"""

    # Get Gmail credentials from environment
    gmail_address = os.getenv('GMAIL_ADDRESS')
    gmail_password = os.getenv('GMAIL_APP_PASSWORD')

    if not gmail_address or not gmail_password:
        print("⚠️  Gmail credentials not found in environment variables")
        print()
        print("Need to set:")
        print("  GMAIL_ADDRESS")
        print("  GMAIL_APP_PASSWORD")
        print()
        print("Alternatively, I can create instructions for manual sending...")
        return False

    print("📧 Sending email to beta testers...")
    print()

    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = gmail_address
        msg['To'] = gmail_address  # Send to self
        msg['Bcc'] = ", ".join(BETA_TESTERS)  # BCC all testers
        msg['Subject'] = SUBJECT

        msg.attach(MIMEText(BODY, 'plain'))

        # Connect to Gmail
        print("🔐 Connecting to Gmail SMTP...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_address, gmail_password)

        # Send
        print("📤 Sending to 9 beta testers...")
        server.send_message(msg)
        server.quit()

        print()
        print("✅ EMAIL SENT SUCCESSFULLY!")
        print()
        print(f"Sent to: {len(BETA_TESTERS)} beta testers")
        print()
        return True

    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False


def create_manual_instructions():
    """Create manual email instructions"""

    print()
    print("="*70)
    print("📧 MANUAL EMAIL INSTRUCTIONS")
    print("="*70)
    print()
    print("1. Open Gmail")
    print("2. Click Compose")
    print("3. In BCC field, paste:")
    print()
    print(", ".join(BETA_TESTERS))
    print()
    print("4. Subject:")
    print(SUBJECT)
    print()
    print("5. Body:")
    print()
    print(BODY)
    print()
    print("6. Send!")
    print()


if __name__ == '__main__':
    print()
    print("="*70)
    print("📧 SENDING BETA TESTER NOTIFICATION")
    print("="*70)
    print()

    # Try automated sending
    success = send_email()

    if not success:
        # Fall back to manual instructions
        create_manual_instructions()

        print("="*70)
        print()
        print("Copy the text above and send manually via Gmail.")
