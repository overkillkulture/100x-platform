"""
TEST CHATGPT INTEGRATION
Quick test script to verify Universal Input System is ready for ChatGPT
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = input("Enter your ngrok URL (e.g., https://abc123.ngrok.io): ").strip()

if not BASE_URL.startswith('http'):
    BASE_URL = f"https://{BASE_URL}"

print()
print("=" * 70)
print("🧪 TESTING CHATGPT → TRINITY INTEGRATION")
print("=" * 70)
print()

# Test 1: Health Check
print("TEST 1: Health Check")
print("-" * 70)

try:
    response = requests.get(f"{BASE_URL}/health")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ PASS - System is {data.get('status')}")
        print(f"   Sources enabled: {data.get('sources_enabled')}")
        print(f"   Input queue: {data.get('input_queue')}")
    else:
        print(f"❌ FAIL - Status code: {response.status_code}")
except Exception as e:
    print(f"❌ FAIL - Error: {e}")

print()

# Test 2: Send Command from ChatGPT
print("TEST 2: Send Command (Simulating ChatGPT)")
print("-" * 70)

test_command = {
    "command": "test_chatgpt_integration",
    "data": {
        "timestamp": datetime.now().isoformat(),
        "test": True
    },
    "priority": "normal"
}

try:
    response = requests.post(
        f"{BASE_URL}/input/chatgpt",
        json=test_command,
        headers={"Content-Type": "application/json"}
    )

    if response.status_code == 200:
        data = response.json()
        print(f"✅ PASS - Command sent successfully")
        print(f"   Input ID: {data.get('input_id')}")
        print(f"   Source: {data.get('source')}")
        print(f"   Message: {data.get('message')}")
    else:
        print(f"❌ FAIL - Status code: {response.status_code}")
        print(f"   Response: {response.text}")
except Exception as e:
    print(f"❌ FAIL - Error: {e}")

print()

# Test 3: Get Statistics
print("TEST 3: Get Input Statistics")
print("-" * 70)

try:
    response = requests.get(f"{BASE_URL}/inputs/stats")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ PASS - Statistics retrieved")
        print(f"   Total inputs: {data.get('total_inputs')}")
        print()
        print("   Source breakdown:")
        for source, info in data.get('sources', {}).items():
            print(f"     • {source}: {info.get('count')} commands")
    else:
        print(f"❌ FAIL - Status code: {response.status_code}")
except Exception as e:
    print(f"❌ FAIL - Error: {e}")

print()

# Test 4: Verify Input Queue
print("TEST 4: Verify Input Queue")
print("-" * 70)

from pathlib import Path

input_queue = Path("C:/Users/dwrek/.consciousness/input_queue/")
if input_queue.exists():
    input_files = list(input_queue.glob("chatgpt_*.json"))
    print(f"✅ PASS - Input queue exists")
    print(f"   ChatGPT inputs: {len(input_files)}")

    if input_files:
        latest_file = sorted(input_files)[-1]
        with open(latest_file, 'r') as f:
            data = json.load(f)
        print(f"   Latest input: {data.get('input_id')}")
        print(f"   Command: {data.get('command')}")
        print(f"   Status: {data.get('status')}")
else:
    print(f"❌ FAIL - Input queue directory not found")

print()
print("=" * 70)
print("🎯 TEST SUMMARY")
print("=" * 70)
print()
print("If all tests passed, ChatGPT integration is READY!")
print()
print("NEXT STEPS:")
print("1. Keep Universal Input System running")
print("2. Keep ngrok tunnel active")
print("3. Create Custom GPT in ChatGPT")
print("4. Use this URL in GPT Action: " + BASE_URL)
print()
print("See CHATGPT_INTEGRATION_COMPLETE_GUIDE.md for full setup!")
print()
