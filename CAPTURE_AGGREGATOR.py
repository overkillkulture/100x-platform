#!/usr/bin/env python3
"""
EXECUTION CAPTURE AGGREGATOR
Aggregates all execution captures across all instances

Shows Commander EVERYTHING being accomplished across:
- All 16 Claude instances
- All 3 computers
- All time periods

Proves total progress, not just individual tasks.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from collections import defaultdict

class CaptureAggregator:
    """Aggregates execution captures to show total progress"""

    def __init__(self, capture_dir: str = "EXECUTION_CAPTURES"):
        self.capture_dir = Path(capture_dir)
        self.captures = []
        self.stats = {
            "total_tasks": 0,
            "total_sub_tasks": 0,
            "total_files_created": 0,
            "total_files_edited": 0,
            "total_commands": 0,
            "total_decisions": 0,
            "total_problems_solved": 0,
            "total_systems_touched": 0,
            "total_hours": 0.0,
            "avg_productivity": 0.0,
            "total_velocity": 0.0
        }

    def load_all_captures(self):
        """Load all execution capture files"""
        if not self.capture_dir.exists():
            print(f"⚠️  No captures directory found: {self.capture_dir}")
            return

        json_files = list(self.capture_dir.glob("task_*.json"))

        print(f"📊 Found {len(json_files)} execution captures")

        for json_file in json_files:
            try:
                with open(json_file, 'r') as f:
                    capture_data = json.load(f)
                    self.captures.append(capture_data)
            except Exception as e:
                print(f"⚠️  Error loading {json_file}: {e}")

        print(f"✅ Loaded {len(self.captures)} captures successfully\n")

    def calculate_stats(self):
        """Calculate aggregate statistics"""
        if not self.captures:
            return

        self.stats["total_tasks"] = len(self.captures)

        for capture in self.captures:
            self.stats["total_sub_tasks"] += capture.get("total_sub_tasks", 0)
            self.stats["total_files_created"] += len(capture.get("files_created", []))
            self.stats["total_files_edited"] += len(capture.get("files_edited", []))
            self.stats["total_commands"] += len(capture.get("commands_executed", []))
            self.stats["total_decisions"] += len(capture.get("decisions_made", []))
            self.stats["total_problems_solved"] += len(capture.get("problems_solved", []))
            self.stats["total_systems_touched"] += len(capture.get("systems_touched", []))

            # Time
            if capture.get("actual_hours"):
                self.stats["total_hours"] += capture["actual_hours"]

            # Productivity
            if capture.get("productivity_score"):
                self.stats["avg_productivity"] += capture["productivity_score"]

            # Velocity
            if capture.get("velocity"):
                self.stats["total_velocity"] += capture["velocity"]

        # Calculate averages
        if self.stats["total_tasks"] > 0:
            self.stats["avg_productivity"] /= self.stats["total_tasks"]
            self.stats["total_velocity"] /= self.stats["total_tasks"]

    def generate_summary_report(self) -> str:
        """Generate comprehensive summary report"""

        report = f"""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║              🌍 TOTAL PROGRESS ACROSS ALL INSTANCES                  ║
║                   PROOF YOU RAN AROUND THE WORLD                     ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝

📅 Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  📊 AGGREGATE STATISTICS (ALL INSTANCES)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 Tasks Completed:       {self.stats['total_tasks']}
✅ Sub-tasks Completed:   {self.stats['total_sub_tasks']}
📄 Files Created:         {self.stats['total_files_created']}
✏️  Files Edited:         {self.stats['total_files_edited']}
⚙️  Commands Executed:    {self.stats['total_commands']}
🎯 Decisions Made:        {self.stats['total_decisions']}
💡 Problems Solved:       {self.stats['total_problems_solved']}
🔧 Systems Touched:       {self.stats['total_systems_touched']}

⏱️  Total Time:           {self.stats['total_hours']:.2f} hours
⚡ Avg Productivity:      {self.stats['avg_productivity']:.0f}/100
⚡ Avg Velocity:          {self.stats['total_velocity']:.1f} tasks/hour

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  📋 TASK BREAKDOWN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""

        # List all completed tasks
        for i, capture in enumerate(self.captures, 1):
            status = capture.get("status", "UNKNOWN")
            task_id = capture.get("task_id", "?")
            task_desc = capture.get("task", "Unknown task")
            sub_tasks = capture.get("total_sub_tasks", 0)

            icon = "✅" if status == "COMPLETED" else "⏳"

            report += f"{icon} Task #{task_id}: {task_desc[:60]}\n"
            report += f"   • Sub-tasks: {sub_tasks}\n"
            report += f"   • Files: {len(capture.get('files_created', []))} created, {len(capture.get('files_edited', []))} edited\n"
            report += f"   • Status: {status}\n\n"

        report += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  💡 PROBLEMS SOLVED ACROSS ALL INSTANCES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""

        # Aggregate problems solved
        all_problems = []
        for capture in self.captures:
            all_problems.extend(capture.get("problems_solved", []))

        if all_problems:
            for i, problem in enumerate(all_problems, 1):
                report += f"{i}. {problem['problem']}\n"
                report += f"   Solution: {problem['solution']}\n\n"
        else:
            report += "   (No problems recorded yet)\n\n"

        report += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🔧 SYSTEMS IMPROVED ACROSS ALL INSTANCES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""

        # Aggregate systems touched
        systems_map = defaultdict(list)
        for capture in self.captures:
            for system in capture.get("systems_touched", []):
                systems_map[system['system']].append(system['modifications'])

        if systems_map:
            for system, mods in systems_map.items():
                report += f"🔧 {system}:\n"
                for mod in mods:
                    report += f"   • {mod}\n"
                report += "\n"
        else:
            report += "   (No systems recorded yet)\n\n"

        report += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  💭 THE ULTIMATE TRUTH
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This is not one instance.
This is not one task.
This is not one day.

This is EVERYTHING across ALL instances, ALL computers, ALL work.

You thought: "Am I stuck on a treadmill?"

Reality: Look at these {self.stats['total_tasks']} tasks, {self.stats['total_sub_tasks']} sub-tasks,
         {self.stats['total_files_created']} files created, {self.stats['total_problems_solved']} problems solved.

You didn't run around the world once.
You ran around it {self.stats['total_tasks']} times.

THIS IS PROOF.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 Individual captures: {self.capture_dir}/
🏆 Total Victories: {self.stats['total_tasks']}
"""

        return report

    def generate_html_dashboard(self) -> str:
        """Generate interactive HTML dashboard"""

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏆 Total Progress Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            min-height: 100vh;
        }}

        .header {{
            text-align: center;
            margin-bottom: 40px;
            animation: fadeIn 1s;
        }}

        .header h1 {{
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}

        .stat-card {{
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            transition: transform 0.3s, box-shadow 0.3s;
            animation: slideIn 0.5s;
        }}

        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }}

        .stat-number {{
            font-size: 3em;
            font-weight: bold;
            margin: 10px 0;
        }}

        .stat-label {{
            font-size: 1.1em;
            opacity: 0.9;
        }}

        .tasks-list {{
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
        }}

        .task-item {{
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 15px;
            transition: background 0.3s;
        }}

        .task-item:hover {{
            background: rgba(255,255,255,0.2);
        }}

        .task-title {{
            font-size: 1.3em;
            font-weight: bold;
            margin-bottom: 10px;
        }}

        .task-details {{
            opacity: 0.9;
            line-height: 1.8;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}

        @keyframes slideIn {{
            from {{
                opacity: 0;
                transform: translateY(20px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        .truth-section {{
            background: rgba(255,255,255,0.15);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 40px;
            text-align: center;
            font-size: 1.3em;
            line-height: 1.8;
            margin-top: 40px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🏆 TOTAL PROGRESS DASHBOARD</h1>
        <p>Proof You Ran Around The World</p>
        <p style="opacity: 0.8; margin-top: 10px;">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>

    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-label">🎯 Tasks Completed</div>
            <div class="stat-number">{self.stats['total_tasks']}</div>
        </div>

        <div class="stat-card">
            <div class="stat-label">✅ Sub-tasks</div>
            <div class="stat-number">{self.stats['total_sub_tasks']}</div>
        </div>

        <div class="stat-card">
            <div class="stat-label">📄 Files Created</div>
            <div class="stat-number">{self.stats['total_files_created']}</div>
        </div>

        <div class="stat-card">
            <div class="stat-label">✏️ Files Edited</div>
            <div class="stat-number">{self.stats['total_files_edited']}</div>
        </div>

        <div class="stat-card">
            <div class="stat-label">💡 Problems Solved</div>
            <div class="stat-number">{self.stats['total_problems_solved']}</div>
        </div>

        <div class="stat-card">
            <div class="stat-label">🔧 Systems Touched</div>
            <div class="stat-number">{self.stats['total_systems_touched']}</div>
        </div>

        <div class="stat-card">
            <div class="stat-label">⏱️ Total Hours</div>
            <div class="stat-number">{self.stats['total_hours']:.1f}</div>
        </div>

        <div class="stat-card">
            <div class="stat-label">⚡ Productivity</div>
            <div class="stat-number">{self.stats['avg_productivity']:.0f}/100</div>
        </div>
    </div>

    <div class="tasks-list">
        <h2 style="margin-bottom: 25px; font-size: 2em;">📋 All Completed Tasks</h2>
"""

        for capture in self.captures:
            task_id = capture.get("task_id", "?")
            task_desc = capture.get("task", "Unknown task")
            status = capture.get("status", "UNKNOWN")
            sub_tasks = capture.get("total_sub_tasks", 0)
            files_created = len(capture.get("files_created", []))
            files_edited = len(capture.get("files_edited", []))

            html += f"""
        <div class="task-item">
            <div class="task-title">✅ Task #{task_id}: {task_desc}</div>
            <div class="task-details">
                • {sub_tasks} sub-tasks completed<br>
                • {files_created} files created, {files_edited} edited<br>
                • Status: {status}
            </div>
        </div>
"""

        html += f"""
    </div>

    <div class="truth-section">
        <h2 style="margin-bottom: 20px;">💭 THE TRUTH</h2>
        <p>
            You thought: "Am I stuck on a treadmill?"<br><br>
            Reality: <strong>{self.stats['total_tasks']} tasks completed,
            {self.stats['total_sub_tasks']} sub-tasks done,
            {self.stats['total_files_created']} files created</strong><br><br>
            You didn't run around the world once.<br>
            You ran around it <strong>{self.stats['total_tasks']} times</strong>.<br><br>
            <strong>THIS IS PROOF.</strong>
        </p>
    </div>

    <script>
        // Auto-refresh every 30 seconds
        setTimeout(() => location.reload(), 30000);
    </script>
</body>
</html>
"""

        return html


def main():
    print("\n" + "="*70)
    print("  🌍 EXECUTION CAPTURE AGGREGATOR")
    print("  Proof of Total Progress Across All Instances")
    print("="*70 + "\n")

    aggregator = CaptureAggregator()

    # Load all captures
    aggregator.load_all_captures()

    if not aggregator.captures:
        print("⚠️  No captures found. Run some tasks first!")
        return

    # Calculate stats
    aggregator.calculate_stats()

    # Generate text report
    report = aggregator.generate_summary_report()
    print(report)

    # Save text report
    report_file = Path("TOTAL_PROGRESS_REPORT.txt")
    with open(report_file, 'w') as f:
        f.write(report)
    print(f"\n💾 Text report saved: {report_file}")

    # Generate HTML dashboard
    html = aggregator.generate_html_dashboard()
    html_file = Path("TOTAL_PROGRESS_DASHBOARD.html")
    with open(html_file, 'w') as f:
        f.write(html)
    print(f"💾 HTML dashboard saved: {html_file}")

    print(f"\n✅ Open {html_file} in your browser to see the full dashboard!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
