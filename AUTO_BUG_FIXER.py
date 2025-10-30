#!/usr/bin/env python3
"""
AUTO BUG FIXER - Autonomous Bug Monitoring and Fixing System

Monitors bugs-live.html data and automatically works on new bugs.
Creates task files for Claude to pick up and implement.
"""

import requests
import json
import time
import os
from datetime import datetime
from pathlib import Path

# Configuration
BUGS_API = "https://conciousnessrevolution.io/.netlify/functions/get-all-bugs"
TASK_DIR = Path("C:/Users/dwrek/100X_DEPLOYMENT/.bug_tasks")
PROCESSED_FILE = Path("C:/Users/dwrek/100X_DEPLOYMENT/.processed_bugs.json")
CHECK_INTERVAL = 5  # seconds
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")

# Create task directory
TASK_DIR.mkdir(exist_ok=True)

def load_processed_bugs():
    """Load list of already processed bug numbers"""
    if PROCESSED_FILE.exists():
        with open(PROCESSED_FILE, 'r') as f:
            return set(json.load(f))
    return set()

def save_processed_bugs(processed):
    """Save list of processed bug numbers"""
    with open(PROCESSED_FILE, 'w') as f:
        json.dump(list(processed), f)

def fetch_bugs():
    """Fetch current bugs from API"""
    try:
        response = requests.get(BUGS_API, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[ERROR] Failed to fetch bugs: {e}")
        return []

def create_task_file(bug):
    """Create a task file for Claude to pick up"""
    task_file = TASK_DIR / f"bug_{bug['number']}.json"

    task = {
        "bug_number": bug['number'],
        "title": bug['title'],
        "reporter": bug['user']['login'],
        "description": bug['body'],
        "created_at": bug['created_at'],
        "status": "pending",
        "task_created": datetime.now().isoformat()
    }

    with open(task_file, 'w') as f:
        json.dump(task, f, indent=2)

    print(f"[TASK CREATED] Bug #{bug['number']}: {bug['title'][:50]}")
    return task_file

def post_github_comment(bug_number, comment):
    """Post a comment on the GitHub issue"""
    if not GITHUB_TOKEN:
        print("[WARNING] No GitHub token - skipping comment")
        return False

    url = f"https://api.github.com/repos/overkillkulture/consciousness-bugs/issues/{bug_number}/comments"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    try:
        response = requests.post(url, headers=headers, json={"body": comment})
        response.raise_for_status()
        print(f"[GITHUB] Comment posted on bug #{bug_number}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to post comment: {e}")
        return False

def close_github_issue(bug_number):
    """Close a GitHub issue"""
    if not GITHUB_TOKEN:
        print("[WARNING] No GitHub token - skipping close")
        return False

    url = f"https://api.github.com/repos/overkillkulture/consciousness-bugs/issues/{bug_number}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    try:
        response = requests.patch(url, headers=headers, json={"state": "closed"})
        response.raise_for_status()
        print(f"[GITHUB] Bug #{bug_number} closed")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to close issue: {e}")
        return False

def monitor_bugs():
    """Main monitoring loop"""
    print("="*60)
    print("AUTO BUG FIXER - Starting...")
    print("="*60)
    print(f"Monitoring: {BUGS_API}")
    print(f"Check interval: {CHECK_INTERVAL} seconds")
    print(f"Task directory: {TASK_DIR}")
    print()

    processed = load_processed_bugs()
    print(f"Already processed: {len(processed)} bugs")

    iteration = 0

    while True:
        iteration += 1
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Check #{iteration}")

        # Fetch current bugs
        bugs = fetch_bugs()
        if not bugs:
            print("No bugs fetched, retrying...")
            time.sleep(CHECK_INTERVAL)
            continue

        # Filter for open bugs we haven't processed
        open_bugs = [b for b in bugs if b['state'] == 'open']
        new_bugs = [b for b in open_bugs if b['number'] not in processed]

        print(f"Total bugs: {len(bugs)} | Open: {len(open_bugs)} | New: {len(new_bugs)}")

        # Create tasks for new bugs
        for bug in new_bugs:
            create_task_file(bug)
            processed.add(bug['number'])

        # Save processed list
        if new_bugs:
            save_processed_bugs(processed)

        # Check for completed tasks and close bugs
        for task_file in TASK_DIR.glob("bug_*.json"):
            with open(task_file, 'r') as f:
                task = json.load(f)

            if task['status'] == 'completed':
                bug_num = task['bug_number']

                # Post completion comment
                comment = f"""## ✅ Bug Fixed

**What was done:**
{task.get('fix_description', 'Bug has been resolved')}

**Changes made:**
{task.get('changes_made', 'See deployment logs')}

**Deployed:** {task.get('deployment_url', 'https://conciousnessrevolution.io')}

**Status:** Fixed and live ✅

---
🤖 Auto-fixed by Claude Code Bug Fixer
"""
                post_github_comment(bug_num, comment)

                # Close the issue
                close_github_issue(bug_num)

                # Archive the task
                archive_file = TASK_DIR / f"COMPLETED_bug_{bug_num}.json"
                task_file.rename(archive_file)
                print(f"[ARCHIVED] Bug #{bug_num} → {archive_file.name}")

        # Wait for next check
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    try:
        monitor_bugs()
    except KeyboardInterrupt:
        print("\n\n[STOPPED] Auto Bug Fixer stopped by user")
    except Exception as e:
        print(f"\n\n[FATAL ERROR] {e}")
        raise
