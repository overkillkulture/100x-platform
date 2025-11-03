"""
AUTOFIX TRIGGER SYSTEM
Monitors bugs for AUTOFIX keyword and autonomously fixes all open bugs
"""

import requests
import json
import time
from datetime import datetime

GITHUB_API = "https://api.github.com/repos/overkillkulture/consciousness-bugs/issues"
CHECK_INTERVAL = 30  # Check every 30 seconds

def fetch_bugs():
    """Fetch all open bugs from GitHub"""
    response = requests.get(f"{GITHUB_API}?state=open&per_page=100")
    if response.ok:
        return response.json()
    return []

def check_for_autofix_trigger():
    """Check if any bug contains AUTOFIX trigger word"""
    bugs = fetch_bugs()

    trigger_words = ["AUTOFIX", "FIX_ALL_BUGS", "AUTO_FIX_NOW"]

    for bug in bugs:
        description = bug.get('body', '')
        title = bug.get('title', '')

        # Check if trigger word in title or description
        for trigger in trigger_words:
            if trigger in description.upper() or trigger in title.upper():
                return True, bug['number'], bug['user']['login']

    return False, None, None

def create_status_file(triggered_by_bug, triggered_by_user):
    """Create status file for Commander to see"""
    status = {
        "triggered_at": datetime.now().isoformat(),
        "triggered_by_bug": triggered_by_bug,
        "triggered_by_user": triggered_by_user,
        "status": "AUTOFIX ACTIVATED",
        "message": f"Bug #{triggered_by_bug} by {triggered_by_user} triggered AUTOFIX. Fetching all open bugs and starting autonomous fixes..."
    }

    with open('C:/Users/dwrek/Desktop/AUTOFIX_ACTIVATED.json', 'w') as f:
        json.dump(status, f, indent=2)

    print("=" * 60)
    print("🚨 AUTOFIX TRIGGERED!")
    print(f"   Triggered by: Bug #{triggered_by_bug} ({triggered_by_user})")
    print(f"   Time: {status['triggered_at']}")
    print("=" * 60)

def trigger_autonomous_fix():
    """Trigger Claude to fix all bugs"""
    bugs = fetch_bugs()

    # Save all open bugs for Claude to fix
    bug_list = []
    for bug in bugs:
        bug_list.append({
            "number": bug['number'],
            "title": bug['title'],
            "description": bug['body'],
            "reporter": bug['user']['login'],
            "created_at": bug['created_at']
        })

    # Save to file for Claude
    with open('C:/Users/dwrek/Desktop/BUGS_TO_FIX_NOW.json', 'w') as f:
        json.dump({
            "total_bugs": len(bug_list),
            "bugs": bug_list,
            "instructions": "Fix all these bugs autonomously. Prioritize by date (oldest first). Deploy after each fix."
        }, f, indent=2)

    print(f"✅ Found {len(bug_list)} open bugs")
    print(f"📋 Bug list saved to: C:/Users/dwrek/Desktop/BUGS_TO_FIX_NOW.json")
    print("\n🤖 Claude should now review and fix all bugs!")

if __name__ == "__main__":
    print("🔍 AUTOFIX TRIGGER MONITOR")
    print("=" * 60)
    print("Monitoring bugs for AUTOFIX trigger words:")
    print("  - AUTOFIX")
    print("  - FIX_ALL_BUGS")
    print("  - AUTO_FIX_NOW")
    print("=" * 60)

    while True:
        triggered, bug_num, user = check_for_autofix_trigger()

        if triggered:
            create_status_file(bug_num, user)
            trigger_autonomous_fix()
            print("\n✅ AUTOFIX process complete!")
            print("   Check Desktop for BUGS_TO_FIX_NOW.json")
            break
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] No AUTOFIX trigger found. Checking again in {CHECK_INTERVAL}s...")
            time.sleep(CHECK_INTERVAL)
