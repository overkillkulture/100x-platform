#!/usr/bin/env python3
"""
AUTONOMOUS BUG FIXER - Works 24/7 even when Claude terminal is down
Uses API failover: Primary → Backup → Ollama offline
"""

import os
import time
import json
import requests
from datetime import datetime

class AutoBugFixer:
    def __init__(self):
        # Load API keys from environment
        self.primary_api = os.getenv('ANTHROPIC_API_KEY', '')
        self.backup_api = os.getenv('ANTHROPIC_BACKUP_API_KEY', '')
        self.github_token = os.getenv('GITHUB_TOKEN', '')

        self.current_api = 'primary'
        self.ollama_fallback = True  # Use Ollama if both APIs fail

    def get_api_key(self):
        """Get current API key with automatic failover"""
        if self.current_api == 'primary' and self.primary_api:
            return self.primary_api
        elif self.current_api == 'backup' and self.backup_api:
            return self.backup_api
        else:
            print("⚠️  Both API keys exhausted, falling back to Ollama")
            return None

    def switch_to_backup(self):
        """Switch to backup API when primary fails"""
        if self.current_api == 'primary':
            print("🔄 Switching to backup API...")
            self.current_api = 'backup'
            return True
        else:
            print("⚠️  No more backup APIs available")
            return False

    def get_open_bugs(self):
        """Fetch open bugs from GitHub"""
        url = 'https://api.github.com/repos/overkillkulture/consciousness-bugs/issues?state=open'
        headers = {
            'Authorization': f'Bearer {self.github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }

        try:
            response = requests.get(url, headers=headers)
            if response.ok:
                return response.json()
            else:
                print(f"❌ GitHub API error: {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ Error fetching bugs: {e}")
            return []

    def is_real_bug(self, issue):
        """Filter out test submissions"""
        test_patterns = [
            'test', 'gfhg', 'are you there', 'are youthere',
            'new 42', 'new 100'  # Test submissions
        ]

        title_lower = issue['title'].lower()
        body_lower = (issue['body'] or '').lower()

        # If it's just a few words, probably a test
        if len(title_lower.split()) <= 3 and not issue['body']:
            return False

        # Check for test patterns
        for pattern in test_patterns:
            if pattern in title_lower or pattern in body_lower:
                return False

        return True

    def analyze_bug_with_claude(self, bug):
        """Use Claude API to analyze and suggest fix"""
        api_key = self.get_api_key()

        if not api_key:
            return self.analyze_bug_with_ollama(bug)

        prompt = f"""Analyze this bug report and suggest a fix:

Title: {bug['title']}
Description: {bug['body'] or 'No description'}
URL: {bug['html_url']}

Provide:
1. What the bug likely is
2. Which file(s) need to be fixed
3. Specific code changes needed
4. Priority level (low/medium/high)

Format as JSON."""

        headers = {
            'x-api-key': api_key,
            'anthropic-version': '2023-06-01',
            'content-type': 'application/json'
        }

        data = {
            'model': 'claude-3-5-sonnet-20241022',
            'max_tokens': 1024,
            'messages': [{
                'role': 'user',
                'content': prompt
            }]
        }

        try:
            response = requests.post(
                'https://api.anthropic.com/v1/messages',
                headers=headers,
                json=data,
                timeout=30
            )

            if response.status_code == 429:  # Rate limit
                print("⚠️  API rate limit hit, switching to backup...")
                if self.switch_to_backup():
                    return self.analyze_bug_with_claude(bug)
                else:
                    return self.analyze_bug_with_ollama(bug)

            if response.ok:
                result = response.json()
                return result['content'][0]['text']
            else:
                print(f"❌ Claude API error: {response.status_code}")
                return None

        except Exception as e:
            print(f"❌ Error calling Claude: {e}")
            return None

    def analyze_bug_with_ollama(self, bug):
        """Fallback to Ollama when APIs are exhausted"""
        print("🤖 Using Ollama (offline mode)...")

        prompt = f"""Analyze this bug and suggest a fix:
Title: {bug['title']}
Description: {bug['body'] or 'No description'}

Provide file to fix and code changes needed."""

        try:
            response = requests.post(
                'http://localhost:11434/api/generate',
                json={
                    'model': 'deepseek-r1:8b',
                    'prompt': prompt,
                    'stream': False
                },
                timeout=60
            )

            if response.ok:
                return response.json()['response']
            else:
                print(f"❌ Ollama error: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Ollama not available: {e}")
            return None

    def save_bug_analysis(self, bug, analysis):
        """Save bug analysis for later review"""
        bug_dir = 'BUG_ANALYSES'
        os.makedirs(bug_dir, exist_ok=True)

        filename = f"{bug_dir}/bug_{bug['number']}_{int(time.time())}.json"

        data = {
            'bug_number': bug['number'],
            'title': bug['title'],
            'url': bug['html_url'],
            'analysis': analysis,
            'analyzed_at': datetime.now().isoformat()
        }

        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"💾 Saved analysis to {filename}")
        return filename

    def run_continuous(self, interval=300):
        """Run continuously, checking for bugs every N seconds"""
        print("🤖 Autonomous Bug Fixer started!")
        print(f"📊 Checking for bugs every {interval} seconds")
        print(f"🔑 Using API: {self.current_api}")
        print(f"🔄 Backup available: {bool(self.backup_api)}")
        print(f"🖥️  Ollama fallback: {self.ollama_fallback}")
        print("\n" + "="*60 + "\n")

        while True:
            try:
                print(f"\n🔍 [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Checking for new bugs...")

                bugs = self.get_open_bugs()
                real_bugs = [b for b in bugs if self.is_real_bug(b)]

                print(f"📋 Found {len(bugs)} total issues, {len(real_bugs)} real bugs")

                for bug in real_bugs:
                    print(f"\n🐛 Analyzing: #{bug['number']} - {bug['title']}")

                    analysis = self.analyze_bug_with_claude(bug)

                    if analysis:
                        self.save_bug_analysis(bug, analysis)
                        print(f"✅ Bug #{bug['number']} analyzed")
                    else:
                        print(f"⚠️  Could not analyze bug #{bug['number']}")

                print(f"\n💤 Sleeping for {interval} seconds...\n")
                time.sleep(interval)

            except KeyboardInterrupt:
                print("\n\n🛑 Stopping autonomous bug fixer...")
                break
            except Exception as e:
                print(f"❌ Error in main loop: {e}")
                time.sleep(60)  # Wait a minute before retrying

if __name__ == '__main__':
    fixer = AutoBugFixer()
    fixer.run_continuous(interval=300)  # Check every 5 minutes
