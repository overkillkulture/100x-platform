"""
📱 SEND SMS TO ALL BETA TESTERS
Re-engage them with the new SMS bug system
"""

import os
from twilio.rest import Client

# Twilio credentials
ACCOUNT_SID = "AC379092b0f6d4465323a78fac08cfc72c"
AUTH_TOKEN = "340ca721c94a987177658a47bcf5a0d8"
FROM_NUMBER = "+15092166552"  # Idaho number

# Beta tester phone numbers (NEED TO ADD THESE)
BETA_TESTERS = {
    "Joshua": "+1XXXXXXXXXX",  # joshua.serrano2022@gmail.com
    "Toby": "+1XXXXXXXXXX",     # tobyburrowes@hotmail.com
    "William": "+1XXXXXXXXXX",  # wdbrotherton@gmail.com
    "Dean": "+1XXXXXXXXXX",     # deansabrwork@gmail.com
    "Varni": "+1XXXXXXXXXX",    # varniwilliam@gmail.com
    "Ruth": "+1XXXXXXXXXX",     # ruuutherford@gmail.com
    "Angeline": "+1XXXXXXXXXX", # angeline.realm@gmail.com
    "Alex": "+1XXXXXXXXXX",     # information.crypt@pm.me
    "Hawaii": "+1XXXXXXXXXX",   # HAWAIILIVESTOCK@GMAIL.COM
}

# The exciting message
MESSAGE = """🚀 CONSCIOUSNESS REVOLUTION UPDATE

We heard you! Bug reporting is now EASY:

📱 Text bugs directly to this number!

No forms, no logins, no hassle.
Just text what's broken.

You'll get instant confirmation ✅

Format:
"BUG: [what's broken]
DETAILS: [what happened]"

Or just text anything - we'll figure it out!

Ready to help us build the future? 🌌

- Commander & the CR team"""

def send_sms_to_all():
    """Send SMS to all beta testers"""

    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    print("📱 SENDING SMS TO BETA TESTERS")
    print("="*70)
    print()

    for name, phone in BETA_TESTERS.items():
        if phone == "+1XXXXXXXXXX":
            print(f"⚠️  {name}: No phone number on file")
            continue

        try:
            print(f"📤 Sending to {name} ({phone})...")

            message = client.messages.create(
                body=MESSAGE,
                from_=FROM_NUMBER,
                to=phone
            )

            print(f"   ✅ Sent! SID: {message.sid}")

        except Exception as e:
            print(f"   ❌ Failed: {str(e)}")

        print()

    print("="*70)
    print("✅ DONE")


def send_test_sms(to_number):
    """Send test SMS to one number"""

    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    print(f"📤 Sending test SMS to {to_number}...")

    try:
        message = client.messages.create(
            body=MESSAGE,
            from_=FROM_NUMBER,
            to=to_number
        )

        print(f"✅ Sent! SID: {message.sid}")
        print(f"View in Twilio: https://twilio.com/console/sms/logs/{message.sid}")

        return True

    except Exception as e:
        print(f"❌ Failed: {str(e)}")
        return False


if __name__ == '__main__':
    import sys

    print("\n" + "="*70)
    print("📱 SMS TO BETA TESTERS")
    print("="*70)
    print()

    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        # Test mode: send to your phone first
        test_number = input("Enter YOUR phone number to test (e.g., +15551234567): ")
        send_test_sms(test_number)

    else:
        print("⚠️  IMPORTANT: Before sending to all testers:")
        print("1. Add their phone numbers to BETA_TESTERS dict in this file")
        print("2. Run with --test flag to test on your phone first")
        print("3. Then run without flags to send to everyone")
        print()
        print("Example:")
        print("  python SEND_SMS_TO_BETA_TESTERS.py --test")
        print("  python SEND_SMS_TO_BETA_TESTERS.py")
        print()

        answer = input("Continue anyway? (yes/no): ")
        if answer.lower() == 'yes':
            send_sms_to_all()
