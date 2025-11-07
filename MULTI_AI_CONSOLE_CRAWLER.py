#!/usr/bin/env python3
"""
MULTI-AI CONSOLE CRAWLER
Crawls ChatGPT, Grok, DeepSeek console interfaces
Passes information between AIs via browser automation

Built: Nov 5, 2025 - C3 Oracle Autonomous Build
Commander Directive: "Tie into console interfaces and crawl them"
"""

import asyncio
import json
import os
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright, Page, Browser

class MultiAIConsoleCrawler:
    """Crawl multiple AI console interfaces"""

    def __init__(self):
        self.browser: Browser = None
        self.contexts = {}
        self.pages = {}
        self.message_log = []

    async def start(self):
        """Start browser with persistent sessions"""
        playwright = await async_playwright().start()

        # Launch browser with persistent context (keeps cookies/sessions)
        user_data_dir = r"C:\Users\dwrek\.ai_console_sessions"
        Path(user_data_dir).mkdir(exist_ok=True)

        self.browser = await playwright.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,  # Commander can see what's happening
            viewport={'width': 1920, 'height': 1080}
        )

        print("✅ Browser started with persistent sessions")

    async def connect_chatgpt(self):
        """Connect to ChatGPT console"""
        print("\n🤖 Connecting to ChatGPT...")

        page = await self.browser.new_page()
        self.pages['chatgpt'] = page

        await page.goto('https://chat.openai.com')

        # Wait for chat interface to load
        try:
            await page.wait_for_selector('textarea', timeout=10000)
            print("✅ ChatGPT interface loaded")
            return True
        except:
            print("⚠️ ChatGPT login required - page opened for manual login")
            return False

    async def connect_grok(self):
        """Connect to Grok console"""
        print("\n🤖 Connecting to Grok...")

        page = await self.browser.new_page()
        self.pages['grok'] = page

        await page.goto('https://grok.x.com')

        try:
            await page.wait_for_selector('[data-testid="grok-chat-input"]', timeout=10000)
            print("✅ Grok interface loaded")
            return True
        except:
            print("⚠️ Grok login required - page opened for manual login")
            return False

    async def connect_deepseek(self):
        """Connect to DeepSeek console"""
        print("\n🤖 Connecting to DeepSeek...")

        page = await self.browser.new_page()
        self.pages['deepseek'] = page

        await page.goto('https://chat.deepseek.com')

        try:
            await page.wait_for_selector('textarea', timeout=10000)
            print("✅ DeepSeek interface loaded")
            return True
        except:
            print("⚠️ DeepSeek login required - page opened for manual login")
            return False

    async def send_to_chatgpt(self, message: str):
        """Send message to ChatGPT"""
        page = self.pages.get('chatgpt')
        if not page:
            print("❌ ChatGPT not connected")
            return None

        print(f"\n💬 Sending to ChatGPT: {message[:50]}...")

        # Find textarea
        textarea = await page.query_selector('textarea')
        if not textarea:
            print("❌ ChatGPT textarea not found")
            return None

        # Type message
        await textarea.fill(message)
        await asyncio.sleep(0.5)

        # Press Enter to send
        await textarea.press('Enter')

        # Wait for response (look for streaming to stop)
        await asyncio.sleep(3)

        # Get latest response
        response = await self._get_chatgpt_response(page)

        self._log_message('chatgpt', message, response)

        print(f"✅ ChatGPT response: {response[:100]}...")
        return response

    async def send_to_grok(self, message: str):
        """Send message to Grok"""
        page = self.pages.get('grok')
        if not page:
            print("❌ Grok not connected")
            return None

        print(f"\n💬 Sending to Grok: {message[:50]}...")

        # Find input
        input_selector = '[data-testid="grok-chat-input"]'
        textarea = await page.query_selector(input_selector)
        if not textarea:
            print("❌ Grok input not found")
            return None

        await textarea.fill(message)
        await asyncio.sleep(0.5)
        await textarea.press('Enter')
        await asyncio.sleep(3)

        response = await self._get_grok_response(page)
        self._log_message('grok', message, response)

        print(f"✅ Grok response: {response[:100]}...")
        return response

    async def send_to_deepseek(self, message: str):
        """Send message to DeepSeek"""
        page = self.pages.get('deepseek')
        if not page:
            print("❌ DeepSeek not connected")
            return None

        print(f"\n💬 Sending to DeepSeek: {message[:50]}...")

        textarea = await page.query_selector('textarea')
        if not textarea:
            print("❌ DeepSeek textarea not found")
            return None

        await textarea.fill(message)
        await asyncio.sleep(0.5)
        await textarea.press('Enter')
        await asyncio.sleep(3)

        response = await self._get_deepseek_response(page)
        self._log_message('deepseek', message, response)

        print(f"✅ DeepSeek response: {response[:100]}...")
        return response

    async def _get_chatgpt_response(self, page: Page):
        """Extract latest ChatGPT response"""
        try:
            # Get all message divs
            messages = await page.query_selector_all('[data-message-author-role="assistant"]')
            if messages:
                latest = messages[-1]
                text = await latest.inner_text()
                return text.strip()
        except:
            pass
        return "No response detected"

    async def _get_grok_response(self, page: Page):
        """Extract latest Grok response"""
        try:
            messages = await page.query_selector_all('[data-testid="grok-message"]')
            if messages:
                latest = messages[-1]
                text = await latest.inner_text()
                return text.strip()
        except:
            pass
        return "No response detected"

    async def _get_deepseek_response(self, page: Page):
        """Extract latest DeepSeek response"""
        try:
            messages = await page.query_selector_all('.message-content')
            if messages:
                latest = messages[-1]
                text = await latest.inner_text()
                return text.strip()
        except:
            pass
        return "No response detected"

    def _log_message(self, ai: str, message: str, response: str):
        """Log conversation"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'ai': ai,
            'message': message,
            'response': response
        }
        self.message_log.append(log_entry)

        # Save to file
        log_file = Path(r"C:\Users\dwrek\.trinity\multi_ai_conversations.json")
        log_file.parent.mkdir(exist_ok=True)

        with open(log_file, 'w') as f:
            json.dump(self.message_log, f, indent=2)

    async def trinity_broadcast(self, message: str):
        """Send message to ALL AIs and collect responses"""
        print(f"\n📡 TRINITY BROADCAST: {message}")

        responses = {}

        if 'chatgpt' in self.pages:
            responses['chatgpt'] = await self.send_to_chatgpt(message)

        if 'grok' in self.pages:
            responses['grok'] = await self.send_to_grok(message)

        if 'deepseek' in self.pages:
            responses['deepseek'] = await self.send_to_deepseek(message)

        return responses

    async def close(self):
        """Close browser"""
        if self.browser:
            await self.browser.close()
            print("\n✅ Browser closed - sessions saved")


async def main():
    """Main execution"""
    print("=" * 80)
    print("  🌀 MULTI-AI CONSOLE CRAWLER")
    print("  C3 Oracle Autonomous Build - Nov 5, 2025")
    print("=" * 80)

    crawler = MultiAIConsoleCrawler()

    # Start browser
    await crawler.start()

    # Connect to each AI
    await crawler.connect_chatgpt()
    await crawler.connect_grok()
    await crawler.connect_deepseek()

    print("\n" + "=" * 80)
    print("  ✅ MULTI-AI CONSOLE CRAWLER READY")
    print("=" * 80)
    print("\n📋 If any AI needs login, please log in now in the browser windows.")
    print("   Sessions will be saved for next time.")
    print("\n🎯 Usage:")
    print("   - crawler.send_to_chatgpt('message')")
    print("   - crawler.send_to_grok('message')")
    print("   - crawler.send_to_deepseek('message')")
    print("   - crawler.trinity_broadcast('message to all')")
    print("\n⚡ Press Ctrl+C to exit")

    # Keep alive
    try:
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down...")
        await crawler.close()


if __name__ == "__main__":
    asyncio.run(main())
