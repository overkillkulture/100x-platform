#!/usr/bin/env python3
"""
🤖 TRAINING BOT SYSTEM - Automated User Flow Testing
Simulates 3 types of users testing the platform
"""

import asyncio
import random
import requests
from datetime import datetime
from playwright.async_api import async_playwright
import json
from pathlib import Path

# Bot personalities
BOTS = {
    'curious_newbie': {
        'name': 'Sarah (Curious Newbie)',
        'emoji': '🟢',
        'behavior': 'Explores basics, asks simple questions, submits obvious bugs',
        'pages_to_visit': [
            'https://conciousnessrevolution.io',
            'https://conciousnessrevolution.io/bugs.html',
            'https://conciousnessrevolution.io/simple-gate-v2.html',
        ],
        'questions': [
            "What is this platform about?",
            "How do I get started?",
            "Where do I find the tools?",
            "Is this free to use?"
        ],
        'bug_probability': 0.3,  # 30% chance to submit bug
        'session_duration': 300  # 5 minutes
    },
    'power_user': {
        'name': 'Marcus (Power User)',
        'emoji': '🟡',
        'behavior': 'Tests edge cases, deep dives, detailed bug reports',
        'pages_to_visit': [
            'https://conciousnessrevolution.io',
            'https://conciousnessrevolution.io/bugs.html',
            'https://conciousnessrevolution.io/araya-chat.html',
            'https://conciousnessrevolution.io/COMMAND_CENTER_HUD_COMMS.html',
        ],
        'questions': [
            "How does the Trinity system coordinate between instances?",
            "What's the technical architecture of the bug tracking?",
            "Can I integrate this with my own tools?",
            "What APIs are available?"
        ],
        'bug_probability': 0.7,  # 70% chance to submit bug
        'session_duration': 900  # 15 minutes
    },
    'silent_observer': {
        'name': 'Alex (Silent Observer)',
        'emoji': '🔵',
        'behavior': 'Just browses, tests analytics, no interaction',
        'pages_to_visit': [
            'https://conciousnessrevolution.io',
            'https://conciousnessrevolution.io/simple-gate-v2.html',
        ],
        'questions': [],  # Silent - no questions
        'bug_probability': 0.05,  # 5% chance to submit bug
        'session_duration': 180  # 3 minutes
    }
}

CHATGPT_API = 'http://localhost:5555/chat'

class TrainingBot:
    """Automated testing bot with personality"""

    def __init__(self, bot_type: str):
        self.type = bot_type
        self.config = BOTS[bot_type]
        self.session_id = f"training_bot_{bot_type}_{datetime.now().strftime('%H%M%S')}"
        self.log = []

    async def run_session(self, headless=True):
        """Run complete bot session"""
        print(f"\n{'='*60}")
        print(f"{self.config['emoji']} Starting: {self.config['name']}")
        print(f"{'='*60}")
        print(f"Behavior: {self.config['behavior']}")
        print(f"Duration: {self.config['session_duration']}s")
        print(f"Pages to visit: {len(self.config['pages_to_visit'])}")

        self.log.append({
            'event': 'session_start',
            'timestamp': datetime.now().isoformat(),
            'bot': self.config['name']
        })

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=headless)
            page = await browser.new_page()

            # Visit each page
            for url in self.config['pages_to_visit']:
                await self._visit_page(page, url)
                await asyncio.sleep(random.uniform(2, 5))  # Natural delay

            # Ask questions (if any)
            for question in self.config['questions']:
                await self._ask_chatgpt(question)
                await asyncio.sleep(random.uniform(1, 3))

            # Maybe submit bug
            if random.random() < self.config['bug_probability']:
                await self._submit_test_bug(page)

            await browser.close()

        self.log.append({
            'event': 'session_end',
            'timestamp': datetime.now().isoformat(),
            'duration': self.config['session_duration']
        })

        self._save_log()
        print(f"\n✅ {self.config['name']} session complete!")
        return self.log

    async def _visit_page(self, page, url):
        """Visit a page and log interaction"""
        print(f"\n📄 Visiting: {url}")

        try:
            await page.goto(url, timeout=15000)
            await page.wait_for_load_state('networkidle', timeout=10000)

            # Scroll randomly
            scroll_amount = random.randint(100, 500)
            await page.evaluate(f'window.scrollBy(0, {scroll_amount})')

            self.log.append({
                'event': 'page_visit',
                'timestamp': datetime.now().isoformat(),
                'url': url,
                'status': 'success'
            })

            print(f"✅ Loaded successfully")

        except Exception as e:
            print(f"❌ Error: {e}")
            self.log.append({
                'event': 'page_visit',
                'timestamp': datetime.now().isoformat(),
                'url': url,
                'status': 'error',
                'error': str(e)
            })

    async def _ask_chatgpt(self, question):
        """Ask ChatGPT a question via API"""
        print(f"\n💬 Asking ChatGPT: {question}")

        try:
            response = requests.post(
                CHATGPT_API,
                json={
                    'message': question,
                    'session_id': self.session_id
                },
                timeout=30
            )

            if response.status_code == 200:
                answer = response.json().get('response', 'No response')
                print(f"✅ Got answer: {answer[:100]}...")

                self.log.append({
                    'event': 'chatgpt_query',
                    'timestamp': datetime.now().isoformat(),
                    'question': question,
                    'answer': answer,
                    'status': 'success'
                })
            else:
                print(f"❌ API error: {response.status_code}")

        except Exception as e:
            print(f"❌ Error: {e}")
            self.log.append({
                'event': 'chatgpt_query',
                'timestamp': datetime.now().isoformat(),
                'question': question,
                'status': 'error',
                'error': str(e)
            })

    async def _submit_test_bug(self, page):
        """Submit a test bug report"""
        print(f"\n🐛 Submitting test bug...")

        bugs = [
            {
                'title': f"[TEST BOT] Button not responding on homepage",
                'description': f"Found by {self.config['name']} during automated testing"
            },
            {
                'title': f"[TEST BOT] Page loading slow",
                'description': f"Automated test detected slow load time by {self.config['name']}"
            }
        ]

        bug = random.choice(bugs)

        self.log.append({
            'event': 'bug_submission',
            'timestamp': datetime.now().isoformat(),
            'bug': bug,
            'status': 'simulated'
        })

        print(f"✅ Bug logged: {bug['title']}")

    def _save_log(self):
        """Save session log"""
        log_dir = Path('TRAINING_BOT_LOGS')
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / f"{self.session_id}.json"
        with open(log_file, 'w') as f:
            json.dump({
                'bot_type': self.type,
                'bot_name': self.config['name'],
                'session_id': self.session_id,
                'log': self.log
            }, f, indent=2)

        print(f"\n📝 Log saved: {log_file}")


async def run_all_bots(headless=True):
    """Run all 3 bot types in sequence"""
    print("\n" + "🤖"*30)
    print("     TRAINING BOT SYSTEM - STARTING ALL BOTS")
    print("🤖"*30)

    results = {}

    for bot_type in BOTS.keys():
        bot = TrainingBot(bot_type)
        results[bot_type] = await bot.run_session(headless=headless)
        await asyncio.sleep(5)  # Brief pause between bots

    print("\n" + "="*60)
    print("✅ ALL BOTS COMPLETE")
    print("="*60)

    # Summary
    print("\n📊 SUMMARY:")
    for bot_type, log in results.items():
        print(f"\n{BOTS[bot_type]['emoji']} {BOTS[bot_type]['name']}:")
        print(f"  - Events: {len(log)}")
        print(f"  - Duration: {BOTS[bot_type]['session_duration']}s")

    return results


async def run_single_bot(bot_type: str, headless=True):
    """Run a single bot for testing"""
    if bot_type not in BOTS:
        print(f"❌ Unknown bot type: {bot_type}")
        print(f"Available: {', '.join(BOTS.keys())}")
        return

    bot = TrainingBot(bot_type)
    return await bot.run_session(headless=headless)


if __name__ == '__main__':
    import sys

    print("""
    🤖 TRAINING BOT SYSTEM
    =====================

    Simulates 3 user types testing your platform:

    🟢 Curious Newbie - Basic exploration
    🟡 Power User - Deep testing & bug hunting
    🔵 Silent Observer - Passive browsing

    Usage:
        python TRAINING_BOT_SYSTEM.py               # Run all bots
        python TRAINING_BOT_SYSTEM.py newbie        # Run newbie only
        python TRAINING_BOT_SYSTEM.py power         # Run power user only
        python TRAINING_BOT_SYSTEM.py silent        # Run silent observer only

    Logs saved to: TRAINING_BOT_LOGS/
    """)

    if len(sys.argv) > 1:
        bot_map = {
            'newbie': 'curious_newbie',
            'power': 'power_user',
            'silent': 'silent_observer'
        }
        bot_type = bot_map.get(sys.argv[1])

        if bot_type:
            asyncio.run(run_single_bot(bot_type, headless=False))
        else:
            print(f"❌ Unknown bot: {sys.argv[1]}")
            print(f"Available: {', '.join(bot_map.keys())}")
    else:
        # Run all bots
        asyncio.run(run_all_bots(headless=False))
