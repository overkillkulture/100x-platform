"""
BUG EMAIL NOTIFIER
Sends email updates to fa.sha.man.mc@gmail.com when bugs are fixed
Bug #90 and #86 fix
"""

import smtplib
import json
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pathlib import Path

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
FROM_EMAIL = "darrick.preble@gmail.com"
APP_PASSWORD = "gzzvemuxppfnjsup"
TO_EMAIL = "fa.sha.man.mc@gmail.com"

# Tracking file
SENT_BUGS_FILE = "C:/Users/dwrek/100X_DEPLOYMENT/.bug_tasks/emailed_bugs.json"

def load_sent_bugs():
    """Load list of bugs we've already emailed about"""
    try:
        if Path(SENT_BUGS_FILE).exists():
            with open(SENT_BUGS_FILE, 'r') as f:
                return json.load(f)
        return []
    except:
        return []

def save_sent_bug(bug_number):
    """Mark bug as emailed"""
    sent = load_sent_bugs()
    if bug_number not in sent:
        sent.append(bug_number)
        Path(SENT_BUGS_FILE).parent.mkdir(parents=True, exist_ok=True)
        with open(SENT_BUGS_FILE, 'w') as f:
            json.dump(sent, f)

def send_bug_fix_email(bug_data):
    """Send email notification about a fixed bug"""
    try:
        # Create email
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"✅ Bug #{bug_data['bug_number']} Fixed: {bug_data['title'][:50]}"
        msg['From'] = FROM_EMAIL
        msg['To'] = TO_EMAIL

        # Create HTML email body
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background: #0a0a0a; color: #00ff88; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background: #1a1a1a; border: 2px solid #00ff88; border-radius: 8px; padding: 20px;">
                <h1 style="color: #00ffff;">🐛 Bug Fixed!</h1>

                <div style="background: rgba(0, 255, 136, 0.1); padding: 15px; border-radius: 4px; margin: 20px 0;">
                    <h2 style="color: #00ff88; margin-top: 0;">Bug #{bug_data['bug_number']}</h2>
                    <p><strong>Title:</strong> {bug_data['title']}</p>
                    <p><strong>Reporter:</strong> {bug_data['reporter']}</p>
                </div>

                <div style="margin: 20px 0;">
                    <h3 style="color: #00ffff;">📝 Original Description:</h3>
                    <p style="color: #e8e8e8; line-height: 1.6;">{bug_data.get('description', 'No description')[:500]}</p>
                </div>

                <div style="background: rgba(0, 255, 255, 0.1); padding: 15px; border-radius: 4px; margin: 20px 0;">
                    <h3 style="color: #00ffff; margin-top: 0;">✅ What Was Fixed:</h3>
                    <p style="color: #e8e8e8; line-height: 1.6;">{bug_data.get('fix_description', 'Fix completed')}</p>
                </div>

                <div style="margin: 20px 0;">
                    <h3 style="color: #00ffff;">📍 Where:</h3>
                    <p style="color: #e8e8e8;">
                        {bug_data.get('files_changed', 'Multiple files updated')}
                    </p>
                </div>

                <div style="margin: 20px 0;">
                    <h3 style="color: #00ffff;">⏰ When:</h3>
                    <p style="color: #e8e8e8;">Fixed at: {bug_data.get('fixed_at', 'Just now')}</p>
                </div>

                <div style="margin: 30px 0; padding: 20px; background: rgba(0, 255, 136, 0.05); border-left: 4px solid #00ff88; border-radius: 4px;">
                    <h3 style="color: #00ff88; margin-top: 0;">🚀 Status:</h3>
                    <p style="color: #e8e8e8; font-size: 1.1em;">
                        ✅ Fix deployed to production<br>
                        🌐 Live at: <a href="https://conciousnessrevolution.io" style="color: #00ffff;">conciousnessrevolution.io</a>
                    </p>
                </div>

                <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #333; text-align: center; color: #888;">
                    <p>Automated notification from Consciousness Revolution Bug System</p>
                    <p style="font-size: 0.9em;">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
            </div>
        </body>
        </html>
        """

        msg.attach(MIMEText(html_body, 'html'))

        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(FROM_EMAIL, APP_PASSWORD)
            server.send_message(msg)

        print(f"✅ Email sent for Bug #{bug_data['bug_number']}")
        return True

    except Exception as e:
        print(f"❌ Failed to send email for Bug #{bug_data['bug_number']}: {e}")
        return False

def check_for_completed_bugs():
    """Check .bug_tasks directory for newly completed bugs"""
    task_dir = Path("C:/Users/dwrek/100X_DEPLOYMENT/.bug_tasks")
    sent_bugs = load_sent_bugs()

    if not task_dir.exists():
        print("No .bug_tasks directory found")
        return

    # Check all bug task files
    for bug_file in task_dir.glob("bug_*.json"):
        try:
            with open(bug_file, 'r') as f:
                bug_data = json.load(f)

            bug_number = bug_data.get('bug_number')
            status = bug_data.get('status')

            # If bug is completed and we haven't emailed about it yet
            if status == 'completed' and bug_number not in sent_bugs:
                print(f"\n{'='*60}")
                print(f"📧 Found completed bug #{bug_number} - sending email...")

                if send_bug_fix_email(bug_data):
                    save_sent_bug(bug_number)
                    print(f"✅ Email sent and logged for Bug #{bug_number}")
                else:
                    print(f"❌ Failed to send email for Bug #{bug_number}")

                print(f"{'='*60}\n")
                time.sleep(2)  # Prevent rate limiting

        except Exception as e:
            print(f"Error processing {bug_file}: {e}")

def main():
    """Main monitoring loop"""
    print("="*60)
    print("📧 BUG EMAIL NOTIFIER")
    print("="*60)
    print(f"Monitoring: C:/Users/dwrek/100X_DEPLOYMENT/.bug_tasks")
    print(f"Sending to: {TO_EMAIL}")
    print(f"Check interval: 30 seconds")
    print("="*60)
    print()

    check_count = 0
    while True:
        check_count += 1
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Check #{check_count}")

        try:
            check_for_completed_bugs()
            print(f"✓ Check complete")
        except Exception as e:
            print(f"✗ Error during check: {e}")

        time.sleep(30)

if __name__ == "__main__":
    main()
