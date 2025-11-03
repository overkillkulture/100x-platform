#!/usr/bin/env python3
"""
INSTAGRAM DM SENDER - Automated Messaging
Uses Playwright to send direct messages through browser automation
NO API CREDENTIALS NEEDED - Works immediately!

Commander can use this to reach out to beta testers via Instagram.
"""

import asyncio
import json
from datetime import datetime
from playwright.async_api import async_playwright
from pathlib import Path

class InstagramDMSender:
    def __init__(self):
        self.browser = None
        self.context = None
        self.page = None
        self.logged_in = False
        self.session_file = 'C:/Users/dwrek/instagram_session.json'
        self.message_log = Path('C:/Users/dwrek/100X_DEPLOYMENT/instagram_dm_log.json')
        self.load_message_log()

    def load_message_log(self):
        """Load sent message history"""
        if self.message_log.exists():
            with open(self.message_log) as f:
                self.log = json.load(f)
        else:
            self.log = {'messages_sent': []}

    def save_message_log(self):
        """Save message history"""
        with open(self.message_log, 'w') as f:
            json.dump(self.log, f, indent=2)

    async def launch_browser(self):
        """Launch browser with persistent session"""
        playwright = await async_playwright().start()

        self.browser = await playwright.chromium.launch(
            headless=False,  # Show browser so you can see what's happening
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

    async def login_to_instagram(self):
        """Navigate to Instagram and check if logged in"""
        await self.page.goto('https://www.instagram.com/')
        await self.page.wait_for_load_state('networkidle')

        # Check if already logged in
        try:
            await self.page.wait_for_selector('svg[aria-label*="Direct"]', timeout=3000)
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

    async def navigate_to_messages(self):
        """Navigate to Instagram Direct Messages"""
        if not self.logged_in:
            raise Exception("Not logged in to Instagram")

        # Click on Direct Messages icon
        dm_icon = await self.page.wait_for_selector('svg[aria-label*="Direct"]')
        await dm_icon.click()

        await self.page.wait_for_load_state('networkidle')
        await asyncio.sleep(2)

        print("✅ Navigated to Direct Messages")

    async def send_message_to_user(self, username, message):
        """Send a direct message to a specific user"""
        try:
            print(f"\n📤 Sending message to @{username}...")

            # Navigate to messages if not already there
            current_url = self.page.url
            if 'direct' not in current_url:
                await self.navigate_to_messages()

            # Click "Send message" button
            send_btn_selectors = [
                'text=Send message',
                'button:has-text("Send message")',
                'div[role="button"]:has-text("Send message")'
            ]

            for selector in send_btn_selectors:
                try:
                    send_btn = await self.page.wait_for_selector(selector, timeout=2000)
                    await send_btn.click()
                    break
                except:
                    continue

            await asyncio.sleep(1)

            # Search for user
            search_input = await self.page.wait_for_selector('input[placeholder*="Search"]')
            await search_input.fill(username)
            await asyncio.sleep(2)  # Wait for search results

            # Click on the first result
            result_selectors = [
                f'div[role="button"]:has-text("{username}")',
                'div[role="button"]'
            ]

            for selector in result_selectors:
                try:
                    first_result = await self.page.wait_for_selector(selector, timeout=3000)
                    await first_result.click()
                    break
                except:
                    continue

            # Click "Chat" button
            chat_btn = await self.page.wait_for_selector('button:has-text("Chat")', timeout=5000)
            await chat_btn.click()

            await asyncio.sleep(1)

            # Type message
            message_input = await self.page.wait_for_selector('div[role="textbox"]')
            await message_input.fill(message)

            await asyncio.sleep(0.5)

            # Send message
            send_button = await self.page.wait_for_selector('button:has-text("Send")')
            await send_button.click()

            print(f"✅ Message sent to @{username}!")

            # Log the message
            self.log['messages_sent'].append({
                'username': username,
                'message': message,
                'timestamp': datetime.now().isoformat(),
                'success': True
            })
            self.save_message_log()

            return True

        except Exception as e:
            print(f"❌ Failed to send message to @{username}: {e}")
            self.log['messages_sent'].append({
                'username': username,
                'message': message,
                'timestamp': datetime.now().isoformat(),
                'success': False,
                'error': str(e)
            })
            self.save_message_log()
            return False

    async def send_bulk_messages(self, users_and_messages):
        """
        Send messages to multiple users
        users_and_messages: [{'username': 'user1', 'message': 'Hi!'}, ...]
        """
        results = []

        for item in users_and_messages:
            username = item['username']
            message = item['message']

            success = await self.send_message_to_user(username, message)
            results.append({
                'username': username,
                'success': success
            })

            # Wait between messages to avoid rate limiting
            await asyncio.sleep(5)

        return results

    async def close(self):
        """Close browser"""
        if self.browser:
            await self.browser.close()


# Simple CLI interface
async def main():
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📱 INSTAGRAM DM SENDER")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

    sender = InstagramDMSender()

    # Launch and login
    await sender.launch_browser()
    await sender.login_to_instagram()

    # Example: Send to beta tester
    print("\n" + "="*50)
    print("EXAMPLE: Sending beta invite to user")
    print("="*50 + "\n")

    # Wait for user to decide
    username = input("Enter Instagram username to message: ")
    message = input("Enter your message: ")

    if username and message:
        await sender.send_message_to_user(username, message)
    else:
        print("❌ Cancelled")

    print("\n✅ Session complete!")
    print(f"📊 Message log saved to: {sender.message_log}")

    # Keep browser open for manual use
    print("\n💡 Browser will stay open. Close it when done.")
    input("Press ENTER to close...")

    await sender.close()


if __name__ == '__main__':
    asyncio.run(main())
