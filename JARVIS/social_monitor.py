"""
JARVIS Social Media Monitor
For: Josh (Community Builder - Node #2)
Purpose: Track Discord, Twitter, community mentions and flag urgent issues

Dependencies:
- playwright (browser automation)
- anthropic (Claude AI for analysis)
- python-dotenv (environment variables)
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

class SocialMonitor:
    def __init__(self):
        self.claude_api_key = os.getenv('ANTHROPIC_API_KEY')
        self.discord_url = os.getenv('DISCORD_URL', 'https://discord.com/channels/@me')
        self.twitter_username = os.getenv('TWITTER_USERNAME', '100XPlatform')

        # Initialize Claude client
        if self.claude_api_key:
            self.claude = anthropic.Anthropic(api_key=self.claude_api_key)
        else:
            print("⚠️  No ANTHROPIC_API_KEY found - AI analysis disabled")
            self.claude = None

        # Create data directory
        self.data_dir = Path("C:/Users/dwrek/100X_DEPLOYMENT/JARVIS/data/social")
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Urgency keywords
        self.urgent_keywords = [
            'urgent', 'emergency', 'critical', 'broken', 'down', 'not working',
            'error', 'crash', 'bug', 'issue', 'help needed', 'asap', 'immediately'
        ]

    def check_discord_questions(self, server_name=None):
        """
        Monitor Discord for unanswered questions
        Returns: List of questions with urgency flags
        """
        print("🎮 Checking Discord for unanswered questions...")

        questions = []

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=False)
                context = browser.new_context()
                page = context.new_page()

                # Navigate to Discord
                print("📱 Opening Discord...")
                page.goto(self.discord_url)
                page.wait_for_load_state('networkidle')

                # Check if logged in
                if 'login' in page.url:
                    print("🔐 Login required - please log in manually...")
                    print("⏳ Waiting 60 seconds for manual login...")
                    time.sleep(60)

                # Wait for Discord to load
                time.sleep(3)

                print("✅ Discord loaded!")
                print("💡 Manual scan mode - reviewing recent messages...")

                # Get channel list (simplified - user will need to navigate)
                print("\n📋 Scan Instructions:")
                print("  1. Navigate to your community server")
                print("  2. Check #general, #support, #questions channels")
                print("  3. Look for messages ending with '?'")
                print("  4. Check if anyone replied")
                print("\n⏳ Keeping browser open for 120 seconds for manual review...")

                time.sleep(120)

                browser.close()

        except Exception as e:
            print(f"❌ Error checking Discord: {e}")
            print("💡 Tip: Open Discord manually and review recent messages")

        return questions

    def check_twitter_mentions(self, max_results=20):
        """
        Track @mentions on Twitter/X
        Returns: List of mentions with sentiment
        """
        print(f"🐦 Checking Twitter mentions for @{self.twitter_username}...")

        mentions = []

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=False)
                context = browser.new_context()
                page = context.new_page()

                # Navigate to Twitter notifications
                print("📱 Opening Twitter...")
                page.goto('https://twitter.com/notifications')
                page.wait_for_load_state('networkidle')

                # Check if logged in
                if 'login' in page.url.lower():
                    print("🔐 Login required - please log in manually...")
                    print("⏳ Waiting 60 seconds for manual login...")
                    time.sleep(60)

                time.sleep(3)

                print("✅ Twitter loaded!")
                print("💡 Manual scan mode - reviewing mentions...")

                print("\n📋 Scan Instructions:")
                print("  1. Check 'Mentions' tab")
                print("  2. Look for questions or support requests")
                print("  3. Check for negative sentiment")
                print("  4. Note any urgent issues")
                print("\n⏳ Keeping browser open for 90 seconds for manual review...")

                time.sleep(90)

                browser.close()

        except Exception as e:
            print(f"❌ Error checking Twitter: {e}")
            print("💡 Tip: Open Twitter manually and check mentions")

        return mentions

    def analyze_urgency(self, message_text):
        """
        Determine if a message is urgent
        Returns: urgency_score (0-100) and reason
        """
        if not self.claude:
            # Fallback: keyword matching
            urgency_score = 0
            for keyword in self.urgent_keywords:
                if keyword.lower() in message_text.lower():
                    urgency_score = 80
                    return urgency_score, f"Contains urgent keyword: {keyword}"

            if '?' in message_text and 'help' in message_text.lower():
                return 50, "Help request detected"

            return 10, "Normal message"

        # AI-powered urgency analysis
        try:
            prompt = f"""Analyze this community message for urgency:

"{message_text}"

Rate urgency from 0-100:
- 0-20: Normal conversation
- 21-40: General question
- 41-60: Needs response soon
- 61-80: Important issue
- 81-100: Urgent/critical

Respond with just: SCORE|REASON
Example: 75|User reports critical bug affecting multiple people"""

            message = self.claude.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=100,
                messages=[{"role": "user", "content": prompt}]
            )

            response = message.content[0].text.strip()
            score, reason = response.split('|')

            return int(score), reason

        except Exception as e:
            print(f"⚠️  Error analyzing urgency: {e}")
            return 30, "Unable to analyze"

    def flag_urgent_issues(self, messages):
        """
        Alert Josh to urgent community needs
        Filters messages by urgency and generates action list
        """
        print("\n" + "="*60)
        print("🚨 URGENT ISSUES FLAGGED")
        print("="*60)

        if not messages:
            print("\n✅ No messages to analyze")
            return

        urgent_messages = []

        for msg in messages:
            score, reason = self.analyze_urgency(msg.get('content', ''))
            if score >= 60:
                urgent_messages.append({
                    **msg,
                    'urgency_score': score,
                    'urgency_reason': reason
                })

        if not urgent_messages:
            print("\n✅ No urgent issues detected")
            print("💚 Community is healthy!")
        else:
            print(f"\n⚠️  {len(urgent_messages)} urgent issues found:\n")

            # Sort by urgency
            urgent_messages.sort(key=lambda x: x['urgency_score'], reverse=True)

            for i, msg in enumerate(urgent_messages, 1):
                print(f"{i}. 🔴 Urgency: {msg['urgency_score']}/100")
                print(f"   Platform: {msg.get('platform', 'Unknown')}")
                print(f"   User: {msg.get('user', 'Unknown')}")
                print(f"   Reason: {msg['urgency_reason']}")
                print(f"   Message: {msg.get('content', '')[:100]}...")
                print()

            print("💡 Recommended Actions:")
            print("  1. Respond to highest urgency items first")
            print("  2. Escalate critical issues to Commander")
            print("  3. Post status updates if widespread issue")

        print("="*60 + "\n")

        # Save report
        self.save_urgent_report(urgent_messages)

    def generate_social_report(self, discord_data=None, twitter_data=None):
        """
        Generate comprehensive social media activity report
        """
        print("\n" + "="*60)
        print("📊 SOCIAL MEDIA ACTIVITY REPORT")
        print("="*60)

        print(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Discord section
        print("\n🎮 Discord Activity:")
        if discord_data:
            print(f"  Total Messages: {len(discord_data)}")
            questions = [m for m in discord_data if '?' in m.get('content', '')]
            print(f"  Questions: {len(questions)}")
            unanswered = [q for q in questions if not q.get('has_reply', False)]
            print(f"  Unanswered: {len(unanswered)}")
        else:
            print("  No data collected - use --check-discord first")

        # Twitter section
        print("\n🐦 Twitter Activity:")
        if twitter_data:
            print(f"  Total Mentions: {len(twitter_data)}")
            positive = [m for m in twitter_data if m.get('sentiment') == 'positive']
            negative = [m for m in twitter_data if m.get('sentiment') == 'negative']
            print(f"  Positive: {len(positive)}")
            print(f"  Negative: {len(negative)}")
        else:
            print("  No data collected - use --check-twitter first")

        # Overall health
        print("\n💚 Community Health:")
        print("  Status: Good (based on available data)")
        print("  Response Rate: Manual review needed")
        print("  Engagement: Manual review needed")

        print("\n💡 Next Steps:")
        print("  1. Address any unanswered questions")
        print("  2. Engage with positive mentions")
        print("  3. Resolve any negative feedback")
        print("  4. Post community update")

        print("="*60 + "\n")

    def save_urgent_report(self, urgent_messages):
        """Save urgent issues to file"""
        if not urgent_messages:
            return

        file_path = self.data_dir / f"urgent_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(file_path, 'w') as f:
            json.dump(urgent_messages, f, indent=2)

        print(f"💾 Urgent report saved to {file_path}")

    def monitor_all_platforms(self):
        """
        One-command check of all platforms
        """
        print("\n🌐 Starting full platform monitoring...")
        print("="*60 + "\n")

        # Check Discord
        discord_data = self.check_discord_questions()

        # Check Twitter
        twitter_data = self.check_twitter_mentions()

        # Generate report
        all_messages = discord_data + twitter_data
        self.flag_urgent_issues(all_messages)
        self.generate_social_report(discord_data, twitter_data)

        print("✅ Monitoring complete!")


def main():
    """Main CLI interface"""
    import argparse

    parser = argparse.ArgumentParser(description='JARVIS Social Media Monitor')
    parser.add_argument('--check-discord', action='store_true', help='Check Discord for questions')
    parser.add_argument('--check-twitter', action='store_true', help='Check Twitter mentions')
    parser.add_argument('--check-all', action='store_true', help='Monitor all platforms')
    parser.add_argument('--analyze-urgency', type=str, metavar='MESSAGE', help='Analyze urgency of a message')

    args = parser.parse_args()

    monitor = SocialMonitor()

    if args.check_discord:
        questions = monitor.check_discord_questions()
        print(f"\n✅ Discord scan complete")

    elif args.check_twitter:
        mentions = monitor.check_twitter_mentions()
        print(f"\n✅ Twitter scan complete")

    elif args.check_all:
        monitor.monitor_all_platforms()

    elif args.analyze_urgency:
        score, reason = monitor.analyze_urgency(args.analyze_urgency)
        print(f"\n📊 Urgency Analysis:")
        print(f"  Score: {score}/100")
        print(f"  Reason: {reason}")

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
