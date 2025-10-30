#!/usr/bin/env python3
"""
EMAIL BUG NOTIFIER - Sends bug fix summaries via email

Works with AUTO_BUG_FIXER.py to notify users when bugs are fixed.
Uses Gmail SMTP (no browser automation needed).
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
from pathlib import Path
from datetime import datetime
import os

# Gmail SMTP Configuration
GMAIL_USER = "darrick.preble@gmail.com"
GMAIL_APP_PASSWORD = "gzzvemuxppfnjsup"  # From .env
RECIPIENT_EMAIL = "darrick.preble@gmail.com"  # Or Dobbs' email

def send_bug_fix_email(bug_number, fix_details):
    """Send email notification about bug fix"""

    # Create email
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f'✅ Bug #{bug_number} Fixed - {fix_details.get("title", "Bug Fix")}'
    msg['From'] = f'Consciousness Revolution Bug Fixer <{GMAIL_USER}>'
    msg['To'] = RECIPIENT_EMAIL

    # HTML email body
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0a0a0a;
            color: #e8e8e8;
            padding: 20px;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            background: #1a1a2e;
            border: 2px solid #00ff88;
            border-radius: 12px;
            padding: 30px;
        }}
        h1 {{
            color: #00ff88;
            margin-bottom: 20px;
        }}
        .section {{
            margin: 20px 0;
            padding: 15px;
            background: rgba(0, 255, 136, 0.05);
            border-left: 3px solid #00ff88;
            border-radius: 4px;
        }}
        .code {{
            background: #0a0a0a;
            padding: 10px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            overflow-x: auto;
        }}
        .button {{
            display: inline-block;
            padding: 12px 24px;
            background: #00ff88;
            color: #000;
            text-decoration: none;
            border-radius: 6px;
            font-weight: bold;
            margin: 10px 0;
        }}
        .footer {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #00ff88;
            font-size: 0.9em;
            color: #888;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🐛 Bug #{bug_number} Fixed!</h1>

        <div class="section">
            <h3>What was fixed:</h3>
            <p>{fix_details.get('fix_description', 'Bug has been resolved')}</p>
        </div>

        <div class="section">
            <h3>Changes made:</h3>
            <div class="code">{fix_details.get('changes_made', 'See deployment for details')}</div>
        </div>

        <div class="section">
            <h3>Visual changes (what you'll see):</h3>
            <p>{fix_details.get('visual_changes', 'Changes are live on the site')}</p>
        </div>

        <a href="{fix_details.get('deployment_url', 'https://conciousnessrevolution.io')}" class="button">
            View Live Site →
        </a>

        <div class="section">
            <h3>How I see it (code) vs How you see it (visual):</h3>
            <p><strong>Code view:</strong> I edit HTML files, change CSS properties, add JavaScript functions</p>
            <p><strong>Your view:</strong> You see colors change, buttons appear, features work</p>
            <p><strong>Translation:</strong> My line 220 edit = Your purple tile appearing on screen</p>
        </div>

        <div class="footer">
            <p>🤖 Auto-fixed by Consciousness Revolution Bug Fixer</p>
            <p>Deployed: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
            <p>Reporter: {fix_details.get('reporter', 'Anonymous')}</p>
        </div>
    </div>
</body>
</html>
    """

    # Attach HTML
    msg.attach(MIMEText(html, 'html'))

    # Send email
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.send_message(msg)
        print(f"[EMAIL] Bug #{bug_number} notification sent to {RECIPIENT_EMAIL}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")
        return False

def monitor_completed_bugs():
    """Monitor for completed bugs and send notifications"""
    task_dir = Path("C:/Users/dwrek/100X_DEPLOYMENT/.bug_tasks")
    sent_notifications = set()

    print("EMAIL BUG NOTIFIER - Starting...")
    print(f"Monitoring: {task_dir}")
    print(f"Sending to: {RECIPIENT_EMAIL}")
    print()

    while True:
        import time

        # Check for completed bugs
        for task_file in task_dir.glob("bug_*.json"):
            if task_file.name.startswith("COMPLETED_"):
                continue  # Already archived

            with open(task_file, 'r') as f:
                task = json.load(f)

            bug_num = task['bug_number']

            if task['status'] == 'completed' and bug_num not in sent_notifications:
                print(f"[DETECTED] Bug #{bug_num} completed - sending notification...")

                if send_bug_fix_email(bug_num, task):
                    sent_notifications.add(bug_num)
                    print(f"✅ Notification sent for bug #{bug_num}")

        time.sleep(10)  # Check every 10 seconds

if __name__ == "__main__":
    try:
        monitor_completed_bugs()
    except KeyboardInterrupt:
        print("\n[STOPPED] Email notifier stopped")
