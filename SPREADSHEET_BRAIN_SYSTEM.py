#!/usr/bin/env python3
"""
SPREADSHEET BRAIN - CENTRAL NERVOUS SYSTEM
===========================================

Google Sheets as the source of truth for all computers.

ALL computers report here:
- Status updates
- Task progress
- Errors/issues
- Completed work
- Resource usage

Commander sees EVERYTHING in one spreadsheet.
"""

import gspread
from google.oauth2.service_account import Credentials
import socket
import platform
import psutil
from datetime import datetime
import json
from pathlib import Path
import os
import sys

class SpreadsheetBrain:
    """Central nervous system - all computers report here"""

    def __init__(self, spreadsheet_url=None):
        """
        Initialize connection to Google Sheets brain

        Args:
            spreadsheet_url: URL to the master spreadsheet
                           If None, will create new spreadsheet
        """
        self.computer_id = socket.gethostname()
        self.spreadsheet_url = spreadsheet_url

        # Try to authenticate
        self.client = self.authenticate()
        self.sheet = None

        if self.client and spreadsheet_url:
            self.connect_to_brain()

    def authenticate(self):
        """Authenticate with Google Sheets using service account or OAuth"""

        # Method 1: Try service account (if credentials file exists)
        creds_file = Path("C:/Users/dwrek/.consciousness/google_credentials.json")
        if creds_file.exists():
            try:
                scopes = [
                    'https://www.googleapis.com/auth/spreadsheets',
                    'https://www.googleapis.com/auth/drive'
                ]
                creds = Credentials.from_service_account_file(str(creds_file), scopes=scopes)
                return gspread.authorize(creds)
            except Exception as e:
                print(f"⚠️  Service account auth failed: {e}")

        # Method 2: Use OAuth (simpler for personal use)
        print("📝 Google Sheets authentication needed")
        print("   Follow instructions at: https://docs.gspread.org/en/latest/oauth2.html")
        print("   Or use Airtable as backup (already configured)")
        return None

    def connect_to_brain(self):
        """Connect to existing spreadsheet brain"""
        if not self.client:
            return False

        try:
            self.sheet = self.client.open_by_url(self.spreadsheet_url)
            print(f"✅ Connected to Spreadsheet Brain: {self.sheet.title}")
            return True
        except Exception as e:
            print(f"❌ Failed to connect: {e}")
            return False

    def create_brain(self, title="Consciousness Revolution - Master Brain"):
        """Create new spreadsheet brain with proper structure"""
        if not self.client:
            print("❌ Can't create brain - authentication needed")
            return None

        try:
            # Create spreadsheet
            sheet = self.client.create(title)
            self.sheet = sheet

            # Share with yourself (make editable)
            sheet.share('darrick.preble@gmail.com', perm_type='user', role='writer')

            # Create worksheets
            self.setup_worksheets()

            print(f"✅ Brain created: {sheet.url}")
            return sheet.url

        except Exception as e:
            print(f"❌ Failed to create brain: {e}")
            return None

    def setup_worksheets(self):
        """Set up the brain structure"""
        if not self.sheet:
            return

        # Worksheet 1: Computer Status (real-time)
        status_sheet = self.sheet.sheet1
        status_sheet.update_title("Computer Status")
        status_sheet.update('A1:H1', [[
            'Computer ID', 'Status', 'Last Seen', 'CPU %', 'RAM %',
            'Tasks Running', 'Tasks Completed', 'Issues'
        ]])

        # Worksheet 2: Task Log (history)
        task_sheet = self.sheet.add_worksheet("Task Log", rows=1000, cols=10)
        task_sheet.update('A1:J1', [[
            'Timestamp', 'Computer ID', 'Task', 'Status', 'Duration',
            'Result', 'Errors', 'Files Created', 'Next Steps', 'Notes'
        ]])

        # Worksheet 3: Errors & Issues
        error_sheet = self.sheet.add_worksheet("Errors & Issues", rows=500, cols=8)
        error_sheet.update('A1:H1', [[
            'Timestamp', 'Computer ID', 'Severity', 'Error Type',
            'Message', 'Stack Trace', 'Fixed?', 'Fix Applied'
        ]])

        # Worksheet 4: Daily Summary
        summary_sheet = self.sheet.add_worksheet("Daily Summary", rows=365, cols=12)
        summary_sheet.update('A1:L1', [[
            'Date', 'Total Tasks', 'Completed', 'Failed', 'Errors',
            'Deployments', 'Commits', 'Files Created', 'CPU Avg',
            'RAM Avg', 'Uptime Hours', 'Notes'
        ]])

        # Worksheet 5: Priorities (Commander sets these)
        priority_sheet = self.sheet.add_worksheet("Priorities", rows=100, cols=6)
        priority_sheet.update('A1:F1', [[
            'Priority', 'Task', 'Assigned To', 'Deadline',
            'Status', 'Notes'
        ]])

        print("✅ Brain worksheets configured")

    def report_status(self):
        """Report current computer status to brain"""
        if not self.sheet:
            print("⚠️  Not connected to brain - can't report")
            return False

        try:
            status_sheet = self.sheet.worksheet("Computer Status")

            # Gather system info
            status_data = [
                self.computer_id,
                "🟢 ONLINE",
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                f"{psutil.cpu_percent()}%",
                f"{psutil.virtual_memory().percent}%",
                self.get_running_tasks(),
                self.get_completed_tasks(),
                self.get_current_issues()
            ]

            # Find row for this computer or append new
            all_values = status_sheet.get_all_values()
            computer_row = None

            for i, row in enumerate(all_values[1:], start=2):  # Skip header
                if row[0] == self.computer_id:
                    computer_row = i
                    break

            if computer_row:
                # Update existing row
                status_sheet.update(f'A{computer_row}:H{computer_row}', [status_data])
            else:
                # Append new row
                status_sheet.append_row(status_data)

            print(f"✅ Status reported to brain")
            return True

        except Exception as e:
            print(f"❌ Failed to report status: {e}")
            return False

    def log_task(self, task_name, status, result=None, duration=None, files_created=None):
        """Log task completion to brain"""
        if not self.sheet:
            return False

        try:
            task_sheet = self.sheet.worksheet("Task Log")

            task_data = [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                self.computer_id,
                task_name,
                status,
                duration or "N/A",
                result or "N/A",
                "",  # Errors
                files_created or "N/A",
                "",  # Next steps
                ""   # Notes
            ]

            task_sheet.append_row(task_data)
            print(f"✅ Task logged: {task_name} - {status}")
            return True

        except Exception as e:
            print(f"❌ Failed to log task: {e}")
            return False

    def log_error(self, error_type, message, severity="WARNING", stack_trace=None):
        """Log error to brain"""
        if not self.sheet:
            return False

        try:
            error_sheet = self.sheet.worksheet("Errors & Issues")

            error_data = [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                self.computer_id,
                severity,
                error_type,
                message,
                stack_trace or "N/A",
                "❌ No",  # Fixed?
                ""        # Fix applied
            ]

            error_sheet.append_row(error_data)
            print(f"⚠️  Error logged: {error_type} - {message}")
            return True

        except Exception as e:
            print(f"❌ Failed to log error: {e}")
            return False

    def get_priorities(self):
        """Get priority tasks assigned by Commander"""
        if not self.sheet:
            return []

        try:
            priority_sheet = self.sheet.worksheet("Priorities")
            priorities = priority_sheet.get_all_records()

            # Filter for this computer or unassigned
            my_priorities = [
                p for p in priorities
                if p['Assigned To'] in [self.computer_id, 'ANY', '']
                and p['Status'] != 'COMPLETED'
            ]

            return my_priorities

        except Exception as e:
            print(f"❌ Failed to get priorities: {e}")
            return []

    def get_running_tasks(self):
        """Count currently running tasks"""
        # TODO: Integrate with actual task tracker
        return "0"

    def get_completed_tasks(self):
        """Count completed tasks today"""
        # TODO: Integrate with actual task tracker
        return "0"

    def get_current_issues(self):
        """Get current issues/warnings"""
        # TODO: Integrate with actual error tracker
        return "None"


# ============================================================================
# COMMAND LINE INTERFACE
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("⚡ SPREADSHEET BRAIN - CENTRAL NERVOUS SYSTEM ⚡")
    print("=" * 60)
    print()

    brain = SpreadsheetBrain()

    if not brain.client:
        print("❌ Google Sheets authentication required")
        print()
        print("OPTION 1: Use Airtable (already set up)")
        print("   Airtable works the same way but is already configured")
        print()
        print("OPTION 2: Set up Google Sheets")
        print("   1. Go to: https://console.cloud.google.com/")
        print("   2. Create service account")
        print("   3. Download credentials JSON")
        print("   4. Save to: C:/Users/dwrek/.consciousness/google_credentials.json")
        print()
        print("For now, using local file-based brain...")
        print()

        # Fallback: Use local JSON file
        local_brain = Path("C:/Users/dwrek/.consciousness/local_brain.json")
        print(f"Local brain: {local_brain}")

        sys.exit(1)

    # Test: Create new brain
    print("Creating new Spreadsheet Brain...")
    url = brain.create_brain()

    if url:
        print()
        print("=" * 60)
        print("✅ SPREADSHEET BRAIN ONLINE!")
        print("=" * 60)
        print(f"\nURL: {url}")
        print()
        print("Save this URL - all computers will use it!")
        print()

        # Test reporting
        print("Testing status report...")
        brain.report_status()

        print()
        print("Testing task logging...")
        brain.log_task(
            "Test Task",
            "COMPLETED",
            result="Success",
            duration="5 seconds"
        )

        print()
        print("=" * 60)
        print("Brain is LIVE and ready for all computers!")
        print("=" * 60)
    else:
        print("❌ Failed to create brain")
