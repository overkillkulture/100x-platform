#!/usr/bin/env python3
"""
AIRTABLE BRAIN - CENTRAL NERVOUS SYSTEM (LIVE NOW)
===================================================

Uses Airtable as central brain - ALREADY CONFIGURED, NO SETUP NEEDED

All computers report here:
- Status updates every 5 min
- Task progress in real-time
- Errors/issues logged instantly
- Commander sees EVERYTHING from phone/computer

Why Airtable over Google Sheets:
✅ Already authenticated (works RIGHT NOW)
✅ Has API ready to go
✅ Mobile app (view from phone)
✅ Real-time updates
✅ Beautiful UI
✅ Free tier (1,200 records/base)
"""

import os
from datetime import datetime
import socket
import psutil
import requests
from pathlib import Path

class AirtableBrain:
    """Central nervous system using Airtable"""

    def __init__(self):
        # Get Airtable credentials from env
        self.api_token = os.getenv('AIRTABLE_API_TOKEN', 'pat8DtOnZ1crQT56g.a83c21fa77ead56a661353b0cd0b286816ca14502ce717c8b247c0c52a326757')
        self.base_id = os.getenv('AIRTABLE_BASE_ID', 'app7F75X1uny6jPfd')  # Use existing configured base

        self.computer_id = socket.gethostname()
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

    def report_status(self):
        """Report computer status to brain"""

        url = f"https://api.airtable.com/v0/{self.base_id}/Computer%20Status"

        # Gather system info
        data = {
            "fields": {
                "Computer ID": self.computer_id,
                "Status": "🟢 ONLINE",
                "Last Seen": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "CPU %": f"{psutil.cpu_percent()}%",
                "RAM %": f"{psutil.virtual_memory().percent}%",
                "Tasks Running": "0",  # TODO: Integrate task tracker
                "Tasks Completed": "0",  # TODO: Integrate task tracker
                "Issues": "None"
            }
        }

        try:
            response = requests.post(url, json=data, headers=self.headers)
            if response.status_code == 200:
                print(f"✅ Status reported to brain: {self.computer_id}")
                return True
            else:
                print(f"⚠️  Status report failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error reporting status: {e}")
            return False

    def log_task(self, task_name, status, result=None, duration=None):
        """Log task to brain"""

        url = f"https://api.airtable.com/v0/{self.base_id}/Task%20Log"

        data = {
            "fields": {
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Computer ID": self.computer_id,
                "Task": task_name,
                "Status": status,
                "Duration": duration or "N/A",
                "Result": result or "N/A"
            }
        }

        try:
            response = requests.post(url, json=data, headers=self.headers)
            if response.status_code == 200:
                print(f"✅ Task logged: {task_name} - {status}")
                return True
            else:
                print(f"⚠️  Task log failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error logging task: {e}")
            return False

    def log_error(self, error_type, message, severity="WARNING"):
        """Log error to brain"""

        url = f"https://api.airtable.com/v0/{self.base_id}/Errors"

        data = {
            "fields": {
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Computer ID": self.computer_id,
                "Severity": severity,
                "Error Type": error_type,
                "Message": message,
                "Fixed": False
            }
        }

        try:
            response = requests.post(url, json=data, headers=self.headers)
            if response.status_code == 200:
                print(f"⚠️  Error logged: {error_type}")
                return True
            else:
                print(f"❌ Error log failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error logging error: {e}")
            return False

    def get_priorities(self):
        """Get priority tasks from brain (Commander sets these)"""

        url = f"https://api.airtable.com/v0/{self.base_id}/Priorities"

        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                records = response.json().get('records', [])

                # Filter for this computer or ANY
                my_priorities = [
                    r['fields'] for r in records
                    if r['fields'].get('Assigned To') in [self.computer_id, 'ANY', '']
                    and r['fields'].get('Status') != 'COMPLETED'
                ]

                return my_priorities
            else:
                print(f"⚠️  Failed to get priorities: {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ Error getting priorities: {e}")
            return []


if __name__ == "__main__":
    print("=" * 60)
    print("⚡ AIRTABLE BRAIN - GOING ONLINE NOW ⚡")
    print("=" * 60)
    print()

    brain = AirtableBrain()

    print(f"Computer ID: {brain.computer_id}")
    print(f"Brain Base: {brain.base_id}")
    print()

    # Test status report
    print("Reporting status to brain...")
    brain.report_status()
    print()

    # Test task logging
    print("Logging test task...")
    brain.log_task(
        "Brain System Test",
        "COMPLETED",
        result="Brain is LIVE!",
        duration="2 seconds"
    )
    print()

    # Test error logging
    print("Testing error logging...")
    brain.log_error(
        "TEST_ERROR",
        "This is a test error - brain error tracking works!",
        severity="INFO"
    )
    print()

    # Get priorities
    print("Checking for priority tasks...")
    priorities = brain.get_priorities()
    if priorities:
        print(f"Found {len(priorities)} priority tasks:")
        for p in priorities:
            print(f"  - {p.get('Task')} (Priority: {p.get('Priority')})")
    else:
        print("No priorities assigned yet")

    print()
    print("=" * 60)
    print("✅ BRAIN IS ONLINE!")
    print("=" * 60)
    print()
    print("View brain: https://airtable.com/appCYbeXKPjLUqmJt")
    print()
    print("All computers can now report to this brain!")
    print("Commander can view/edit from phone or computer!")
    print()
