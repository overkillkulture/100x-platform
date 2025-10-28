"""
Auto-send builder package when beta testers reply "I'm in"

This monitors Gmail for replies containing "I'm in" and automatically sends them:
1. Link to GitHub repo
2. Builder onboarding package
3. Next steps

Run this in background to automate onboarding.
"""

import imaplib
import email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

GMAIL_ADDRESS = 'darrick.preble@gmail.com'
GMAIL_PASSWORD = 'gzzvemuxppfnjsup'

BETA_TESTER_EMAILS = [
    'joshua.serrano2022@gmail.com',
    'tobyburrowes@hotmail.com',
    'wdbrotherton@gmail.com',
    'deansabrwork@gmail.com',
    'varniwilliam@gmail.com',
    'ruuutherford@gmail.com',
    'angeline.realm@gmail.com',
    'information.crypt@pm.me',
    'HAWAIILIVESTOCK@GMAIL.COM'
]

BUILDER_RESPONSE_EMAIL = """🚀 WELCOME BUILDER!

You're in. Here's everything you need:

## STEP 1: GET THE WORKSPACE

GitHub Repo:
https://github.com/overkillkulture/consciousness-revolution

Clone it:
git clone https://github.com/overkillkulture/consciousness-revolution
cd consciousness-revolution

## STEP 2: GET CREDENTIALS

I'm attaching the builder credentials separately.
(Check next email for CREDENTIALS.txt)

## STEP 3: CONFIGURE CLAUDE CODE

Copy CLAUDE.md to your home directory:
cp CLAUDE.md ~/CLAUDE.md

Then open Claude Code and say:
"I'm a builder for Consciousness Revolution. Read ~/CLAUDE.md and show me what to work on."

## STEP 4: START BUILDING

You have FULL access:
- Deploy to production
- Commit to main
- Send beta tester emails
- Everything Commander can do

Don't ask permission. Just build.

## NEED HELP?

Text Commander: +1 (509) 216-6552
Or ask Claude Code - it knows everything.

Welcome to the revolution. Now let's build. 🌌

- Commander
"""

def check_for_replies():
    """Check Gmail for 'I'm in' replies from beta testers"""

    print("🔍 Checking Gmail for builder responses...")

    # Connect to Gmail
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(GMAIL_ADDRESS, GMAIL_PASSWORD)
    mail.select('inbox')

    # Search for recent emails from beta testers
    status, messages = mail.search(None, 'UNSEEN')

    if status != 'OK':
        print("No new messages")
        return []

    new_builders = []

    for num in messages[0].split():
        status, data = mail.fetch(num, '(RFC822)')
        if status != 'OK':
            continue

        msg = email.message_from_bytes(data[0][1])
        from_email = email.utils.parseaddr(msg['From'])[1]
        subject = msg['Subject']

        # Check if from beta tester
        if from_email.lower() not in [e.lower() for e in BETA_TESTER_EMAILS]:
            continue

        # Get body
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = msg.get_payload(decode=True).decode()

        # Check for "I'm in" or similar
        if any(phrase in body.lower() for phrase in ["i'm in", "im in", "i am in", "ready", "signed up"]):
            print(f"✅ Found builder: {from_email}")
            new_builders.append(from_email)

    mail.close()
    mail.logout()

    return new_builders

def send_builder_package(to_email):
    """Send builder package to new builder"""

    print(f"📤 Sending builder package to {to_email}...")

    msg = MIMEMultipart()
    msg['From'] = GMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = "🚀 Your Builder Access - Consciousness Revolution"

    msg.attach(MIMEText(BUILDER_RESPONSE_EMAIL, 'plain'))

    # Send
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(GMAIL_ADDRESS, GMAIL_PASSWORD)
    server.send_message(msg)
    server.quit()

    print(f"✅ Builder package sent to {to_email}")

def monitor_continuously():
    """Run continuously checking for new builders"""

    print("="*70)
    print("🤖 AUTO BUILDER ONBOARDING - MONITORING GMAIL")
    print("="*70)
    print()
    print("Watching for beta tester replies containing:")
    print("- 'I'm in'")
    print("- 'ready'")
    print("- 'signed up'")
    print()
    print("When detected, automatically sends builder package.")
    print()
    print("Press Ctrl+C to stop")
    print("="*70)
    print()

    while True:
        try:
            new_builders = check_for_replies()

            for builder_email in new_builders:
                send_builder_package(builder_email)
                print(f"🎉 NEW BUILDER ONBOARDED: {builder_email}")
                print()

            if new_builders:
                print(f"✅ Onboarded {len(new_builders)} new builders this check")

            # Check every 5 minutes
            print(f"💤 Sleeping 5 minutes... (next check at {time.strftime('%I:%M %p')})")
            time.sleep(300)

        except KeyboardInterrupt:
            print()
            print("👋 Stopping builder monitoring")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Retrying in 1 minute...")
            time.sleep(60)

if __name__ == '__main__':
    monitor_continuously()
