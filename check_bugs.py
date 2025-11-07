#!/usr/bin/env python3
import json
from pathlib import Path

bug_dir = Path("/home/user/100x-platform/.bug_tasks")

pending_bugs = []
completed_bugs = []

for num in [26, 27, 29, 34, 68, 70, 71, 72, 73, 74, 75, 76, 77, 78, 83, 85, 86, 87, 88, 90, 91, 92]:
    bug_file = bug_dir / f"bug_{num}.json"
    if bug_file.exists():
        with open(bug_file) as f:
            data = json.load(f)
        status = data.get('status', 'pending')
        title = data.get('title', '')[:60]

        if status == 'completed':
            completed_bugs.append((num, title))
        else:
            pending_bugs.append((num, status, title))

print("=" * 70)
print("PENDING BUGS:")
print("=" * 70)
for num, status, title in pending_bugs:
    print(f"Bug #{num} ({status}): {title}")

print("\n" + "=" * 70)
print("COMPLETED BUGS (need to be moved):")
print("=" * 70)
for num, title in completed_bugs:
    print(f"Bug #{num}: {title}")

print(f"\nTotal Pending: {len(pending_bugs)}")
print(f"Total Completed: {len(completed_bugs)}")
