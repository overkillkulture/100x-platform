"""
SMS CODE READER - Twilio API Integration
Automatically reads SMS verification codes from your ported number

DOMINO #2: SMS Automation
Once 509-216-6552 ports to Twilio, this script auto-reads 2FA codes

Status: READY - Will activate when port completes (5-11 days)
"""

import requests
from datetime import datetime, timedelta
import re
import json
from pathlib import Path

class TwilioSMSReader:
    def __init__(self):
        """Initialize with Twilio credentials"""
        self.account_sid = "AC379092b0f6d446532a78fac08cfc72c"
        self.auth_token = "hqOEVtUSDE58HyTShtMzyIhx5VNDFacj"
        self.phone_number = "+15092166552"

        # API endpoint for reading messages
        self.api_url = f"https://api.twilio.com/2010-04-01/Accounts/{self.account_sid}/Messages.json"

    def get_recent_messages(self, minutes_back=5):
        """Get all SMS messages received in last N minutes"""

        # Calculate cutoff time
        cutoff_time = datetime.now() - timedelta(minutes=minutes_back)

        # Query Twilio API
        params = {
            'To': self.phone_number,
            'DateSent>': cutoff_time.strftime('%Y-%m-%d'),
            'PageSize': 20
        }

        response = requests.get(
            self.api_url,
            auth=(self.account_sid, self.auth_token),
            params=params
        )

        if response.status_code == 200:
            messages = response.json()['messages']

            # Filter to only recent messages
            recent = [
                msg for msg in messages
                if datetime.fromisoformat(msg['date_sent'].replace('Z', '+00:00')) > cutoff_time
            ]

            return recent
        else:
            print(f"Error fetching messages: {response.status_code}")
            return []

    def extract_verification_code(self, message_body):
        """Extract verification code from message text"""

        # Common patterns for verification codes
        patterns = [
            r'\b(\d{6})\b',                    # 6 digits
            r'\b(\d{4})\b',                    # 4 digits
            r'code[:\s]+(\d{4,6})',            # "code: 123456"
            r'verification[:\s]+(\d{4,6})',    # "verification: 123456"
            r'is[:\s]+(\d{4,6})',              # "is: 123456"
            r'(\d{3}-\d{3})',                  # "123-456"
        ]

        for pattern in patterns:
            match = re.search(pattern, message_body, re.IGNORECASE)
            if match:
                return match.group(1).replace('-', '')

        return None

    def get_latest_code(self, service_name=None, minutes_back=5):
        """
        Get the most recent verification code

        Args:
            service_name: Optional - filter by service (e.g., "Microsoft", "Stripe")
            minutes_back: How far back to search (default 5 minutes)

        Returns:
            code (string) or None
        """

        messages = self.get_recent_messages(minutes_back)

        if not messages:
            print("No recent SMS messages found")
            return None

        # If service name provided, filter messages
        if service_name:
            messages = [
                msg for msg in messages
                if service_name.lower() in msg['body'].lower()
            ]

        # Get most recent message
        if messages:
            latest = messages[0]
            code = self.extract_verification_code(latest['body'])

            if code:
                print(f"✅ Found code: {code}")
                print(f"From: {latest['from']}")
                print(f"Message: {latest['body'][:100]}...")
                return code
            else:
                print(f"No code found in message: {latest['body']}")
                return None
        else:
            print(f"No messages from {service_name} found")
            return None

    def monitor_codes(self, callback=None):
        """
        Continuously monitor for new verification codes

        Args:
            callback: Function to call when code is received
        """

        import time

        print(f"📱 Monitoring SMS to {self.phone_number}...")
        print("Press Ctrl+C to stop")

        seen_messages = set()

        try:
            while True:
                messages = self.get_recent_messages(minutes_back=1)

                for msg in messages:
                    msg_id = msg['sid']

                    if msg_id not in seen_messages:
                        seen_messages.add(msg_id)

                        code = self.extract_verification_code(msg['body'])

                        if code:
                            print(f"\n🔔 NEW CODE: {code}")
                            print(f"From: {msg['from']}")
                            print(f"Message: {msg['body'][:100]}...")

                            if callback:
                                callback(code, msg)

                time.sleep(10)  # Check every 10 seconds

        except KeyboardInterrupt:
            print("\n\n✅ Monitoring stopped")


# ============================================
# USAGE EXAMPLES
# ============================================

def example_basic_usage():
    """Get latest verification code"""

    reader = TwilioSMSReader()

    # Get any recent code
    code = reader.get_latest_code()

    if code:
        print(f"Use this code: {code}")
    else:
        print("No verification code found")


def example_service_specific():
    """Get code from specific service"""

    reader = TwilioSMSReader()

    # Get code from Microsoft
    code = reader.get_latest_code(service_name="Microsoft")

    # Or from Stripe
    code = reader.get_latest_code(service_name="Stripe")


def example_monitoring():
    """Monitor for codes in real-time"""

    def handle_code(code, message):
        """What to do when code is received"""
        print(f"AUTO-ENTERING CODE: {code}")
        # Could auto-fill into browser here

    reader = TwilioSMSReader()
    reader.monitor_codes(callback=handle_code)


# ============================================
# UNIVERSAL JAILBREAK INTEGRATION
# ============================================

def get_sms_verification_code(service_name=None):
    """
    Universal function for authentication jailbreak system
    Call this whenever you need an SMS code
    """

    reader = TwilioSMSReader()
    return reader.get_latest_code(service_name=service_name)


if __name__ == "__main__":
    print("SMS CODE READER")
    print("=" * 50)
    print()
    print("STATUS: Waiting for number port to complete")
    print("Number: 509-216-6552")
    print("Port ETA: 5-11 days from Oct 6, 2025")
    print()
    print("This script will activate automatically when port completes!")
    print()
    print("=" * 50)

    # Uncomment to test (will work after port completes):
    # example_basic_usage()
