"""
📱 SMS BUG NOTIFIER FOR DOBBS
Direct SMS notifications when bugs are fixed - no GitHub API needed!

This replaces the GitHub token dependency with direct SMS to Dobbs.
"""

import json
import time
from pathlib import Path
from datetime import datetime
from twilio.rest import Client

# Twilio credentials
ACCOUNT_SID = "AC379092b0f6d4465323a78fac08cfc72c"
AUTH_TOKEN = "340ca721c94a987177658a47bcf5a0d8"
FROM_NUMBER = "+15092166552"  # Idaho number

# Dobbs's phone number
DOBBS_PHONE = "+19147740843"  # Christopher Michael Dobbins

# Bug tasks directory
BUG_TASKS_DIR = Path("C:/Users/dwrek/100X_DEPLOYMENT/.bug_tasks")
SENT_SMS_FILE = BUG_TASKS_DIR / "sms_sent.json"

def load_sent_sms():
    """Load list of bugs we've already texted about"""
    if SENT_SMS_FILE.exists():
        with open(SENT_SMS_FILE, 'r') as f:
            return set(json.load(f))
    return set()

def save_sent_sms(bug_number):
    """Mark bug as texted"""
    sent = load_sent_sms()
    sent.add(bug_number)
    with open(SENT_SMS_FILE, 'w') as f:
        json.dump(list(sent), f)

def send_bug_fix_sms(bug_data):
    """Send SMS to Dobbs about fixed bug"""

    try:
        client = Client(ACCOUNT_SID, AUTH_TOKEN)

        # Create short SMS message (SMS has 160 char limit, but we can send longer)
        message_body = f"""✅ BUG #{bug_data['bug_number']} FIXED!

{bug_data['title'][:50]}

WHAT WAS FIXED:
{bug_data.get('fix_description', 'Completed')[:150]}

LIVE SITE:
https://conciousnessrevolution.io

- CR Build System"""

        message = client.messages.create(
            body=message_body,
            from_=FROM_NUMBER,
            to=DOBBS_PHONE
        )

        print(f"✅ SMS sent to Dobbs for Bug #{bug_data['bug_number']}")
        print(f"   Message SID: {message.sid}")
        return True

    except Exception as e:
        print(f"❌ Failed to send SMS: {e}")
        return False

def check_and_notify():
    """Check for completed bugs and send SMS"""

    if not BUG_TASKS_DIR.exists():
        print(f"❌ Bug tasks directory not found: {BUG_TASKS_DIR}")
        return

    sent_bugs = load_sent_sms()

    for bug_file in BUG_TASKS_DIR.glob("bug_*.json"):
        try:
            with open(bug_file, 'r') as f:
                bug_data = json.load(f)

            bug_number = bug_data.get('bug_number')
            status = bug_data.get('status')

            # If bug is completed and we haven't texted about it yet
            if status == 'completed' and bug_number not in sent_bugs:
                print(f"\n📱 New completed bug found: #{bug_number}")

                if send_bug_fix_sms(bug_data):
                    save_sent_sms(bug_number)
                    print(f"   ✅ Dobbs notified via SMS")
                else:
                    print(f"   ❌ Failed to notify Dobbs")

                # Wait between messages to avoid rate limits
                time.sleep(2)

        except Exception as e:
            print(f"❌ Error processing {bug_file.name}: {e}")

def run_monitor():
    """Continuously monitor for completed bugs and send SMS"""

    print("="*70)
    print("📱 SMS BUG NOTIFIER FOR DOBBS")
    print("="*70)
    print(f"Monitoring: {BUG_TASKS_DIR}")
    print(f"Texting to: {DOBBS_PHONE}")
    print(f"From: {FROM_NUMBER}")
    print()
    print("Press Ctrl+C to stop")
    print("="*70)
    print()

    if DOBBS_PHONE == "+1XXXXXXXXXX":
        print("⚠️  WARNING: DOBBS_PHONE not set!")
        print("   Edit this file and add Dobbs's phone number")
        print("   Then restart the script")
        return

    try:
        while True:
            check_and_notify()
            time.sleep(30)  # Check every 30 seconds
    except KeyboardInterrupt:
        print("\n\n✅ SMS notifier stopped")

def send_test_sms(test_number=None):
    """Send test SMS to verify system works"""

    if test_number is None:
        test_number = input("Enter phone number to test (e.g., +15551234567): ")

    print(f"\n📤 Sending test SMS to {test_number}...")

    try:
        client = Client(ACCOUNT_SID, AUTH_TOKEN)

        message = client.messages.create(
            body="""🧪 TEST MESSAGE

This is a test of the Consciousness Revolution bug notification system.

If you're receiving this, the SMS system is working!

✅ All systems operational

- CR Build System""",
            from_=FROM_NUMBER,
            to=test_number
        )

        print(f"✅ Test SMS sent!")
        print(f"   SID: {message.sid}")
        print(f"   View in Twilio: https://twilio.com/console/sms/logs/{message.sid}")
        return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == '__main__':
    import sys

    print("\n" + "="*70)
    print("📱 SMS BUG NOTIFIER FOR DOBBS")
    print("="*70)
    print()

    if len(sys.argv) > 1:
        if sys.argv[1] == '--test':
            # Test mode
            test_num = sys.argv[2] if len(sys.argv) > 2 else None
            send_test_sms(test_num)
        elif sys.argv[1] == '--once':
            # Check once and exit
            check_and_notify()
        else:
            print(f"Unknown option: {sys.argv[1]}")
            print("Usage:")
            print("  python BUG_SMS_NOTIFIER_DOBBS.py           # Run continuous monitor")
            print("  python BUG_SMS_NOTIFIER_DOBBS.py --test    # Send test SMS")
            print("  python BUG_SMS_NOTIFIER_DOBBS.py --once    # Check once and exit")
    else:
        # Default: run continuous monitor
        run_monitor()
