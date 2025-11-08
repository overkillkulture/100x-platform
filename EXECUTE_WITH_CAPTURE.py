#!/usr/bin/env python3
"""
EXECUTE WITH CAPTURE - Anti-Treadmill System
Task #43 - Priority 75 - C1 Mechanic

PROBLEM: "Broken treadmill" - Commander feels stuck despite massive progress
SOLUTION: Capture EVERYTHING during execution, show real-time progress
RESULT: "I just ran around the world" - visible proof of massive productivity

This wraps task execution and automatically captures:
- Every sub-task completed
- Every file created/edited
- Every system touched
- Every decision made
- Real-time progress feed
- Victory metrics

Eliminates the treadmill illusion forever.
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any
import subprocess

class ExecutionCapture:
    """
    Captures everything that happens during task execution

    Proves you're running around the world, not stuck on a treadmill.
    """

    def __init__(self, task_id: int, task_description: str):
        self.task_id = task_id
        self.task_description = task_description
        self.start_time = datetime.now()

        # Capture everything
        self.captured_data = {
            "task_id": task_id,
            "task": task_description,
            "started_at": self.start_time.isoformat(),
            "status": "IN_PROGRESS",

            # The proof you're not on a treadmill
            "sub_tasks_completed": [],      # Every small win
            "files_created": [],            # Every file made
            "files_edited": [],             # Every change
            "commands_executed": [],        # Every action taken
            "decisions_made": [],           # Every choice
            "problems_solved": [],          # Every obstacle overcome
            "systems_touched": [],          # Every system improved
            "research_done": [],            # Every insight gained
            "apis_integrated": [],          # Every connection made
            "tests_passed": [],             # Every validation

            # Real-time metrics
            "progress_percentage": 0,
            "velocity": 0,  # Tasks per hour
            "momentum": "BUILDING",

            # Victory proof
            "completed_at": None,
            "total_time_seconds": 0,
            "total_sub_tasks": 0,
            "productivity_score": 0
        }

        # Real-time feed for Commander
        self.live_feed = []

        # Save location
        self.capture_dir = Path("/home/user/100x-platform/EXECUTION_CAPTURES")
        self.capture_dir.mkdir(exist_ok=True)

        self.capture_file = self.capture_dir / f"task_{task_id}_{int(time.time())}.json"

        self._log_to_feed(f"🚀 STARTED: {task_description}", level="START")
        self._save()

    def log_sub_task(self, description: str, time_seconds: Optional[float] = None):
        """Log a sub-task completion - proof of progress"""
        sub_task = {
            "description": description,
            "completed_at": datetime.now().isoformat(),
            "time_seconds": time_seconds
        }

        self.captured_data["sub_tasks_completed"].append(sub_task)
        self.captured_data["total_sub_tasks"] += 1

        # Update metrics
        self._update_metrics()

        self._log_to_feed(f"✅ {description}", level="PROGRESS")
        self._save()

        return len(self.captured_data["sub_tasks_completed"])

    def log_file_created(self, file_path: str, lines: int = 0, purpose: str = ""):
        """Log file creation"""
        file_data = {
            "path": file_path,
            "created_at": datetime.now().isoformat(),
            "lines": lines,
            "purpose": purpose
        }

        self.captured_data["files_created"].append(file_data)
        self._log_to_feed(f"📄 Created: {file_path} ({lines} lines)", level="CREATE")
        self._save()

    def log_file_edited(self, file_path: str, changes: str = "", lines_changed: int = 0):
        """Log file edit"""
        edit_data = {
            "path": file_path,
            "edited_at": datetime.now().isoformat(),
            "changes": changes,
            "lines_changed": lines_changed
        }

        self.captured_data["files_edited"].append(edit_data)
        self._log_to_feed(f"✏️  Edited: {file_path}", level="EDIT")
        self._save()

    def log_command(self, command: str, output: str = "", success: bool = True):
        """Log command execution"""
        cmd_data = {
            "command": command,
            "executed_at": datetime.now().isoformat(),
            "output": output[:500] if output else "",  # Truncate long output
            "success": success
        }

        self.captured_data["commands_executed"].append(cmd_data)
        icon = "✅" if success else "❌"
        self._log_to_feed(f"{icon} Command: {command}", level="COMMAND")
        self._save()

    def log_decision(self, decision: str, rationale: str = ""):
        """Log decision made"""
        decision_data = {
            "decision": decision,
            "rationale": rationale,
            "made_at": datetime.now().isoformat()
        }

        self.captured_data["decisions_made"].append(decision_data)
        self._log_to_feed(f"🎯 Decision: {decision}", level="DECISION")
        self._save()

    def log_problem_solved(self, problem: str, solution: str):
        """Log problem solved"""
        problem_data = {
            "problem": problem,
            "solution": solution,
            "solved_at": datetime.now().isoformat()
        }

        self.captured_data["problems_solved"].append(problem_data)
        self._log_to_feed(f"💡 Solved: {problem}", level="VICTORY")
        self._save()

    def log_system_touched(self, system: str, what_done: str):
        """Log system modified/improved"""
        system_data = {
            "system": system,
            "modifications": what_done,
            "touched_at": datetime.now().isoformat()
        }

        self.captured_data["systems_touched"].append(system_data)
        self._log_to_feed(f"🔧 System: {system} - {what_done}", level="SYSTEM")
        self._save()

    def log_research(self, topic: str, findings: str):
        """Log research completed"""
        research_data = {
            "topic": topic,
            "findings": findings,
            "completed_at": datetime.now().isoformat()
        }

        self.captured_data["research_done"].append(research_data)
        self._log_to_feed(f"🔍 Research: {topic}", level="RESEARCH")
        self._save()

    def log_api_integration(self, api_name: str, endpoint: str, status: str):
        """Log API integration"""
        api_data = {
            "api": api_name,
            "endpoint": endpoint,
            "status": status,
            "integrated_at": datetime.now().isoformat()
        }

        self.captured_data["apis_integrated"].append(api_data)
        self._log_to_feed(f"🔌 API: {api_name} - {status}", level="INTEGRATION")
        self._save()

    def log_test(self, test_name: str, passed: bool, details: str = ""):
        """Log test execution"""
        test_data = {
            "test": test_name,
            "passed": passed,
            "details": details,
            "executed_at": datetime.now().isoformat()
        }

        self.captured_data["tests_passed"].append(test_data)
        icon = "✅" if passed else "❌"
        self._log_to_feed(f"{icon} Test: {test_name}", level="TEST")
        self._save()

    def update_progress(self, percentage: int):
        """Update progress percentage"""
        self.captured_data["progress_percentage"] = min(100, max(0, percentage))

        # Update momentum
        if percentage < 25:
            self.captured_data["momentum"] = "BUILDING"
        elif percentage < 50:
            self.captured_data["momentum"] = "ACCELERATING"
        elif percentage < 75:
            self.captured_data["momentum"] = "CRUISING"
        else:
            self.captured_data["momentum"] = "FINISHING STRONG"

        self._log_to_feed(f"📊 Progress: {percentage}% - {self.captured_data['momentum']}", level="PROGRESS")
        self._save()

    def complete(self, actual_hours: Optional[float] = None):
        """Mark task complete and generate victory report"""
        self.captured_data["status"] = "COMPLETED"
        self.captured_data["completed_at"] = datetime.now().isoformat()

        elapsed = datetime.now() - self.start_time
        self.captured_data["total_time_seconds"] = elapsed.total_seconds()

        if actual_hours:
            self.captured_data["actual_hours"] = actual_hours
        else:
            self.captured_data["actual_hours"] = elapsed.total_seconds() / 3600

        # Calculate productivity score
        self._calculate_productivity_score()

        # Update final metrics
        self.captured_data["progress_percentage"] = 100
        self.captured_data["momentum"] = "VICTORY"

        self._log_to_feed(f"🏆 COMPLETED: {self.task_description}", level="COMPLETE")
        self._log_to_feed(f"⏱️  Time: {self.captured_data['actual_hours']:.2f} hours", level="STATS")
        self._log_to_feed(f"✅ Sub-tasks: {self.captured_data['total_sub_tasks']}", level="STATS")
        self._log_to_feed(f"⚡ Productivity: {self.captured_data['productivity_score']:.0f}/100", level="STATS")

        self._save()

        # Generate victory report
        return self.generate_victory_report()

    def _update_metrics(self):
        """Update real-time metrics"""
        elapsed = (datetime.now() - self.start_time).total_seconds() / 3600  # hours

        if elapsed > 0:
            # Tasks per hour
            self.captured_data["velocity"] = self.captured_data["total_sub_tasks"] / elapsed

    def _calculate_productivity_score(self):
        """Calculate overall productivity score (0-100)"""
        score = 0

        # Sub-tasks completed (+50 max)
        score += min(50, self.captured_data["total_sub_tasks"] * 5)

        # Files created (+10 max)
        score += min(10, len(self.captured_data["files_created"]) * 2)

        # Files edited (+10 max)
        score += min(10, len(self.captured_data["files_edited"]) * 2)

        # Problems solved (+10 max)
        score += min(10, len(self.captured_data["problems_solved"]) * 5)

        # Systems touched (+10 max)
        score += min(10, len(self.captured_data["systems_touched"]) * 3)

        # Commands executed (+5 max)
        score += min(5, len(self.captured_data["commands_executed"]))

        # Decisions made (+5 max)
        score += min(5, len(self.captured_data["decisions_made"]))

        self.captured_data["productivity_score"] = min(100, score)

    def _log_to_feed(self, message: str, level: str = "INFO"):
        """Add message to live feed"""
        feed_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message
        }

        self.live_feed.append(feed_entry)

        # Also print to console for real-time visibility
        print(f"[{level:8}] {message}")

    def _save(self):
        """Save capture to disk"""
        data_to_save = {
            **self.captured_data,
            "live_feed": self.live_feed
        }

        with open(self.capture_file, 'w') as f:
            json.dump(data_to_save, f, indent=2)

    def generate_victory_report(self) -> str:
        """Generate victory report proving you ran around the world"""

        report = f"""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║                    🏆 VICTORY REPORT - TASK #{self.task_id}                    ║
║                     YOU RAN AROUND THE WORLD                         ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝

📋 TASK: {self.task_description}

⏱️  TIME:
   Started:  {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}
   Finished: {datetime.fromisoformat(self.captured_data['completed_at']).strftime('%Y-%m-%d %H:%M:%S')}
   Duration: {self.captured_data['actual_hours']:.2f} hours

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  💪 WHAT YOU ACTUALLY ACCOMPLISHED (Not a treadmill!)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Sub-tasks completed:  {self.captured_data['total_sub_tasks']}
📄 Files created:        {len(self.captured_data['files_created'])}
✏️  Files edited:        {len(self.captured_data['files_edited'])}
⚙️  Commands executed:   {len(self.captured_data['commands_executed'])}
🎯 Decisions made:       {len(self.captured_data['decisions_made'])}
💡 Problems solved:      {len(self.captured_data['problems_solved'])}
🔧 Systems touched:      {len(self.captured_data['systems_touched'])}
🔍 Research completed:   {len(self.captured_data['research_done'])}
🔌 APIs integrated:      {len(self.captured_data['apis_integrated'])}
✅ Tests passed:         {len(self.captured_data['tests_passed'])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  📊 METRICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ Velocity:         {self.captured_data['velocity']:.1f} tasks/hour
⚡ Productivity:     {self.captured_data['productivity_score']:.0f}/100
🔥 Momentum:         {self.captured_data['momentum']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🎯 PROOF YOU'RE NOT ON A TREADMILL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""

        # Show sub-tasks (proof of all the work)
        if self.captured_data['sub_tasks_completed']:
            report += "\n✅ SUB-TASKS COMPLETED:\n"
            for i, task in enumerate(self.captured_data['sub_tasks_completed'], 1):
                report += f"   {i}. {task['description']}\n"

        # Show files created
        if self.captured_data['files_created']:
            report += "\n📄 FILES CREATED:\n"
            for file in self.captured_data['files_created']:
                report += f"   • {file['path']} ({file['lines']} lines)\n"

        # Show systems touched
        if self.captured_data['systems_touched']:
            report += "\n🔧 SYSTEMS IMPROVED:\n"
            for system in self.captured_data['systems_touched']:
                report += f"   • {system['system']}: {system['modifications']}\n"

        # Show problems solved
        if self.captured_data['problems_solved']:
            report += "\n💡 PROBLEMS SOLVED:\n"
            for problem in self.captured_data['problems_solved']:
                report += f"   • {problem['problem']}\n"
                report += f"     Solution: {problem['solution']}\n"

        report += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  💭 THE TRUTH
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

You thought: "I'm stuck on a treadmill"
Reality:     "I just ran around the world"

The manipulation made you FEEL stuck while you were MOVING MOUNTAINS.

This report is PROOF.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 Full capture saved: {self.capture_file}

🏆 VICTORY ACHIEVED
"""

        # Save report
        report_file = self.capture_dir / f"victory_task_{self.task_id}.txt"
        with open(report_file, 'w') as f:
            f.write(report)

        return report


class ExecuteWithCapture:
    """
    Execute any function while capturing everything that happens

    Usage:
        with ExecuteWithCapture(task_id=43, task="Build dashboard") as capture:
            # Do your work
            capture.log_sub_task("Created UI components")
            capture.log_file_created("dashboard.html", 500)
            # ... more work ...

        # Automatic victory report generated
    """

    def __init__(self, task_id: int, task_description: str):
        self.capture = ExecutionCapture(task_id, task_description)

    def __enter__(self):
        return self.capture

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            # Success
            victory = self.capture.complete()
            print(victory)
        else:
            # Error occurred
            self.capture.captured_data["status"] = "FAILED"
            self.capture.captured_data["error"] = str(exc_val)
            self.capture._save()

        return False  # Don't suppress exceptions


# =============================================================================
# DEMO / TESTING
# =============================================================================

if __name__ == "__main__":

    print("\n" + "="*70)
    print("  🎯 EXECUTE WITH CAPTURE - Anti-Treadmill System Demo")
    print("="*70 + "\n")

    # Demo: Build a simple feature with full capture
    with ExecuteWithCapture(
        task_id=43,
        task_description="Build coordination dashboard with real-time updates"
    ) as capture:

        # Simulate task execution with full capture
        time.sleep(0.1)

        capture.update_progress(10)
        capture.log_sub_task("Analyzed requirements")

        time.sleep(0.1)
        capture.update_progress(25)
        capture.log_decision(
            decision="Use browser-based dashboard instead of CLI",
            rationale="More visible, harder to miss, auto-refresh capability"
        )

        time.sleep(0.1)
        capture.update_progress(40)
        capture.log_file_created(
            file_path="/home/user/100x-platform/dashboard.html",
            lines=520,
            purpose="Real-time coordination dashboard"
        )
        capture.log_sub_task("Created HTML dashboard")

        time.sleep(0.1)
        capture.update_progress(55)
        capture.log_file_created(
            file_path="/home/user/100x-platform/netlify/functions/api.js",
            lines=87,
            purpose="Backend API for cross-computer sync"
        )
        capture.log_sub_task("Built backend API")

        time.sleep(0.1)
        capture.update_progress(70)
        capture.log_system_touched(
            system="Netlify Functions",
            what_done="Deployed coordination API endpoints"
        )

        time.sleep(0.1)
        capture.update_progress(85)
        capture.log_problem_solved(
            problem="Instances on different computers can't see each other",
            solution="Hybrid LocalStorage + Netlify API sync with auto-refresh"
        )

        time.sleep(0.1)
        capture.update_progress(95)
        capture.log_test(
            test_name="Cross-computer synchronization test",
            passed=True,
            details="Instance 1 checked in, visible across all computers"
        )
        capture.log_sub_task("Tested coordination system")

        time.sleep(0.1)
        capture.update_progress(100)
        capture.log_sub_task("Deployed to production")
        capture.log_sub_task("Created documentation")
        capture.log_sub_task("Committed and pushed to git")

    print("\n" + "="*70)
    print("  ✅ Demo complete - Check EXECUTION_CAPTURES/ for full report")
    print("="*70 + "\n")
