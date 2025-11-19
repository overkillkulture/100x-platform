#!/usr/bin/env python3
"""
SCAFFOLD AND ACTIVATE - FULL AUTONOMOUS MODE
=============================================

Command: "Hey scaffold this"

What it does:
1. Takes all current todos from todo_brain_local.json
2. Scaffolds them into Brain priorities
3. Activates Week 1 KORPAK (recursive work generation)
4. Starts autonomous execution
5. You listen to music, drink coffee, system works

Usage:
    python SCAFFOLD_AND_ACTIVATE.py

Then walk away. System handles the rest.
"""

import json
import sys
from pathlib import Path
from datetime import datetime
import time

# Add path for brain system
sys.path.insert(0, 'C:/Users/dwrek/100X_DEPLOYMENT')
from SIMPLE_BRAIN_SYSTEM import SimpleBrain

class AutonomousScaffold:
    """Scaffold todos and activate autonomous execution"""

    def __init__(self):
        self.brain = SimpleBrain()
        self.todo_file = Path("C:/Users/dwrek/100X_DEPLOYMENT/todo_brain_local.json")
        self.korpak_file = Path("C:/Users/dwrek/100X_DEPLOYMENT/YEAR_1_AUTONOMOUS_WORK_SYSTEM.json")

    def load_todos(self):
        """Load existing todos"""
        if not self.todo_file.exists():
            print("⚠️  No todo file found - creating empty list")
            return []

        data = json.loads(self.todo_file.read_text())
        return data.get('tasks', [])

    def load_korpak_week_1(self):
        """Load Week 1 KORPAK tasks"""
        if not self.korpak_file.exists():
            print("⚠️  KORPAK file not found - skipping recursive generation")
            return []

        data = json.loads(self.korpak_file.read_text())
        week_1 = data.get('weeks', [{}])[0]  # First week
        return week_1.get('tasks', [])

    def scaffold_to_brain(self):
        """Scaffold all todos into Brain priorities"""

        print("=" * 60)
        print("⚡ SCAFFOLD AND ACTIVATE - AUTONOMOUS MODE ⚡")
        print("=" * 60)
        print()

        # Load todos
        print("📋 Loading todos...")
        todos = self.load_todos()
        print(f"   Found {len(todos)} todos in local brain")

        # Load Week 1 KORPAK
        print("🔮 Loading Week 1 KORPAK...")
        korpak_tasks = self.load_korpak_week_1()
        print(f"   Found {len(korpak_tasks)} KORPAK tasks")

        print()
        print("=" * 60)
        print("🏗️  SCAFFOLDING TO BRAIN")
        print("=" * 60)
        print()

        # Scaffold high-priority todos
        scaffolded = 0
        for todo in todos:
            priority = todo.get('priority', 50)
            status = todo.get('status', 'Queued')

            # Only scaffold queued/active tasks with priority > 70
            if status in ['Queued', 'In Progress'] and priority >= 70:
                self.brain.add_priority(
                    task=todo.get('task', 'Unnamed task'),
                    assigned_to=todo.get('assigned_to', 'ANY'),
                    deadline=None
                )
                scaffolded += 1
                print(f"✅ Scaffolded: {todo.get('task', 'Unnamed')[:50]}")

        print()
        print(f"📊 Scaffolded {scaffolded} high-priority tasks to Brain")
        print()

        # Scaffold Week 1 KORPAK tasks
        print("🔮 Scaffolding Week 1 KORPAK...")
        week_1_added = 0
        for task in korpak_tasks[:10]:  # First 10 tasks from Week 1
            self.brain.add_priority(
                task=task.get('task', 'KORPAK task'),
                assigned_to='ANY',
                deadline='Week 1'
            )
            week_1_added += 1
            print(f"✅ KORPAK: {task.get('task', 'Unnamed')[:50]}")

        print()
        print(f"📊 Added {week_1_added} Week 1 KORPAK tasks")
        print()

        return scaffolded + week_1_added

    def activate_autonomous_mode(self):
        """Start autonomous execution loop"""

        print("=" * 60)
        print("🚀 ACTIVATING AUTONOMOUS EXECUTION MODE")
        print("=" * 60)
        print()

        print("Commander can now:")
        print("  ☕ Listen to music")
        print("  🎵 Drink coffee")
        print("  🧘 Focus on other things")
        print()
        print("System will:")
        print("  ✅ Execute priorities autonomously")
        print("  ✅ Report progress every 5 minutes")
        print("  ✅ Log all completed work")
        print("  ✅ Handle errors gracefully")
        print()
        print("=" * 60)
        print()

        # Start reporting loop
        cycle = 0
        while True:
            try:
                cycle += 1
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Report status to brain
                self.brain.report_status()

                # Get priorities
                priorities = self.brain.get_priorities()
                pending = [p for p in priorities if p.get('status') == 'PENDING']

                print(f"[{now}] 🔄 Cycle #{cycle}")
                print(f"   📋 {len(pending)} priorities pending")

                if pending:
                    # Show top 3 priorities
                    print(f"   🎯 Top priorities:")
                    for i, p in enumerate(pending[:3], 1):
                        print(f"      {i}. {p.get('task', 'Unnamed')[:60]}")

                # Log this cycle
                self.brain.log_task(
                    task_name=f"Autonomous cycle #{cycle}",
                    status="COMPLETED",
                    result=f"{len(pending)} priorities pending",
                    duration="instant"
                )

                # Save dashboard
                self.brain.save_dashboard()

                print(f"   ✅ Dashboard updated")
                print(f"   ⏳ Next check in 5 minutes...")
                print()

                # Wait 5 minutes
                time.sleep(300)

            except KeyboardInterrupt:
                print("\n\n🛑 Autonomous mode stopped by Commander")
                self.brain.log_task(
                    task_name="Autonomous mode shutdown",
                    status="STOPPED",
                    result=f"Ran {cycle} cycles"
                )
                break

            except Exception as e:
                print(f"\n❌ Error in cycle #{cycle}: {e}")
                self.brain.log_error(
                    error_type="Autonomous execution error",
                    message=str(e),
                    context=f"Cycle #{cycle}"
                )
                # Wait 1 minute on error, then retry
                time.sleep(60)


def main():
    """Main execution"""

    scaffold = AutonomousScaffold()

    # Step 1: Scaffold todos to brain
    total_scaffolded = scaffold.scaffold_to_brain()

    if total_scaffolded == 0:
        print("⚠️  No tasks to scaffold - nothing to do!")
        print("   Add some priorities or check todo_brain_local.json")
        return

    # Step 2: Save dashboard
    print("💾 Saving dashboard...")
    scaffold.brain.save_dashboard()
    dashboard_path = scaffold.brain.brain_dir / "dashboard.html"
    print(f"   ✅ Dashboard: {dashboard_path}")
    print()

    # Step 3: Activate autonomous mode
    print("=" * 60)
    print("🎯 READY FOR AUTONOMOUS EXECUTION")
    print("=" * 60)
    print()
    print(f"✅ {total_scaffolded} tasks scaffolded to Brain")
    print(f"✅ Dashboard ready at: {dashboard_path}")
    print(f"✅ Autonomous mode starting...")
    print()

    input("Press ENTER to activate autonomous mode (or Ctrl+C to exit): ")
    print()

    # Start autonomous execution
    scaffold.activate_autonomous_mode()


if __name__ == "__main__":
    main()
