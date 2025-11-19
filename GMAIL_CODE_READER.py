#!/usr/bin/env python3
"""
GMAIL VERIFICATION CODE READER
Automatically extracts verification codes from Gmail

SOLVES: The authentication war
NO API KEYS NEEDED: Uses Gmail's IMAP (built-in)

USAGE:
    python GMAIL_CODE_READER.py
"""

import imaplib
import email
from email.header import decode_header
import re
from datetime import datetime, timedelta

class GmailCodeReader:
    def __init__(self, email_address, password):
        """
        Initialize Gmail connection

        Args:
            email_address: Your Gmail address
            password: App password (NOT your regular Gmail password)
        """
        self.email_address = email_address
        self.password = password
        self.imap = None

    def connect(self):
        """Connect to Gmail via IMAP"""
        try:
            print("🔐 Connecting to Gmail...")
            self.imap = imaplib.IMAP4_SSL("imap.gmail.com")
            self.imap.login(self.email_address, self.password)
            print("✅ Connected to Gmail")
            return True
        except Exception as e:
            print(f"❌ Failed to connect: {e}")
            print("\n⚠️  If you see 'authentication failed', you need to:")
            print("1. Enable 2-step verification in Gmail")
            print("2. Generate an App Password")
            print("3. Use that App Password here (not your regular password)")
            print("\nSee: GMAIL_APP_PASSWORD_SETUP.md for instructions")
            return False

    def get_latest_verification_code(self, service_name=None, minutes_back=5):
        """
        Get the most recent verification code from Gmail

        Args:
            service_name: Optional - filter by service (e.g., "Microsoft")
            minutes_back: How far back to search (default: 5 minutes)

        Returns:
            The verification code as a string, or None if not found
        """
        if not self.imap:
            if not self.connect():
                return None

        try:
            # Select inbox
            self.imap.select("INBOX")

            # Search for recent emails
            cutoff_time = datetime.now() - timedelta(minutes=minutes_back)
            date_str = cutoff_time.strftime("%d-%b-%Y")

            # Search for emails with common verification keywords
            search_terms = [
                'verification',
                'code',
                'verify',
                'authenticate',
                'security code',
                'confirmation code'
            ]

            all_codes = []

            for term in search_terms:
                # Search for emails containing this term, received today
                status, messages = self.imap.search(None, f'(SINCE {date_str} SUBJECT "{term}")')

                if status != "OK":
                    continue

                # Get list of email IDs
                email_ids = messages[0].split()

                # Process most recent emails first
                for email_id in reversed(email_ids[-10:]):  # Last 10 emails
                    # Fetch the email
                    status, msg_data = self.imap.fetch(email_id, "(RFC822)")

                    if status != "OK":
                        continue

                    # Parse email
                    msg = email.message_from_bytes(msg_data[0][1])

                    # Get subject
                    subject = decode_header(msg["Subject"])[0][0]
                    if isinstance(subject, bytes):
                        subject = subject.decode()

                    # Get sender
                    sender = msg.get("From", "")

                    # Filter by service name if specified
                    if service_name:
                        if service_name.lower() not in subject.lower() and \
                           service_name.lower() not in sender.lower():
                            continue

                    # Get email body
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode()
                                break
                    else:
                        body = msg.get_payload(decode=True).decode()

                    # Search for verification codes in body
                    # Common patterns:
                    # - 6 digits: 123456
                    # - 6 digits with spaces: 123 456
                    # - 6 digits with dashes: 123-456
                    # - 8 alphanumeric: ABC12345

                    patterns = [
                        r'\b(\d{6})\b',  # 6 digits
                        r'\b(\d{3}[\s-]?\d{3})\b',  # 6 digits with separator
                        r'\b([A-Z0-9]{6,8})\b',  # 6-8 alphanumeric
                        r'code[:\s]+(\d{6})',  # "code: 123456"
                        r'verify[:\s]+(\d{6})',  # "verify: 123456"
                    ]

                    for pattern in patterns:
                        matches = re.findall(pattern, body, re.IGNORECASE)
                        for match in matches:
                            # Clean up match (remove spaces/dashes)
                            code = re.sub(r'[\s-]', '', match)

                            # Verify it's numeric or alphanumeric
                            if code and (code.isdigit() or code.isalnum()):
                                all_codes.append({
                                    'code': code,
                                    'subject': subject,
                                    'sender': sender,
                                    'time': msg.get("Date", "")
                                })

            # Return most recent code
            if all_codes:
                latest = all_codes[0]
                print(f"\n✅ Found verification code!")
                print(f"   Code: {latest['code']}")
                print(f"   From: {latest['sender']}")
                print(f"   Subject: {latest['subject']}")
                return latest['code']
            else:
                print(f"\n❌ No verification codes found in last {minutes_back} minutes")
                return None

        except Exception as e:
            print(f"❌ Error reading emails: {e}")
            return None

    def disconnect(self):
        """Close connection"""
        if self.imap:
            try:
                self.imap.close()
                self.imap.logout()
            except:
                pass

def main():
    """Interactive test"""
    print("="*60)
    print("GMAIL VERIFICATION CODE READER")
    print("="*60)
    print()

    # Get credentials
    email_address = input("Gmail address: ").strip()

    print("\n⚠️  IMPORTANT: Use an App Password, not your regular password!")
    print("If you haven't created one yet, see: GMAIL_APP_PASSWORD_SETUP.md")
    password = input("App Password: ").strip()

    # Create reader
    reader = GmailCodeReader(email_address, password)

    # Get code
    print("\n🔍 Searching for verification codes...")
    code = reader.get_latest_verification_code(minutes_back=10)

    if code:
        print(f"\n🎯 Your verification code: {code}")
    else:
        print("\n❌ No codes found. Try:")
        print("   • Requesting a new verification code")
        print("   • Checking your email manually to verify it arrived")
        print("   • Running this script again")

    reader.disconnect()

if __name__ == "__main__":
    main()
