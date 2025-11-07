#!/usr/bin/env python3
"""Quick bug analysis script"""
import json
import os
from pathlib import Path

bug_dir = Path("/home/user/100x-platform/.bug_tasks")

bugs = {
    'pending': [],
    'test_messages': [],
    'feature_requests': [],
    'completed': [],
    'requires_action': [],
    'invalid': []
}

for bug_file in sorted(bug_dir.glob("bug_*.json")):
    try:
        with open(bug_file) as f:
            data = json.load(f)

        bug_num = data.get('bug_number', '?')
        title = data.get('title', '')
        desc = data.get('description', '')
        status = data.get('status', 'pending')

        # Categorize based on filename prefix
        name = bug_file.name
        if name.startswith('COMPLETED'):
            bugs['completed'].append(bug_num)
        elif name.startswith('INVALID'):
            bugs['invalid'].append(bug_num)
        elif name.startswith('ANSWERED'):
            bugs['invalid'].append(bug_num)
        elif name.startswith('REQUIRES_USER_ACTION'):
            bugs['requires_action'].append(bug_num)
        elif 'test' in title.lower() or 'are you there' in desc.lower():
            bugs['test_messages'].append((bug_num, title[:50]))
        elif 'combine' in desc.lower() or 'merge' in desc.lower():
            bugs['feature_requests'].append((bug_num, title[:50]))
        else:
            bugs['pending'].append((bug_num, title[:60]))
    except Exception as e:
        print(f"Error reading {bug_file}: {e}")

print("=" * 70)
print("BUG ANALYSIS SUMMARY")
print("=" * 70)
print(f"\n✅ Completed: {len(bugs['completed'])} bugs")
print(f"❌ Invalid/Answered: {len(bugs['invalid'])} bugs")
print(f"⏸️  Requires User Action: {len(bugs['requires_action'])} bugs")
print(f"🧪 Test Messages: {len(bugs['test_messages'])} bugs")
print(f"🎯 Feature Requests: {len(bugs['feature_requests'])} bugs")
print(f"🐛 Real Pending Bugs: {len(bugs['pending'])} bugs")

print("\n" + "=" * 70)
print("REAL PENDING BUGS TO FIX:")
print("=" * 70)
for bug_num, title in bugs['pending'][:20]:
    print(f"Bug #{bug_num}: {title}")

print("\n" + "=" * 70)
print("FEATURE REQUESTS:")
print("=" * 70)
for bug_num, title in bugs['feature_requests'][:10]:
    print(f"Bug #{bug_num}: {title}")

print("\n" + "=" * 70)
print("TEST MESSAGES:")
print("=" * 70)
for bug_num, title in bugs['test_messages'][:10]:
    print(f"Bug #{bug_num}: {title}")
