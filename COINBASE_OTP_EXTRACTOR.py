"""
COINBASE OTP EXTRACTOR - Get your $5K out NOW
Trinity C1 Mechanic Build - Immediate extraction protocol

PROBLEM: $5K stuck in Coinbase, OTP blocked
SOLUTION: Auto-read Coinbase OTP codes from Twilio, extract funds

STATUS: READY TO RUN
"""

import sys
import time
from SMS_CODE_READER import TwilioSMSReader

class CoinbaseOTPExtractor:
    def __init__(self):
        """Initialize Twilio SMS reader for Coinbase codes"""
        self.sms_reader = TwilioSMSReader()
        print("🏦 COINBASE OTP EXTRACTOR ACTIVATED")
        print("=" * 60)
        print()
        print("Phone: 509-216-6552 (Twilio)")
        print("Target: $5,000 extraction from Coinbase")
        print()
        print("=" * 60)
        print()

    def get_coinbase_otp(self, wait_time=120):
        """
        Get Coinbase OTP code

        Args:
            wait_time: How long to wait for code (default 2 minutes)

        Returns:
            OTP code (string) or None
        """

        print("📱 STEP 1: Trigger OTP in Coinbase")
        print("-" * 60)
        print()
        print("ACTION REQUIRED:")
        print("1. Open Coinbase in browser")
        print("2. Start withdrawal process")
        print("3. Click 'Send SMS Code' when prompted")
        print()
        print("I'll monitor for the code automatically...")
        print()
        print("=" * 60)

        input("Press ENTER after clicking 'Send SMS Code' in Coinbase...")

        print()
        print("🔍 Monitoring SMS for Coinbase OTP code...")
        print(f"⏳ Will check for {wait_time} seconds...")
        print()

        # Check every 5 seconds for the code
        checks = wait_time // 5

        for i in range(checks):
            print(f"Check {i+1}/{checks}... ", end="", flush=True)

            code = self.sms_reader.get_latest_code(
                service_name="coinbase",
                minutes_back=3
            )

            if code:
                print()
                print()
                print("=" * 60)
                print("✅ COINBASE OTP CODE RECEIVED!")
                print("=" * 60)
                print()
                print(f"🔐 CODE: {code}")
                print()
                print("=" * 60)
                print()
                print("NEXT STEP:")
                print("1. Enter this code in Coinbase")
                print("2. Complete withdrawal")
                print("3. Your $5K will be free! 🎉")
                print()
                return code

            print("waiting...")
            time.sleep(5)

        print()
        print()
        print("❌ No code received in", wait_time, "seconds")
        print()
        print("TROUBLESHOOTING:")
        print("1. Verify Coinbase has correct phone: 509-216-6552")
        print("2. Check if SMS was sent (may take 30-60 seconds)")
        print("3. Try running script again")
        print()

        return None

    def monitor_continuous(self):
        """
        Continuously monitor for Coinbase codes
        Great for multiple withdrawal attempts
        """

        print("🔄 CONTINUOUS MONITORING MODE")
        print("=" * 60)
        print()
        print("This will watch for Coinbase OTP codes indefinitely")
        print("Press Ctrl+C to stop")
        print()
        print("=" * 60)
        print()

        def handle_coinbase_code(code, message):
            """Auto-display Coinbase codes"""
            print()
            print("=" * 60)
            print("🔔 NEW COINBASE CODE!")
            print("=" * 60)
            print()
            print(f"🔐 CODE: {code}")
            print()
            print("Enter this in Coinbase NOW!")
            print()
            print("=" * 60)
            print()

        self.sms_reader.monitor_codes(callback=handle_coinbase_code)


def test_sms_system():
    """Test if Twilio is receiving SMS"""

    print()
    print("🧪 TESTING SMS SYSTEM")
    print("=" * 60)
    print()

    reader = TwilioSMSReader()

    print("Checking recent messages (last 24 hours)...")
    print()

    messages = reader.get_recent_messages(minutes_back=1440)  # 24 hours

    if messages:
        print(f"✅ Found {len(messages)} recent messages!")
        print()
        print("Latest messages:")
        for i, msg in enumerate(messages[:5]):
            print(f"{i+1}. From: {msg['from']}")
            print(f"   Body: {msg['body'][:50]}...")
            print()

        print("SMS SYSTEM IS WORKING! ✅")
        return True
    else:
        print("⚠️  No recent messages found")
        print()
        print("This means either:")
        print("1. No SMS received in last 24 hours (normal)")
        print("2. Twilio credentials need updating")
        print()
        print("Try sending a test SMS to: 509-216-6552")
        return False


# =============================================================================
# MAIN EXECUTION - THREE MODES
# =============================================================================

if __name__ == "__main__":

    print()
    print("💰" * 30)
    print()
    print("        COINBASE $5K LIBERATION PROTOCOL")
    print("           Trinity C1 Mechanic Build")
    print()
    print("💰" * 30)
    print()

    print("Choose mode:")
    print()
    print("1. TEST SMS SYSTEM (recommended first)")
    print("2. GET COINBASE OTP (one-time extraction)")
    print("3. CONTINUOUS MONITORING (multiple attempts)")
    print()

    choice = input("Enter 1, 2, or 3: ").strip()

    print()
    print("=" * 60)
    print()

    if choice == "1":
        test_sms_system()

    elif choice == "2":
        extractor = CoinbaseOTPExtractor()
        code = extractor.get_coinbase_otp()

        if code:
            print("✅ SUCCESS! Use code above to complete withdrawal")
        else:
            print("❌ No code received. Try mode 3 for continuous monitoring")

    elif choice == "3":
        extractor = CoinbaseOTPExtractor()
        extractor.monitor_continuous()

    else:
        print("Invalid choice. Run script again and enter 1, 2, or 3")

    print()
    print("=" * 60)
    print()
