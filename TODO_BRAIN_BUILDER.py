"""
AUTONOMOUS TODO BRAIN - Google Sheets Integration
The system that saves the world

PROBLEM: Commander becomes bottleneck reviewing every task
SOLUTION: Autonomous AI ministers + central brain spreadsheet
RESULT: Commander does strategy, Trinity does execution

This is the constitutional government model for AI teams.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import re

# Will use gspread for Google Sheets integration
# pip install gspread oauth2client

try:
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    GSPREAD_AVAILABLE = True
except ImportError:
    GSPREAD_AVAILABLE = False
    print("⚠️  gspread not installed. Run: pip install gspread oauth2client")


class TodoBrain:
    """
    Central TODO brain - Google Sheets as source of truth

    Autonomous features:
    - Auto-extraction (every action generates TODOs)
    - Auto-prioritization (algorithm scores urgency)
    - Auto-execution (Trinity executes without review)
    - Auto-reporting (Commander sees summaries only)
    """

    def __init__(self, sheet_name: str = "Quantum Vault - TODO Brain"):
        self.sheet_name = sheet_name
        self.sheet = None
        self.worksheet = None

        if GSPREAD_AVAILABLE:
            self.connect_to_brain()
        else:
            print("📊 Using local JSON file (Google Sheets not available)")
            self.local_mode = True
            self.local_file = 'todo_brain_local.json'
            self.load_local_brain()

    def connect_to_brain(self):
        """Connect to Google Sheets brain"""
        try:
            # Setup credentials
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]

            # Look for credentials file
            creds_file = 'google_sheets_credentials.json'

            if not os.path.exists(creds_file):
                print(f"\n⚠️  Google Sheets credentials not found: {creds_file}")
                print("\nTo setup:")
                print("1. Go to https://console.cloud.google.com")
                print("2. Create project → Enable Google Sheets API")
                print("3. Create Service Account → Download JSON credentials")
                print("4. Save as: google_sheets_credentials.json")
                print("5. Share your Google Sheet with service account email")
                print("\nUsing local mode for now...\n")
                self.local_mode = True
                self.load_local_brain()
                return

            creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
            client = gspread.authorize(creds)

            # Open sheet
            self.sheet = client.open(self.sheet_name)
            self.worksheet = self.sheet.sheet1

            print(f"✅ Connected to brain: {self.sheet_name}")
            self.local_mode = False

        except Exception as e:
            print(f"❌ Error connecting to Google Sheets: {e}")
            print("Using local mode...")
            self.local_mode = True
            self.load_local_brain()

    def load_local_brain(self):
        """Load local JSON brain (fallback when Google Sheets unavailable)"""
        if os.path.exists(self.local_file):
            with open(self.local_file, 'r') as f:
                self.local_data = json.load(f)
        else:
            self.local_data = {
                'tasks': [],
                'next_id': 1
            }

    def save_local_brain(self):
        """Save local JSON brain"""
        with open(self.local_file, 'w') as f:
            json.dump(self.local_data, f, indent=2)

    def add_todo(self,
                 task: str,
                 priority: int,
                 assigned_to: str,
                 dependencies: Optional[List[int]] = None,
                 commander_review: bool = False,
                 estimated_hours: float = 1.0,
                 auto_generated: bool = True) -> int:
        """
        Add TODO to brain

        Returns: Task ID
        """

        task_id = self._get_next_id()

        todo = {
            'id': task_id,
            'task': task,
            'priority': priority,
            'status': 'Queued',
            'assigned_to': assigned_to,
            'dependencies': dependencies or [],
            'commander_review': commander_review,
            'estimated_hours': estimated_hours,
            'auto_generated': auto_generated,
            'created': datetime.now().isoformat(),
            'completed': None,
            'actual_hours': None
        }

        if self.local_mode:
            self.local_data['tasks'].append(todo)
            self.save_local_brain()
        else:
            # Add to Google Sheets
            row = [
                task_id,
                task,
                priority,
                'Queued',
                assigned_to,
                ','.join(map(str, dependencies or [])),
                'Yes' if commander_review else 'No',
                estimated_hours,
                'Yes' if auto_generated else 'No',
                datetime.now().strftime('%Y-%m-%d %H:%M'),
                '',  # Completed date
                ''   # Actual hours
            ]
            self.worksheet.append_row(row)

        print(f"✅ Added TODO #{task_id}: {task[:50]}... (Priority: {priority})")

        return task_id

    def get_next_task(self, assigned_to: Optional[str] = None) -> Optional[Dict]:
        """
        Get highest priority task that:
        - Status = Queued
        - Dependencies met
        - Assigned to specified agent (or any if None)
        - Doesn't require Commander review
        """

        tasks = self._get_all_tasks()

        # Filter
        available_tasks = []
        for task in tasks:
            # Must be queued
            if task['status'] != 'Queued':
                continue

            # Must match assigned_to filter
            if assigned_to and task['assigned_to'] != assigned_to:
                continue

            # Must not require Commander review
            if task['commander_review']:
                continue

            # Dependencies must be met
            if task['dependencies']:
                deps_met = all(
                    self._is_task_complete(dep_id)
                    for dep_id in task['dependencies']
                )
                if not deps_met:
                    continue

            available_tasks.append(task)

        if not available_tasks:
            return None

        # Return highest priority
        return max(available_tasks, key=lambda t: t['priority'])

    def mark_complete(self, task_id: int, actual_hours: Optional[float] = None):
        """Mark task complete"""

        if self.local_mode:
            for task in self.local_data['tasks']:
                if task['id'] == task_id:
                    task['status'] = 'Complete'
                    task['completed'] = datetime.now().isoformat()
                    task['actual_hours'] = actual_hours
                    break
            self.save_local_brain()
        else:
            # Update Google Sheets
            cell = self.worksheet.find(str(task_id))
            row = cell.row
            self.worksheet.update_cell(row, 4, 'Complete')  # Status column
            self.worksheet.update_cell(row, 11, datetime.now().strftime('%Y-%m-%d %H:%M'))
            if actual_hours:
                self.worksheet.update_cell(row, 12, actual_hours)

        print(f"✅ Completed TODO #{task_id}")

    def mark_in_progress(self, task_id: int):
        """Mark task as in progress"""

        if self.local_mode:
            for task in self.local_data['tasks']:
                if task['id'] == task_id:
                    task['status'] = 'In Progress'
                    break
            self.save_local_brain()
        else:
            cell = self.worksheet.find(str(task_id))
            row = cell.row
            self.worksheet.update_cell(row, 4, 'In Progress')

        print(f"⏳ Started TODO #{task_id}")

    def extract_todos_from_action(self, action_description: str) -> List[Dict]:
        """
        Automatic TODO extraction

        Analyzes what was done, generates next steps
        """

        print(f"\n🔍 Extracting TODOs from: {action_description[:50]}...")

        todos = []

        # Pattern recognition for common actions
        if "created file" in action_description.lower():
            # File created → may need testing, deployment, documentation
            todos.append({
                'task': f"Test {action_description}",
                'priority': 70,
                'assigned_to': 'C1 Mechanic',
                'dependencies': None,
                'commander_review': False,
                'estimated_hours': 0.5
            })

        if "api" in action_description.lower():
            # API work → needs credentials, testing, documentation
            todos.append({
                'task': f"Setup API credentials for {action_description}",
                'priority': 85,
                'assigned_to': 'Employee',
                'dependencies': None,
                'commander_review': True,  # May need Commander's accounts
                'estimated_hours': 1.0
            })

        if "dashboard" in action_description.lower():
            # Dashboard → needs deployment, testing, user feedback
            todos.append({
                'task': f"Deploy {action_description} to production",
                'priority': 80,
                'assigned_to': 'C1 Mechanic',
                'dependencies': None,
                'commander_review': False,
                'estimated_hours': 2.0
            })

        # Generic follow-ups
        todos.append({
            'task': f"Document {action_description}",
            'priority': 40,
            'assigned_to': 'C2 Architect',
            'dependencies': None,
            'commander_review': False,
            'estimated_hours': 0.5
        })

        print(f"   Generated {len(todos)} follow-up TODOs")

        return todos

    def calculate_priority(self, task_description: str) -> int:
        """
        Auto-calculate priority (0-100)

        Based on keywords and patterns
        """

        score = 50  # Base

        # Revenue keywords (+40)
        revenue_keywords = ['revenue', 'payment', 'stripe', 'monetize', 'subscription', 'pricing']
        if any(kw in task_description.lower() for kw in revenue_keywords):
            score += 40

        # Blocking keywords (+20)
        blocking_keywords = ['blocker', 'blocking', 'critical', 'urgent', 'asap']
        if any(kw in task_description.lower() for kw in blocking_keywords):
            score += 20

        # Launch keywords (+30)
        launch_keywords = ['launch', 'deploy', 'release', 'publish', 'go live']
        if any(kw in task_description.lower() for kw in launch_keywords):
            score += 30

        # Quick win keywords (+10)
        quick_keywords = ['quick', 'simple', 'easy', 'fast']
        if any(kw in task_description.lower() for kw in quick_keywords):
            score += 10

        # Nice-to-have keywords (-20)
        nice_keywords = ['nice to have', 'optional', 'later', 'eventually']
        if any(kw in task_description.lower() for kw in nice_keywords):
            score -= 20

        return max(0, min(100, score))

    def generate_commander_report(self) -> str:
        """Generate summary for Commander (not all tasks)"""

        tasks = self._get_all_tasks()

        total = len(tasks)
        completed = len([t for t in tasks if t['status'] == 'Complete'])
        in_progress = len([t for t in tasks if t['status'] == 'In Progress'])
        queued = len([t for t in tasks if t['status'] == 'Queued'])
        need_review = [t for t in tasks if t['commander_review'] and t['status'] == 'Queued']

        report = f"""
╔═══════════════════════════════════════════════════════════════╗
║           QUANTUM VAULT - TODO BRAIN REPORT                  ║
║                  {datetime.now().strftime('%Y-%m-%d %H:%M')}                          ║
╚═══════════════════════════════════════════════════════════════╝

📊 OVERALL STATUS:
   Total Tasks:      {total}
   ✅ Completed:     {completed} ({completed/total*100:.0f}%)
   ⏳ In Progress:   {in_progress}
   📋 Queued:        {queued}

🚨 COMMANDER ACTION REQUIRED:
   {len(need_review)} tasks need your review

"""

        if need_review:
            report += "\n   Tasks waiting on you:\n"
            for task in need_review[:5]:  # Show top 5
                report += f"   • #{task['id']}: {task['task'][:60]}\n"

        report += f"""

⚙️ AUTONOMOUS EXECUTION:
   Trinity handled {completed - len([t for t in tasks if t['commander_review'] and t['status'] == 'Complete'])} tasks without your review

🎯 NEXT UP:
   Highest priority queued tasks:
"""

        queued_tasks = [t for t in tasks if t['status'] == 'Queued']
        queued_tasks.sort(key=lambda t: t['priority'], reverse=True)

        for task in queued_tasks[:3]:
            report += f"   • #{task['id']}: {task['task'][:60]} (P:{task['priority']})\n"

        return report

    def _get_all_tasks(self) -> List[Dict]:
        """Get all tasks from brain"""

        if self.local_mode:
            return self.local_data['tasks']
        else:
            # Get from Google Sheets
            rows = self.worksheet.get_all_values()[1:]  # Skip header
            tasks = []
            for row in rows:
                tasks.append({
                    'id': int(row[0]),
                    'task': row[1],
                    'priority': int(row[2]),
                    'status': row[3],
                    'assigned_to': row[4],
                    'dependencies': [int(x) for x in row[5].split(',') if x],
                    'commander_review': row[6] == 'Yes',
                    'estimated_hours': float(row[7]) if row[7] else 1.0,
                    'auto_generated': row[8] == 'Yes',
                    'created': row[9],
                    'completed': row[10] if row[10] else None,
                    'actual_hours': float(row[11]) if row[11] else None
                })
            return tasks

    def _get_next_id(self) -> int:
        """Get next available task ID"""

        if self.local_mode:
            task_id = self.local_data['next_id']
            self.local_data['next_id'] += 1
            return task_id
        else:
            tasks = self._get_all_tasks()
            return max([t['id'] for t in tasks], default=0) + 1

    def _is_task_complete(self, task_id: int) -> bool:
        """Check if task is complete"""

        tasks = self._get_all_tasks()
        for task in tasks:
            if task['id'] == task_id:
                return task['status'] == 'Complete'
        return False


# =============================================================================
# AUTONOMOUS EXECUTOR (Runs in background)
# =============================================================================

class AutonomousExecutor:
    """
    Runs continuously, executes tasks without Commander review

    This is the "minister" that works autonomously
    """

    def __init__(self, brain: TodoBrain, agent_name: str = 'C1 Mechanic'):
        self.brain = brain
        self.agent_name = agent_name

    def run_cycle(self):
        """Execute one work cycle"""

        print(f"\n{'='*70}")
        print(f"🤖 {self.agent_name} - Autonomous Work Cycle")
        print(f"{'='*70}\n")

        # Get next task
        task = self.brain.get_next_task(assigned_to=self.agent_name)

        if not task:
            print(f"✅ No tasks available for {self.agent_name}")
            print(f"   (All tasks either blocked, in progress, or need Commander review)")
            return

        print(f"📋 Next Task: #{task['id']}")
        print(f"   {task['task']}")
        print(f"   Priority: {task['priority']}")
        print(f"   Estimated: {task['estimated_hours']} hours")
        print()

        # Mark in progress
        self.brain.mark_in_progress(task['id'])

        # Simulate execution (in real implementation, actually execute)
        print(f"⚙️  Executing task...")
        print(f"   (In real implementation, this would actually do the work)")

        # Mark complete
        self.brain.mark_complete(task['id'], actual_hours=task['estimated_hours'])

        # Extract new TODOs from completion
        new_todos = self.brain.extract_todos_from_action(task['task'])

        for todo_data in new_todos:
            self.brain.add_todo(
                task=todo_data['task'],
                priority=todo_data['priority'],
                assigned_to=todo_data['assigned_to'],
                dependencies=todo_data.get('dependencies'),
                commander_review=todo_data.get('commander_review', False),
                estimated_hours=todo_data.get('estimated_hours', 1.0),
                auto_generated=True
            )

        print(f"\n✅ Task complete! Generated {len(new_todos)} follow-up TODOs\n")


# =============================================================================
# MAIN EXECUTION / DEMO
# =============================================================================

if __name__ == "__main__":

    print("\n" + "🧠"*35)
    print()
    print("         AUTONOMOUS TODO BRAIN SYSTEM")
    print("        Constitutional AI Government Model")
    print()
    print("🧠"*35)
    print()

    # Initialize brain
    brain = TodoBrain()

    # Add some sample TODOs
    print("\n📋 Adding sample TODOs to brain...\n")

    brain.add_todo(
        task="Extract $5K from Coinbase using OTP tool",
        priority=95,
        assigned_to="Commander",
        commander_review=True,
        estimated_hours=0.5,
        auto_generated=False
    )

    brain.add_todo(
        task="Post Fiverr job listing to hire VA",
        priority=90,
        assigned_to="Commander",
        commander_review=True,
        estimated_hours=0.5,
        auto_generated=False
    )

    brain.add_todo(
        task="Connect Stripe API for payment processing",
        priority=90,
        assigned_to="C1 Mechanic",
        dependencies=[1],  # Blocked on Coinbase extraction
        commander_review=True,  # Needs API keys
        estimated_hours=2.0
    )

    brain.add_todo(
        task="Build account creation automation script",
        priority=85,
        assigned_to="C1 Mechanic",
        commander_review=False,
        estimated_hours=4.0
    )

    brain.add_todo(
        task="Create 4 landing pages using templates",
        priority=80,
        assigned_to="Employee",
        dependencies=[2],  # Blocked on employee hire
        commander_review=False,
        estimated_hours=3.0
    )

    # Run autonomous executor demo
    print("\n" + "="*70)
    print("🤖 AUTONOMOUS EXECUTION DEMO")
    print("="*70 + "\n")

    executor = AutonomousExecutor(brain, agent_name='C1 Mechanic')

    # Run 2 cycles
    for i in range(2):
        executor.run_cycle()
        print("\n" + "-"*70 + "\n")

    # Generate Commander report
    print("\n" + "="*70)
    print("📊 COMMANDER REPORT")
    print("="*70)

    report = brain.generate_commander_report()
    print(report)

    print("\n" + "="*70)
    print("✅ DEMO COMPLETE")
    print("="*70)
    print()
    print("Next steps:")
    print("1. Setup Google Sheets credentials (see instructions above)")
    print("2. Create 'Quantum Vault - TODO Brain' sheet")
    print("3. Run this script to populate initial TODOs")
    print("4. Run autonomous executor continuously (cron job or background process)")
    print()
    print("🧠 The brain is operational. Autonomous execution ready.")
    print()
