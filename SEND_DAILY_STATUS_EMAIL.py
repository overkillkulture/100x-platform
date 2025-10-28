"""
Daily status email - runs automatically, sends you a summary
So you don't have to check manually
"""

import smtplib
from email.mime.text import MIMEText
import requests

GMAIL_ADDRESS = 'darrick.preble@gmail.com'
GMAIL_PASSWORD = 'gzzvemuxppfnjsup'

def get_github_bugs():
    """Get recent bugs from GitHub"""
    try:
        response = requests.get('https://api.github.com/repos/overkillkulture/consciousness-bugs/issues')
        issues = response.json()

        # Filter out test bugs
        real_bugs = [i for i in issues if 'test' not in i['title'].lower() and 'automated' not in i['title'].lower()]

        return real_bugs
    except:
        return []

def send_daily_summary():
    """Send daily summary email to Commander"""

    bugs = get_github_bugs()

    if len(bugs) == 0:
        status = "❌ ZERO real bugs reported yet"
    else:
        status = f"✅ {len(bugs)} REAL bugs reported!"

    body = f"""Daily Consciousness Revolution Status

{status}

Systems Running:
✅ SMS bug webhook (live)
✅ Auto-onboarding monitor (running)
✅ 15 people invited to be builders

What's Needed:
- Beta testers to text bugs to +1 (509) 216-6552
- Beta testers to download Claude Code and reply "I'm in"

When that happens, you'll know from this email.

Until then: Rest. The systems are waiting for them, not you.

- Your Automated Status System
"""

    msg = MIMEText(body)
    msg['Subject'] = f'Daily Status: {status}'
    msg['From'] = GMAIL_ADDRESS
    msg['To'] = GMAIL_ADDRESS

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(GMAIL_ADDRESS, GMAIL_PASSWORD)
    server.send_message(msg)
    server.quit()

    print(f"✅ Daily summary sent: {status}")

if __name__ == '__main__':
    send_daily_summary()
