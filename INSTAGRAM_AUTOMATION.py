#!/usr/bin/env python3
"""
INSTAGRAM AUTOMATION - Browser Control
Check online status, send DMs via Playwright
⚠️ USE CAREFULLY - Violates Instagram ToS (risk of ban)
"""

from playwright.sync_api import sync_playwright
import time
import json
from datetime import datetime, timedelta
from pathlib import Path

class InstagramBot:
    def __init__(self, session_file='instagram_session.json'):
        self.session_file = Path(__file__).parent / session_file
        self.message_log = []
        self.max_messages_per_hour = 15
        self.min_delay_seconds = 60

    def login(self, username, password):
        """Login to Instagram and save session"""
        print("🔐 Logging into Instagram...")

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()

            # Go to Instagram
            page.goto('https://www.instagram.com/')
            time.sleep(3)

            try:
                # Click "Accept cookies" if present
                page.click('button:has-text("Allow")', timeout=3000)
            except:
                pass

            # Fill login form
            page.fill('input[name="username"]', username)
            page.fill('input[name="password"]', password)
            page.click('button[type="submit"]')

            print("⏳ Waiting for login...")
            time.sleep(8)

            # Handle "Save Login Info" prompt
            try:
                page.click('button:has-text("Not")', timeout=5000)
            except:
                pass

            # Handle "Turn on Notifications" prompt
            try:
                page.click('button:has-text("Not Now")', timeout=5000)
            except:
                pass

            # Save session
            context = page.context
            context.storage_state(path=str(self.session_file))

            print("✅ Login successful! Session saved.")
            browser.close()

    def check_online_status(self, username):
        """Check if user is online on Instagram"""
        if not self.session_file.exists():
            print("❌ No session found. Run login() first.")
            return None

        print(f"🔍 Checking if @{username} is online...")

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(storage_state=str(self.session_file))
            page = context.new_page()

            try:
                # Go to DMs
                page.goto('https://www.instagram.com/direct/inbox/')
                time.sleep(4)

                # Search for user
                page.fill('input[placeholder*="Search"]', username)
                time.sleep(2)

                # Click on user's conversation
                try:
                    page.click(f'text={username}', timeout=5000)
                    time.sleep(3)
                except:
                    print(f"❌ Could not find @{username} in DMs")
                    return None

                # Check for "Active now" indicator
                try:
                    # Look for active status text
                    active_now = page.locator('text=/Active now/i').count() > 0

                    if active_now:
                        print(f"🟢 @{username} is ONLINE")
                        return {
                            'username': username,
                            'online': True,
                            'status': 'Active now',
                            'checked_at': datetime.now().isoformat()
                        }
                    else:
                        # Try to get "Active X ago"
                        try:
                            status_text = page.locator('[class*="x1lliihq"]').first.inner_text()
                            print(f"⚪ @{username}: {status_text}")
                            return {
                                'username': username,
                                'online': False,
                                'status': status_text,
                                'checked_at': datetime.now().isoformat()
                            }
                        except:
                            print(f"⚪ @{username} is OFFLINE")
                            return {
                                'username': username,
                                'online': False,
                                'status': 'Offline',
                                'checked_at': datetime.now().isoformat()
                            }
                except Exception as e:
                    print(f"❓ Could not determine status: {e}")
                    return None

            finally:
                browser.close()

    def send_dm(self, username, message):
        """Send Instagram DM (with safety limits)"""
        # Check rate limits
        if not self._can_send_message():
            print(f"⚠️  RATE LIMIT: Already sent {self.max_messages_per_hour} messages in last hour")
            return False

        if not self.session_file.exists():
            print("❌ No session found. Run login() first.")
            return False

        print(f"💬 Sending DM to @{username}...")

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(storage_state=str(self.session_file))
            page = context.new_page()

            try:
                # Go to DMs
                page.goto('https://www.instagram.com/direct/inbox/')
                time.sleep(4)

                # Search for user
                page.fill('input[placeholder*="Search"]', username)
                time.sleep(2)

                # Click on user
                try:
                    page.click(f'text={username}', timeout=5000)
                    time.sleep(3)
                except:
                    print(f"❌ Could not find @{username}")
                    return False

                # Type message
                page.fill('textarea[placeholder*="Message"]', message)
                time.sleep(1)

                # Send
                page.click('button:has-text("Send")')
                time.sleep(2)

                print(f"✅ Message sent to @{username}")

                # Log message for rate limiting
                self._log_message()

                return True

            except Exception as e:
                print(f"❌ Error sending message: {e}")
                return False
            finally:
                browser.close()

    def _can_send_message(self):
        """Check if we can send message (rate limit)"""
        now = datetime.now()
        one_hour_ago = now - timedelta(hours=1)

        # Remove old messages
        self.message_log = [t for t in self.message_log if t > one_hour_ago]

        return len(self.message_log) < self.max_messages_per_hour

    def _log_message(self):
        """Log message timestamp"""
        self.message_log.append(datetime.now())

    def get_message_stats(self):
        """Get current message sending stats"""
        now = datetime.now()
        one_hour_ago = now - timedelta(hours=1)

        recent_messages = [t for t in self.message_log if t > one_hour_ago]

        return {
            'messages_last_hour': len(recent_messages),
            'max_per_hour': self.max_messages_per_hour,
            'can_send': len(recent_messages) < self.max_messages_per_hour
        }


if __name__ == '__main__':
    print("="*60)
    print("📷 INSTAGRAM AUTOMATION")
    print("="*60)
    print("⚠️  WARNING: This violates Instagram ToS")
    print("⚠️  Risk of account ban - use carefully!")
    print("="*60)
    print()

    bot = InstagramBot()

    # Example usage:
    # 1. First time: Login and save session
    # bot.login('your_username', 'your_password')

    # 2. Check if someone is online
    # status = bot.check_online_status('joshua')
    # print(status)

    # 3. Send a DM
    # success = bot.send_dm('joshua', 'Hey! Saw you online 👋')

    # 4. Check rate limits
    # stats = bot.get_message_stats()
    # print(stats)

    print("📖 Instructions:")
    print("1. Uncomment bot.login() and add your Instagram credentials")
    print("2. Run once to save session")
    print("3. Use check_online_status() to see who's online")
    print("4. Use send_dm() to message someone")
    print()
    print("💡 Integrate with Neighborhood Watch for visual status!")
