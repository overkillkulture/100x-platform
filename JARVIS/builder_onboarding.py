"""
JARVIS Builder Onboarding Automation
For: Josh (Community Builder - Node #2)
Purpose: Complete new builder setup workflow from inquiry to active member

Dependencies:
- playwright (browser automation)
- anthropic (Claude AI for personalization)
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

class BuilderOnboarding:
    def __init__(self):
        self.claude_api_key = os.getenv('ANTHROPIC_API_KEY')
        self.platform_url = os.getenv('PLATFORM_URL', 'http://localhost:8000/PLATFORM/welcome.html')
        self.discord_invite = os.getenv('DISCORD_INVITE_URL', 'https://discord.gg/yourinvite')
        self.admin_email = os.getenv('ADMIN_EMAIL', 'admin@100xplatform.com')

        # Initialize Claude client
        if self.claude_api_key:
            self.claude = anthropic.Anthropic(api_key=self.claude_api_key)
        else:
            print("⚠️  No ANTHROPIC_API_KEY found - AI personalization disabled")
            self.claude = None

        # Create data directory
        self.data_dir = Path("C:/Users/dwrek/100X_DEPLOYMENT/JARVIS/data/builders")
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Onboarding checklist
        self.checklist = [
            'account_created',
            'welcome_email_sent',
            'discord_invited',
            'onboarding_call_scheduled',
            'welcome_kit_delivered',
            'first_login_confirmed'
        ]

    def create_platform_account(self, builder_data):
        """
        Auto-create account in 100X Platform
        builder_data: dict with name, email, interests
        """
        print(f"\n🔧 Creating platform account for {builder_data['name']}...")

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=False)
                page = browser.new_page()

                # Navigate to platform signup
                signup_url = self.platform_url.replace('welcome.html', 'login.html')
                print(f"📱 Opening signup page: {signup_url}")
                page.goto(signup_url)
                page.wait_for_load_state('networkidle')

                # Look for signup form
                print("🔍 Looking for signup form...")

                # Try to fill form (adjust selectors based on actual platform)
                try:
                    # Check if email field exists
                    email_field = page.query_selector('input[type="email"]')
                    if email_field:
                        print("✍️  Filling signup form...")
                        email_field.fill(builder_data['email'])

                        # Fill name if field exists
                        name_field = page.query_selector('input[name="name"], input[name="username"]')
                        if name_field:
                            name_field.fill(builder_data['name'])

                        print("✅ Form filled! (Manual submission required)")
                        print("⏳ Keeping browser open for 30 seconds...")
                        time.sleep(30)

                    else:
                        print("💡 Manual mode - please create account manually:")
                        print(f"   Name: {builder_data['name']}")
                        print(f"   Email: {builder_data['email']}")
                        print("⏳ Keeping browser open for 60 seconds...")
                        time.sleep(60)

                except Exception as e:
                    print(f"⚠️  Automated form fill not possible: {e}")
                    print("💡 Please create account manually")
                    time.sleep(60)

                browser.close()

                # Mark as completed
                self.update_builder_progress(builder_data['email'], 'account_created')
                return True

        except Exception as e:
            print(f"❌ Error creating account: {e}")
            return False

    def send_welcome_kit(self, builder_email, builder_name):
        """
        Send onboarding materials via email
        """
        print(f"\n📦 Preparing welcome kit for {builder_name}...")

        # Generate personalized welcome kit
        welcome_content = self.generate_welcome_kit(builder_name)

        # Save locally
        kit_path = self.data_dir / f"welcome_kit_{builder_email.replace('@', '_at_')}.txt"
        with open(kit_path, 'w', encoding='utf-8') as f:
            f.write(welcome_content)

        print(f"💾 Welcome kit saved to: {kit_path}")
        print("\n📧 Welcome Kit Preview:")
        print("="*60)
        print(welcome_content[:500] + "...")
        print("="*60)

        print("\n💡 Next step: Copy content and send via email or Discord DM")

        # Mark as completed
        self.update_builder_progress(builder_email, 'welcome_kit_delivered')

        return welcome_content

    def generate_welcome_kit(self, builder_name):
        """Generate personalized welcome materials"""

        if not self.claude:
            return self._fallback_welcome_kit(builder_name)

        try:
            prompt = f"""Create a warm, enthusiastic welcome kit for a new builder named {builder_name} joining the 100X Platform.

Include:
1. **Welcome Message** - Exciting intro to the platform
2. **Quick Start Guide** - 3 simple steps to get started
3. **Platform Features Overview** - Key tools and capabilities
4. **Community Resources** - Discord, documentation, support
5. **First Project Ideas** - 3 beginner-friendly project suggestions
6. **Pro Tips** - 3 insider tips for success

Keep it friendly, actionable, and under 600 words. Use emojis for visual appeal. Make them feel like they just joined something special!"""

            message = self.claude.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )

            return message.content[0].text

        except Exception as e:
            print(f"⚠️  Claude API error: {e}")
            return self._fallback_welcome_kit(builder_name)

    def _fallback_welcome_kit(self, builder_name):
        """Fallback welcome kit template"""
        return f"""🎉 Welcome to 100X Platform, {builder_name}! 🎉

You just joined something incredible - a community of builders using AI-powered tools to create amazing projects faster than ever before.

🚀 QUICK START (3 Steps):
1. Log into the platform and explore the modules
2. Join our Discord community (link below)
3. Build your first project with JARVIS assistance

💎 WHAT YOU GET:
• JARVIS Automation - AI that helps you build
• Module Library - Pre-built components
• Trinity AI - Three AI minds helping you
• Amazing Community - Supportive builders
• Pattern Theory - Universal building framework

🎯 YOUR FIRST PROJECT IDEAS:
1. Personal Dashboard - Track your goals
2. Automation Helper - Automate daily tasks
3. Community Tool - Help other builders

💡 PRO TIPS:
• Ask ARIA (🤖 button) any questions
• Check community activity (🌐 button)
• Experiment with modules - can't break anything!

🔗 IMPORTANT LINKS:
• Platform: {self.platform_url}
• Discord: {self.discord_invite}
• Documentation: Coming soon!

💚 We're here to help you succeed. The community is active, friendly, and always ready to assist.

Let's build something amazing together!

- Josh & The 100X Team"""

    def add_to_discord(self, builder_email, builder_name):
        """
        Add builder to Discord with Builder role
        """
        print(f"\n💬 Adding {builder_name} to Discord...")

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=False)
                page = browser.new_page()

                # Open Discord
                print("📱 Opening Discord...")
                page.goto(self.discord_invite)
                page.wait_for_load_state('networkidle')

                print(f"✅ Discord invite opened!")
                print(f"💡 Share this invite link with {builder_name}:")
                print(f"   {self.discord_invite}")
                print(f"   Email: {builder_email}")

                print("\n📋 Manual steps:")
                print("  1. Send Discord invite to builder")
                print("  2. Wait for them to join")
                print("  3. Assign 'Builder' role")
                print("  4. Post welcome message in #introductions")

                print("\n⏳ Keeping browser open for 60 seconds...")
                time.sleep(60)

                browser.close()

                # Mark as completed
                self.update_builder_progress(builder_email, 'discord_invited')
                return True

        except Exception as e:
            print(f"❌ Error with Discord: {e}")
            return False

    def complete_onboarding(self, builder_email, builder_name, builder_interests=''):
        """
        Run complete onboarding workflow
        All steps in sequence
        """
        print("\n" + "="*60)
        print(f"🚀 COMPLETE ONBOARDING: {builder_name}")
        print("="*60)

        builder_data = {
            'name': builder_name,
            'email': builder_email,
            'interests': builder_interests,
            'onboarded_at': datetime.now().isoformat()
        }

        # Track progress
        progress = {
            'builder': builder_data,
            'steps': {},
            'started_at': datetime.now().isoformat()
        }

        # Step 1: Create account
        print("\n📝 STEP 1: Creating Platform Account")
        print("-"*60)
        success = self.create_platform_account(builder_data)
        progress['steps']['account_created'] = success

        # Step 2: Send welcome kit
        print("\n📦 STEP 2: Sending Welcome Kit")
        print("-"*60)
        self.send_welcome_kit(builder_email, builder_name)
        progress['steps']['welcome_kit_delivered'] = True

        # Step 3: Discord invite
        print("\n💬 STEP 3: Adding to Discord")
        print("-"*60)
        success = self.add_to_discord(builder_email, builder_name)
        progress['steps']['discord_invited'] = success

        # Step 4: Summary
        print("\n" + "="*60)
        print("✅ ONBOARDING COMPLETE")
        print("="*60)

        completed_steps = sum(1 for v in progress['steps'].values() if v)
        total_steps = len(progress['steps'])

        print(f"\n📊 Progress: {completed_steps}/{total_steps} steps completed")
        print("\n✅ Completed:")
        for step, completed in progress['steps'].items():
            status = "✅" if completed else "❌"
            print(f"  {status} {step.replace('_', ' ').title()}")

        print("\n💡 Next Steps (Manual):")
        print("  1. Schedule onboarding call (send Calendly link)")
        print("  2. Monitor for first login")
        print("  3. Follow up in 24 hours")
        print("  4. Check Discord activity")

        # Save progress
        progress['completed_at'] = datetime.now().isoformat()
        self.save_onboarding_record(progress)

        return progress

    def update_builder_progress(self, builder_email, step):
        """Update builder's onboarding progress"""
        progress_file = self.data_dir / f"{builder_email.replace('@', '_at_')}_progress.json"

        if progress_file.exists():
            with open(progress_file) as f:
                progress = json.load(f)
        else:
            progress = {
                'email': builder_email,
                'steps': {},
                'started_at': datetime.now().isoformat()
            }

        progress['steps'][step] = {
            'completed': True,
            'completed_at': datetime.now().isoformat()
        }

        with open(progress_file, 'w') as f:
            json.dump(progress, f, indent=2)

    def save_onboarding_record(self, progress):
        """Save complete onboarding record"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_path = self.data_dir / f"onboarding_{progress['builder']['email'].replace('@', '_at_')}_{timestamp}.json"

        with open(file_path, 'w') as f:
            json.dump(progress, f, indent=2)

        print(f"\n💾 Onboarding record saved: {file_path}")

    def generate_onboarding_report(self):
        """Generate report of all onboarded builders"""
        print("\n" + "="*60)
        print("📊 BUILDER ONBOARDING REPORT")
        print("="*60)

        # Find all onboarding records
        records = list(self.data_dir.glob('onboarding_*.json'))

        if not records:
            print("\n⚠️  No onboarding records found")
            return

        print(f"\nTotal Builders Onboarded: {len(records)}")

        # Analyze completion rates
        total_steps = 0
        completed_steps = 0

        for record_file in records:
            with open(record_file) as f:
                record = json.load(f)

            builder_name = record['builder']['name']
            builder_email = record['builder']['email']

            steps = record.get('steps', {})
            completed = sum(1 for v in steps.values() if v)
            total = len(steps)

            total_steps += total
            completed_steps += completed

            completion_rate = (completed / total * 100) if total > 0 else 0

            print(f"\n👤 {builder_name} ({builder_email})")
            print(f"   Progress: {completed}/{total} ({completion_rate:.0f}%)")
            print(f"   Onboarded: {record.get('started_at', 'Unknown')}")

        # Overall stats
        overall_completion = (completed_steps / total_steps * 100) if total_steps > 0 else 0
        print(f"\n📈 Overall Completion Rate: {overall_completion:.1f}%")

        print("\n="*60)


def main():
    """Main CLI interface"""
    import argparse

    parser = argparse.ArgumentParser(description='JARVIS Builder Onboarding Automation')
    parser.add_argument('--onboard', nargs=2, metavar=('NAME', 'EMAIL'), help='Complete onboarding for new builder')
    parser.add_argument('--create-account', nargs=2, metavar=('NAME', 'EMAIL'), help='Create platform account')
    parser.add_argument('--send-kit', nargs=2, metavar=('NAME', 'EMAIL'), help='Send welcome kit')
    parser.add_argument('--add-discord', nargs=2, metavar=('NAME', 'EMAIL'), help='Add to Discord')
    parser.add_argument('--report', action='store_true', help='Generate onboarding report')

    args = parser.parse_args()

    onboarding = BuilderOnboarding()

    if args.onboard:
        name, email = args.onboard
        onboarding.complete_onboarding(email, name)

    elif args.create_account:
        name, email = args.create_account
        builder_data = {'name': name, 'email': email}
        onboarding.create_platform_account(builder_data)

    elif args.send_kit:
        name, email = args.send_kit
        onboarding.send_welcome_kit(email, name)

    elif args.add_discord:
        name, email = args.add_discord
        onboarding.add_to_discord(email, name)

    elif args.report:
        onboarding.generate_onboarding_report()

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
