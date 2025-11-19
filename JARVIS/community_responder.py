"""
JARVIS Community Response Automation
For: Josh (Community Builder - Node #2)
Purpose: Monitor inbox, draft responses, schedule calls

Dependencies:
- playwright (browser automation)
- anthropic (Claude AI for drafting)
- python-dotenv (environment variables)
- pyautogui (fallback automation)
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
import anthropic

# Load environment variables
load_dotenv()

class CommunityResponder:
    def __init__(self):
        self.claude_api_key = os.getenv('ANTHROPIC_API_KEY')
        self.gmail_email = os.getenv('GMAIL_EMAIL', '')
        self.gmail_password = os.getenv('GMAIL_PASSWORD', '')
        self.calendly_url = os.getenv('CALENDLY_URL', 'https://calendly.com/yourusername')

        # Initialize Claude client
        if self.claude_api_key:
            self.claude = anthropic.Anthropic(api_key=self.claude_api_key)
        else:
            print("⚠️  No ANTHROPIC_API_KEY found - AI drafting disabled")
            self.claude = None

        # Create data directory
        self.data_dir = Path("C:/Users/dwrek/100X_DEPLOYMENT/JARVIS/data")
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Response templates
        self.templates = self.load_templates()

    def load_templates(self):
        """Load email response templates"""
        return {
            'welcome': {
                'subject_keywords': ['join', 'signup', 'get started', 'new builder'],
                'tone': 'welcoming and enthusiastic',
                'include': ['platform overview', 'next steps', 'onboarding call offer']
            },
            'support': {
                'subject_keywords': ['help', 'issue', 'problem', 'error', 'bug'],
                'tone': 'helpful and solution-focused',
                'include': ['acknowledgment', 'troubleshooting steps', 'follow-up offer']
            },
            'question': {
                'subject_keywords': ['how', 'what', 'when', 'where', 'why'],
                'tone': 'informative and friendly',
                'include': ['direct answer', 'additional resources', 'community links']
            },
            'feedback': {
                'subject_keywords': ['feedback', 'suggestion', 'idea', 'feature'],
                'tone': 'appreciative and engaged',
                'include': ['thanks', 'consideration acknowledgment', 'roadmap mention']
            }
        }

    def check_new_builder_emails(self, max_results=10):
        """
        Check Gmail for new builder applications
        Returns: List of email objects with subject, sender, content
        """
        print("🔍 Checking Gmail for new builder inquiries...")

        emails = []

        try:
            with sync_playwright() as p:
                # Launch browser
                browser = p.chromium.launch(headless=False)
                context = browser.new_context()
                page = context.new_page()

                # Navigate to Gmail
                print("📧 Opening Gmail...")
                page.goto('https://mail.google.com')
                page.wait_for_load_state('networkidle')

                # Check if already logged in
                if 'inbox' not in page.url:
                    print("🔐 Login required - please log in manually...")
                    print("⏳ Waiting 60 seconds for manual login...")
                    time.sleep(60)

                # Wait for inbox to load
                page.wait_for_selector('[role="main"]', timeout=30000)
                print("✅ Inbox loaded!")

                # Get unread emails (simplified selector)
                try:
                    # Click on inbox
                    page.click('a[href*="inbox"]')
                    time.sleep(2)

                    # Get email rows
                    email_rows = page.query_selector_all('tr.zA')[:max_results]

                    print(f"📬 Found {len(email_rows)} recent emails")

                    for idx, row in enumerate(email_rows):
                        try:
                            # Extract email data
                            sender = row.query_selector('.yW span')
                            subject = row.query_selector('.y6 span')

                            if sender and subject:
                                email_data = {
                                    'id': f"email_{idx}_{int(time.time())}",
                                    'sender': sender.inner_text(),
                                    'subject': subject.inner_text(),
                                    'timestamp': datetime.now().isoformat(),
                                    'preview': row.query_selector('.y2')?.inner_text() or ''
                                }

                                emails.append(email_data)
                                print(f"  📨 {email_data['sender']}: {email_data['subject']}")

                        except Exception as e:
                            print(f"  ⚠️  Error extracting email {idx}: {e}")
                            continue

                except Exception as e:
                    print(f"⚠️  Error scanning inbox: {e}")

                # Close browser
                browser.close()

        except Exception as e:
            print(f"❌ Error checking emails: {e}")
            print("💡 Tip: Make sure you're logged into Gmail in your default browser")

        # Save results
        self.save_emails(emails)
        return emails

    def classify_email_type(self, subject, preview):
        """Classify email type based on subject and preview"""
        combined_text = f"{subject} {preview}".lower()

        # Check against template keywords
        for email_type, template in self.templates.items():
            for keyword in template['subject_keywords']:
                if keyword.lower() in combined_text:
                    return email_type

        return 'question'  # Default type

    def draft_welcome_email(self, builder_name, builder_email, original_message=''):
        """
        Use Claude to draft personalized welcome email
        """
        if not self.claude:
            return self._fallback_welcome_template(builder_name)

        print(f"✍️  Drafting personalized welcome email for {builder_name}...")

        prompt = f"""You are Josh, the Community Builder for the 100X Platform - a consciousness revolution platform that helps builders create amazing projects with AI assistance.

A new builder named {builder_name} just reached out. Here's their message:
{original_message or 'They expressed interest in joining the platform.'}

Draft a warm, enthusiastic welcome email that:
1. Thanks them for their interest
2. Gives a brief exciting overview of the 100X Platform (AI-powered building tools, community support, JARVIS automation)
3. Outlines the next steps (create account, onboarding call, join Discord)
4. Offers to schedule a personal onboarding call
5. Includes the Calendly link: {self.calendly_url}
6. Ends with enthusiasm and your signature

Keep it friendly, concise (250-300 words), and authentic. Make them excited to join!

Write only the email body, no subject line."""

        try:
            message = self.claude.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )

            draft = message.content[0].text
            print("✅ Draft complete!")

            # Save draft
            self.save_draft(builder_email, 'welcome', draft)

            return draft

        except Exception as e:
            print(f"⚠️  Claude API error: {e}")
            return self._fallback_welcome_template(builder_name)

    def draft_response(self, email_data):
        """
        Draft appropriate response based on email type
        """
        email_type = self.classify_email_type(email_data['subject'], email_data.get('preview', ''))
        sender_name = email_data['sender'].split()[0]  # First name

        print(f"📝 Drafting {email_type} response for {sender_name}...")

        if email_type == 'welcome':
            return self.draft_welcome_email(sender_name, email_data['sender'], email_data.get('preview', ''))

        # Generic AI-drafted response for other types
        if not self.claude:
            return self._fallback_generic_template(email_type, sender_name)

        template = self.templates[email_type]

        prompt = f"""You are Josh, Community Builder for the 100X Platform.

You received this email:
From: {email_data['sender']}
Subject: {email_data['subject']}
Preview: {email_data.get('preview', '')}

Draft a {template['tone']} response that includes:
{', '.join(template['include'])}

Keep it concise (150-200 words), helpful, and authentic.
Write only the email body, no subject line."""

        try:
            message = self.claude.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )

            draft = message.content[0].text

            # Save draft
            self.save_draft(email_data['sender'], email_type, draft)

            return draft

        except Exception as e:
            print(f"⚠️  Error drafting response: {e}")
            return self._fallback_generic_template(email_type, sender_name)

    def _fallback_welcome_template(self, builder_name):
        """Fallback template when Claude API unavailable"""
        return f"""Hey {builder_name}!

Thanks so much for your interest in the 100X Platform! 🚀

We're building something really special here - a platform where builders get AI-powered automation tools, an amazing supportive community, and the ability to create incredible projects faster than ever before.

Here's what's next:
1. Create your account on the platform
2. Join our Discord community
3. Let's schedule a quick onboarding call so I can get you set up with everything

You can grab a time on my calendar here: {self.calendly_url}

Really excited to have you join us! This community is full of incredible builders and we're all here to help each other succeed.

Looking forward to connecting!

Josh
Community Builder, 100X Platform"""

    def _fallback_generic_template(self, email_type, sender_name):
        """Generic fallback template"""
        return f"""Hey {sender_name},

Thanks for reaching out! I'm looking into your {email_type} and will get back to you with a detailed response shortly.

In the meantime, feel free to check out our platform documentation or join our Discord community if you haven't already.

Talk soon!

Josh
Community Builder, 100X Platform"""

    def schedule_onboarding_call(self, builder_email):
        """
        Open Calendly and prepare invite
        """
        print(f"📅 Preparing onboarding call invite for {builder_email}...")

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=False)
                page = browser.new_page()

                # Open Calendly
                page.goto(self.calendly_url)
                page.wait_for_load_state('networkidle')

                print(f"✅ Calendly opened! Copy this email: {builder_email}")
                print("⏳ Keeping browser open for 60 seconds...")
                time.sleep(60)

                browser.close()

        except Exception as e:
            print(f"⚠️  Error opening Calendly: {e}")
            print(f"💡 Manual fallback: Open {self.calendly_url} and invite {builder_email}")

    def save_emails(self, emails):
        """Save emails to JSON file"""
        file_path = self.data_dir / f"emails_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(file_path, 'w') as f:
            json.dump(emails, f, indent=2)
        print(f"💾 Saved {len(emails)} emails to {file_path}")

    def save_draft(self, recipient, email_type, content):
        """Save draft to file"""
        drafts_dir = self.data_dir / "drafts"
        drafts_dir.mkdir(exist_ok=True)

        file_path = drafts_dir / f"draft_{email_type}_{int(time.time())}.txt"
        with open(file_path, 'w') as f:
            f.write(f"To: {recipient}\n")
            f.write(f"Type: {email_type}\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n")
            f.write("-" * 50 + "\n\n")
            f.write(content)

        print(f"💾 Draft saved to {file_path}")

    def generate_morning_briefing(self, emails):
        """Generate summary of overnight activity"""
        print("\n" + "="*50)
        print("☀️  MORNING COMMUNITY BRIEFING")
        print("="*50)

        print(f"\n📬 Total Emails: {len(emails)}")

        # Categorize emails
        by_type = {}
        for email in emails:
            email_type = self.classify_email_type(email['subject'], email.get('preview', ''))
            by_type[email_type] = by_type.get(email_type, 0) + 1

        print("\n📊 By Type:")
        for email_type, count in by_type.items():
            print(f"  {email_type.title()}: {count}")

        print("\n🔥 Top 3 Priority:")
        for i, email in enumerate(emails[:3], 1):
            print(f"  {i}. {email['sender']}: {email['subject']}")

        print("\n" + "="*50)
        print("💡 Suggested Actions:")
        print("  1. Draft responses for top 3 inquiries")
        print("  2. Check Discord for urgent questions")
        print("  3. Schedule any pending onboarding calls")
        print("="*50 + "\n")


def main():
    """Main CLI interface"""
    import argparse

    parser = argparse.ArgumentParser(description='JARVIS Community Response Automation')
    parser.add_argument('--check-inbox', action='store_true', help='Check Gmail for new emails')
    parser.add_argument('--draft-welcome', nargs=2, metavar=('NAME', 'EMAIL'), help='Draft welcome email')
    parser.add_argument('--draft-response', type=int, metavar='EMAIL_ID', help='Draft response for specific email')
    parser.add_argument('--schedule-call', metavar='EMAIL', help='Schedule onboarding call')
    parser.add_argument('--morning-briefing', action='store_true', help='Generate morning briefing')

    args = parser.parse_args()

    responder = CommunityResponder()

    if args.check_inbox:
        emails = responder.check_new_builder_emails()
        if emails:
            print(f"\n✅ Found {len(emails)} emails!")
            print("💡 Use --draft-response <email_id> to draft a response")

    elif args.draft_welcome:
        name, email = args.draft_welcome
        draft = responder.draft_welcome_email(name, email)
        print("\n" + "="*50)
        print("DRAFT:")
        print("="*50)
        print(draft)
        print("="*50)

    elif args.schedule_call:
        responder.schedule_onboarding_call(args.schedule_call)

    elif args.morning_briefing:
        # Load most recent emails
        email_files = sorted(responder.data_dir.glob('emails_*.json'))
        if email_files:
            with open(email_files[-1]) as f:
                emails = json.load(f)
            responder.generate_morning_briefing(emails)
        else:
            print("⚠️  No emails found. Run --check-inbox first.")

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
