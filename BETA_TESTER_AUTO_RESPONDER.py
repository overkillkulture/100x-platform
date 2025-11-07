"""
🎯 BETA TESTER AUTO-RESPONDER
Monitors bug submissions, responds automatically, updates leaderboard
"""

import json
import os
import time
from datetime import datetime
import requests

TRACKER_FILE = "C:/Users/dwrek/100X_DEPLOYMENT/BETA_TESTER_DEDICATION_TRACKER.json"
GITHUB_API = "https://api.github.com/repos/overkillkulture/consciousness-bugs/issues"
LAST_CHECK_FILE = "C:/Users/dwrek/100X_DEPLOYMENT/.beta_auto_responder_last_check.txt"

# Beta tester PINs mapped to GitHub usernames (when we get them)
BETA_TESTER_MAP = {
    1001: "joshua.serrano2022@gmail.com",
    1002: "tobyburrowes@gmail.com",
    1003: "wdbrotherton@gmail.com",
    1004: "deansabrwork@outlook.com",
    1005: "varniwilliam@gmail.com",
    1006: "ruuutherford@gmail.com",
    1007: "Contact info pending",
    1008: "Contact info pending",
    1009: "Contact info pending"
}

def load_tracker():
    """Load beta tester tracker"""
    with open(TRACKER_FILE, 'r') as f:
        return json.load(f)

def save_tracker(data):
    """Save beta tester tracker"""
    with open(TRACKER_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_last_check_time():
    """Get last check timestamp"""
    if os.path.exists(LAST_CHECK_FILE):
        with open(LAST_CHECK_FILE, 'r') as f:
            return f.read().strip()
    return "2025-11-01T00:00:00Z"  # Default start time

def save_last_check_time(timestamp):
    """Save last check timestamp"""
    with open(LAST_CHECK_FILE, 'w') as f:
        f.write(timestamp)

def check_new_bugs():
    """Check GitHub for new bug submissions"""
    try:
        last_check = get_last_check_time()

        # Fetch recent issues
        response = requests.get(
            GITHUB_API,
            params={"state": "all", "since": last_check}
        )

        if response.status_code == 200:
            issues = response.json()
            return issues
        else:
            print(f"GitHub API error: {response.status_code}")
            return []

    except Exception as e:
        print(f"Error checking bugs: {e}")
        return []

def identify_beta_tester(issue):
    """Try to identify which beta tester submitted this bug"""
    # Check issue body for PIN or email
    body = issue.get('body', '').lower()

    for pin, contact in BETA_TESTER_MAP.items():
        if str(pin) in body or contact.lower() in body:
            return pin

    # Check GitHub username (if we have that mapping)
    return None

def award_points_for_bug(pin, bug_number):
    """Award points to beta tester for bug submission"""
    tracker = load_tracker()

    for tester in tracker['beta_testers']:
        if tester['pin'] == pin:
            task = tester['tasks']['task_1_bugs']

            # Add bug if not already recorded
            if bug_number not in task['bug_ids']:
                task['bug_ids'].append(bug_number)
                task['bugs_submitted'] = len(task['bug_ids'])

                # Check if task completed
                if task['bugs_submitted'] >= task['bugs_required']:
                    task['completed'] = True
                    task['points_earned'] = task['points_possible']

                # Recalculate total points
                tester['total_points'] = calculate_total_points(tester)
                tester['tier'], tester['tier_badge'] = assign_tier(tester['total_points'])

                save_tracker(tracker)

                print(f"✅ Awarded points to PIN {pin} for Bug #{bug_number}")
                print(f"   Progress: {task['bugs_submitted']}/{task['bugs_required']} bugs")
                print(f"   Total points: {tester['total_points']}")
                print(f"   Tier: {tester['tier']} {tester['tier_badge']}")

                return True

    return False

def calculate_total_points(tester):
    """Calculate total points from all tasks"""
    total = 0
    for task_key, task_data in tester['tasks'].items():
        total += task_data.get('points_earned', 0)
    return total

def assign_tier(points):
    """Assign tier based on points"""
    if points >= 70:
        return ("INSIDER", "🥇")
    elif points >= 40:
        return ("ACTIVE", "🥈")
    elif points >= 10:
        return ("CASUAL", "🥉")
    else:
        return ("INACTIVE", "⛔")

def respond_to_bug(issue_number, pin):
    """Post automatic response to bug (if we have GitHub token)"""
    # This would post a comment via GitHub API
    # For now, just log it
    print(f"📝 Would respond to Bug #{issue_number} for PIN {pin}")
    print(f"   Message: 'Thanks for the bug report! Points awarded. Check the leaderboard!'")

def auto_responder_cycle():
    """Main auto-responder cycle"""
    print("="*60)
    print("🎯 BETA TESTER AUTO-RESPONDER")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)

    # Check for new bugs
    new_bugs = check_new_bugs()

    if new_bugs:
        print(f"\n📊 Found {len(new_bugs)} issues since last check")

        for issue in new_bugs:
            bug_number = issue['number']
            title = issue['title']

            print(f"\nBug #{bug_number}: {title}")

            # Try to identify beta tester
            pin = identify_beta_tester(issue)

            if pin:
                print(f"✅ Identified: PIN {pin}")
                # Award points
                if award_points_for_bug(pin, bug_number):
                    # Respond to bug
                    respond_to_bug(bug_number, pin)
            else:
                print(f"⚠️ Could not identify beta tester (might be external report)")
    else:
        print("\n📊 No new issues found")

    # Save current time as last check
    save_last_check_time(datetime.utcnow().isoformat() + "Z")

    print("\n" + "="*60)

if __name__ == '__main__':
    try:
        while True:
            auto_responder_cycle()
            print("\n⏰ Next check in 5 minutes...")
            time.sleep(300)  # Check every 5 minutes
    except KeyboardInterrupt:
        print("\n\n🛑 Auto-responder stopped")
