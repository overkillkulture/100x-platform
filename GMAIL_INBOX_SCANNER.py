"""
Quick inbox scan for emergencies and organization
"""

import imaplib
import email
from email.header import decode_header
from datetime import datetime, timedelta
from collections import Counter

def scan_inbox(email_address, app_password):
    """Scan inbox and categorize messages"""

    print(f"🔍 Scanning {email_address}...")

    # Connect
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(email_address, app_password)
    imap.select("INBOX")

    # Get last 7 days of emails
    cutoff = (datetime.now() - timedelta(days=7)).strftime("%d-%b-%Y")
    status, messages = imap.search(None, f'(SINCE {cutoff})')

    email_ids = messages[0].split()
    total = len(email_ids)

    print(f"📊 Found {total} emails in last 7 days\n")

    # Categories
    urgent_keywords = ['urgent', 'important', 'action required', 'payment', 'invoice', 'overdue']
    spam_keywords = ['sale', 'discount', 'offer', 'deal', 'promo', 'unsubscribe', 'marketing']

    urgent = []
    spam = []
    business = []
    other = []

    senders = []

    # Scan recent emails
    for i, email_id in enumerate(reversed(email_ids[-50:])):  # Last 50 emails
        status, msg_data = imap.fetch(email_id, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])

        # Get subject
        subject = decode_header(msg["Subject"])[0][0]
        if isinstance(subject, bytes):
            subject = subject.decode()

        # Get sender
        sender = msg.get("From", "")
        senders.append(sender)

        # Get date
        date = msg.get("Date", "")

        subject_lower = subject.lower()
        sender_lower = sender.lower()

        # Categorize
        if any(kw in subject_lower for kw in urgent_keywords):
            urgent.append({'from': sender, 'subject': subject, 'date': date})
        elif any(kw in subject_lower or kw in sender_lower for kw in spam_keywords):
            spam.append({'from': sender, 'subject': subject})
        elif 'stripe' in sender_lower or 'twilio' in sender_lower or 'grasshopper' in sender_lower:
            business.append({'from': sender, 'subject': subject, 'date': date})
        else:
            other.append({'from': sender, 'subject': subject})

    imap.close()
    imap.logout()

    # Report
    print("=" * 60)
    print("🚨 URGENT / IMPORTANT")
    print("=" * 60)
    if urgent:
        for msg in urgent[:10]:
            print(f"From: {msg['from'][:50]}")
            print(f"Subject: {msg['subject'][:70]}")
            print(f"Date: {msg['date']}")
            print()
    else:
        print("✅ No urgent emails!\n")

    print("=" * 60)
    print("💼 BUSINESS (Stripe, Twilio, etc.)")
    print("=" * 60)
    if business:
        for msg in business[:10]:
            print(f"From: {msg['from'][:50]}")
            print(f"Subject: {msg['subject'][:70]}")
            print()
    else:
        print("No business emails\n")

    print("=" * 60)
    print("🗑️ SPAM / SALES (Top offenders)")
    print("=" * 60)
    spam_senders = Counter([msg['from'] for msg in spam])
    for sender, count in spam_senders.most_common(10):
        print(f"{count}x - {sender[:60]}")

    print(f"\n💡 Total spam: {len(spam)} emails")
    print(f"📧 Other: {len(other)} emails")

    return {
        'urgent': urgent,
        'spam': spam,
        'business': business,
        'spam_senders': spam_senders
    }

if __name__ == "__main__":
    result = scan_inbox('overkillkulture@gmail.com', 'aycdcdcmnbfsrkvw')
