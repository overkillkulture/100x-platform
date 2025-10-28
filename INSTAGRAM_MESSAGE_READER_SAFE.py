"""
🚨 INSTAGRAM MESSAGE READER - PROBATION-SAFE MODE 🚨

ACCOUNT ON PROBATION UNTIL NOV 2ND - READ ONLY, NO ACTIONS!

This script ONLY reads messages. Does NOT:
- Send messages
- Like anything
- Follow anyone
- Comment on anything
- Post anything

100% safe for probation period.
"""

import asyncio
import json
from datetime import datetime
from playwright.async_api import async_playwright
from pathlib import Path

class InstagramMessageReader:
    """SAFE: Only reads messages, no actions that could trigger ban"""

    def __init__(self):
        self.browser = None
        self.context = None
        self.page = None
        self.logged_in = False
        self.session_file = 'C:/Users/dwrek/instagram_session.json'
        self.messages_log = Path('C:/Users/dwrek/Desktop/INSTAGRAM_MESSAGES_LOG.txt')

    async def launch_browser(self):
        """Launch browser with saved session"""
        playwright = await async_playwright().start()

        self.browser = await playwright.chromium.launch(
            headless=False,  # Show browser for safety
            args=['--start-maximized']
        )

        # Try to load saved session
        try:
            self.context = await self.browser.new_context(
                storage_state=self.session_file,
                viewport={'width': 1920, 'height': 1080}
            )
            print("✅ Loaded saved Instagram session")
        except:
            self.context = await self.browser.new_context(
                viewport={'width': 1920, 'height': 1080}
            )
            print("🔐 New session - will need to login")

        self.page = await self.context.new_page()

    async def login_check(self):
        """Check if logged in (READ ONLY)"""
        await self.page.goto('https://www.instagram.com/')
        await self.page.wait_for_load_state('networkidle')

        # Check if already logged in
        try:
            await self.page.wait_for_selector('svg[aria-label*="Direct"]', timeout=5000)
            self.logged_in = True
            print("✅ Already logged in to Instagram!")
            await self.context.storage_state(path=self.session_file)
            return True
        except:
            print("🔐 Please log in manually in the browser...")
            print("⏳ Waiting for login...")

            # Wait for Direct Messages icon (means logged in)
            await self.page.wait_for_selector('svg[aria-label*="Direct"]', timeout=120000)
            self.logged_in = True

            # Save session
            await self.context.storage_state(path=self.session_file)
            print("✅ Login successful! Session saved.")
            return True

    async def read_all_messages(self):
        """READ ONLY: Check all messages for bugs or requests"""
        if not self.logged_in:
            raise Exception("Not logged in")

        print("\n" + "="*70)
        print("📬 READING INSTAGRAM MESSAGES (Probation-Safe Mode)")
        print("="*70)

        # Navigate to Direct Messages
        dm_icon = await self.page.wait_for_selector('svg[aria-label*="Direct"]')
        await dm_icon.click()
        await self.page.wait_for_load_state('networkidle')
        await asyncio.sleep(2)

        messages_found = []

        try:
            # Get all conversation previews
            conversations = await self.page.query_selector_all('div[role="listitem"]')

            print(f"\n📊 Found {len(conversations)} conversations")

            # Read first 10 conversations
            for i, conv in enumerate(conversations[:10]):
                try:
                    # Click conversation
                    await conv.click()
                    await asyncio.sleep(1)

                    # Get conversation details
                    username_elem = await self.page.query_selector('div[role="dialog"] header span')
                    username = await username_elem.inner_text() if username_elem else "Unknown"

                    # Get recent messages
                    message_elems = await self.page.query_selector_all('div[role="row"]')

                    recent_messages = []
                    for msg_elem in message_elems[-5:]:  # Last 5 messages
                        try:
                            text = await msg_elem.inner_text()
                            recent_messages.append(text)
                        except:
                            pass

                    # Check if contains bug keywords
                    full_text = " ".join(recent_messages).lower()
                    is_bug_related = any(keyword in full_text for keyword in [
                        'bug', 'error', 'broken', 'not working', 'issue', 'problem',
                        'help', 'fix', 'crash', 'fail'
                    ])

                    message_data = {
                        'username': username,
                        'preview': recent_messages[-1] if recent_messages else "No messages",
                        'is_bug_related': is_bug_related,
                        'timestamp': datetime.now().isoformat()
                    }

                    messages_found.append(message_data)

                    # Print status
                    status = "🐛 BUG RELATED" if is_bug_related else "💬 Normal"
                    print(f"\n{i+1}. {status} - @{username}")
                    print(f"   Latest: {message_data['preview'][:100]}...")

                except Exception as e:
                    print(f"   ⚠️  Couldn't read conversation {i+1}: {e}")

        except Exception as e:
            print(f"❌ Error reading messages: {e}")

        # Save log
        self._save_message_log(messages_found)

        return messages_found

    def _save_message_log(self, messages):
        """Save messages to log file"""
        with open(self.messages_log, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("📬 INSTAGRAM MESSAGES - PROBATION-SAFE READ\n")
            f.write(f"Checked: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*70 + "\n\n")

            # Bug-related messages first
            bugs = [m for m in messages if m['is_bug_related']]
            if bugs:
                f.write("🐛 POTENTIAL BUG REPORTS:\n")
                f.write("-"*70 + "\n")
                for msg in bugs:
                    f.write(f"\n@{msg['username']}\n")
                    f.write(f"Message: {msg['preview']}\n")
                    f.write(f"Time: {msg['timestamp']}\n")
                f.write("\n")

            # All other messages
            f.write("\n💬 ALL MESSAGES:\n")
            f.write("-"*70 + "\n")
            for msg in messages:
                status = "🐛" if msg['is_bug_related'] else "💬"
                f.write(f"\n{status} @{msg['username']}\n")
                f.write(f"   {msg['preview'][:200]}\n")

            f.write("\n" + "="*70 + "\n")
            f.write(f"Total: {len(messages)} conversations checked\n")
            f.write(f"Bugs: {len(bugs)} potential bug reports\n")

        print(f"\n✅ Log saved: {self.messages_log}")

    async def close(self):
        """Close browser"""
        if self.browser:
            await self.browser.close()


async def main():
    print("━"*70)
    print("🚨 INSTAGRAM MESSAGE READER - PROBATION-SAFE MODE 🚨")
    print("━"*70)
    print("\n⚠️  ACCOUNT ON PROBATION UNTIL NOVEMBER 2ND")
    print("    This script ONLY READS messages - no actions!")
    print("    100% safe for probation period.\n")

    reader = InstagramMessageReader()

    try:
        # Launch and login
        await reader.launch_browser()
        await reader.login_check()

        # Read all messages
        messages = await reader.read_all_messages()

        # Summary
        bugs = [m for m in messages if m['is_bug_related']]

        print("\n" + "="*70)
        print("📊 MESSAGE CHECK COMPLETE")
        print("="*70)
        print(f"\n✅ Total conversations: {len(messages)}")
        print(f"🐛 Potential bug reports: {len(bugs)}")
        print(f"📝 Log saved: {reader.messages_log}")

        if bugs:
            print("\n🐛 BUG-RELATED MESSAGES:")
            for bug in bugs:
                print(f"   • @{bug['username']}: {bug['preview'][:60]}...")

        print("\n💡 Browser will stay open for manual review.")
        input("Press ENTER to close...")

    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        await reader.close()


if __name__ == '__main__':
    asyncio.run(main())
