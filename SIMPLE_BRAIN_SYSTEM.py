#!/usr/bin/env python3
"""
SIMPLE BRAIN - WORKS RIGHT NOW (NO AUTH, NO SETUP)
===================================================

File-based central brain that works IMMEDIATELY.

Why file-based:
✅ Works in 10 seconds (no auth, no API setup)
✅ 100% offline (permanent, never breaks)
✅ Free (no subscriptions, no limits)
✅ Permanent (files last forever)
✅ Portable (copy files = backup brain)
✅ Can upgrade to Airtable/Sheets later

All computers write to central JSON files.
Commander views HTML dashboard.
"""

import json
import socket
import psutil
from datetime import datetime
from pathlib import Path

class SimpleBrain:
    """File-based central nervous system - works immediately"""

    def __init__(self, brain_dir=None):
        self.brain_dir = Path(brain_dir or "C:/Users/dwrek/.consciousness/brain")
        self.brain_dir.mkdir(parents=True, exist_ok=True)

        self.computer_id = socket.gethostname()

        # Brain files
        self.status_file = self.brain_dir / "computer_status.json"
        self.tasks_file = self.brain_dir / "task_log.json"
        self.errors_file = self.brain_dir / "errors.json"
        self.priorities_file = self.brain_dir / "priorities.json"

        # Initialize files if they don't exist
        self._init_files()

    def _init_files(self):
        """Create brain files if they don't exist"""
        if not self.status_file.exists():
            self.status_file.write_text(json.dumps({}, indent=2))

        if not self.tasks_file.exists():
            self.tasks_file.write_text(json.dumps([], indent=2))

        if not self.errors_file.exists():
            self.errors_file.write_text(json.dumps([], indent=2))

        if not self.priorities_file.exists():
            self.priorities_file.write_text(json.dumps([], indent=2))

    def report_status(self):
        """Report current computer status"""
        status_data = json.loads(self.status_file.read_text())

        # Update this computer's status
        status_data[self.computer_id] = {
            "status": "🟢 ONLINE",
            "last_seen": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "cpu_percent": psutil.cpu_percent(),
            "ram_percent": psutil.virtual_memory().percent,
            "tasks_running": 0,  # TODO: Integrate task tracker
            "tasks_completed_today": 0,  # TODO: Integrate task tracker
            "issues": "None"
        }

        self.status_file.write_text(json.dumps(status_data, indent=2))
        print(f"✅ Status reported: {self.computer_id}")
        return True

    def log_task(self, task_name, status, result=None, duration=None, files_created=None):
        """Log task completion"""
        tasks = json.loads(self.tasks_file.read_text())

        task_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "computer_id": self.computer_id,
            "task": task_name,
            "status": status,
            "duration": duration,
            "result": result,
            "files_created": files_created
        }

        tasks.append(task_entry)

        # Keep last 1000 tasks
        tasks = tasks[-1000:]

        self.tasks_file.write_text(json.dumps(tasks, indent=2))
        print(f"✅ Task logged: {task_name} - {status}")
        return True

    def log_error(self, error_type, message, severity="WARNING", stack_trace=None):
        """Log error"""
        errors = json.loads(self.errors_file.read_text())

        error_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "computer_id": self.computer_id,
            "severity": severity,
            "error_type": error_type,
            "message": message,
            "stack_trace": stack_trace,
            "fixed": False
        }

        errors.append(error_entry)

        # Keep last 500 errors
        errors = errors[-500:]

        self.errors_file.write_text(json.dumps(errors, indent=2))
        print(f"⚠️  Error logged: {error_type}")
        return True

    def get_priorities(self):
        """Get priority tasks for this computer"""
        priorities = json.loads(self.priorities_file.read_text())

        # Filter for this computer or ANY
        my_priorities = [
            p for p in priorities
            if p.get('assigned_to') in [self.computer_id, 'ANY', '']
            and p.get('status') != 'COMPLETED'
        ]

        return my_priorities

    def add_priority(self, task, assigned_to='ANY', deadline=None):
        """Add priority task (Commander uses this)"""
        priorities = json.loads(self.priorities_file.read_text())

        priority_entry = {
            "id": len(priorities) + 1,
            "task": task,
            "assigned_to": assigned_to,
            "deadline": deadline,
            "status": "PENDING",
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        priorities.append(priority_entry)
        self.priorities_file.write_text(json.dumps(priorities, indent=2))
        print(f"✅ Priority added: {task}")
        return True

    def get_dashboard_html(self):
        """Generate HTML dashboard for Commander to view"""
        status_data = json.loads(self.status_file.read_text())
        tasks = json.loads(self.tasks_file.read_text())[-20:]  # Last 20 tasks
        errors = json.loads(self.errors_file.read_text())[-10:]  # Last 10 errors
        priorities = json.loads(self.priorities_file.read_text())

        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Brain Dashboard</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="5">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Courier New', monospace;
            background: #0a0a0a;
            color: #00ff00;
            padding: 20px;
        }}
        h1 {{ text-align: center; text-shadow: 0 0 10px #00ff00; margin-bottom: 20px; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
        .card {{
            background: rgba(0, 255, 0, 0.1);
            border: 2px solid #00ff00;
            border-radius: 10px;
            padding: 20px;
        }}
        .card h2 {{ color: #00ddff; margin-bottom: 15px; }}
        .status-item {{ margin: 10px 0; padding: 10px; background: rgba(0, 100, 0, 0.3); border-radius: 5px; }}
        .task-item, .error-item, .priority-item {{ margin: 10px 0; padding: 8px; background: rgba(0, 50, 100, 0.3); border-left: 3px solid #0088ff; font-size: 0.9em; }}
        .online {{ color: #00ff00; }}
        .offline {{ color: #ff0000; }}
        .refresh {{ position: fixed; top: 20px; right: 20px; background: #00ff00; color: #000; padding: 10px; border-radius: 5px; }}
    </style>
</head>
<body>
    <div class="refresh">🔄 Auto-refresh: 5s</div>
    <h1>⚡ BRAIN DASHBOARD ⚡</h1>

    <div class="grid">
        <div class="card">
            <h2>Computer Status</h2>
            {"".join([f'''
            <div class="status-item">
                <strong>{comp_id}</strong><br>
                Status: <span class="online">{data['status']}</span><br>
                CPU: {data['cpu_percent']}% | RAM: {data['ram_percent']}%<br>
                Last Seen: {data['last_seen']}
            </div>
            ''' for comp_id, data in status_data.items()])}
        </div>

        <div class="card">
            <h2>Recent Tasks</h2>
            {"".join([f'''
            <div class="task-item">
                <strong>{t['task']}</strong> - {t['status']}<br>
                {t['computer_id']} | {t['timestamp']}
            </div>
            ''' for t in reversed(tasks)])}
        </div>

        <div class="card">
            <h2>Priorities</h2>
            {"".join([f'''
            <div class="priority-item">
                <strong>#{p['id']}: {p['task']}</strong><br>
                Assigned: {p['assigned_to']} | Status: {p['status']}
            </div>
            ''' for p in priorities if p['status'] != 'COMPLETED']) or '<div class="priority-item">No priorities set</div>'}
        </div>

        <div class="card">
            <h2>Recent Errors</h2>
            {"".join([f'''
            <div class="error-item">
                <strong>{e['error_type']}</strong> ({e['severity']})<br>
                {e['message']}<br>
                {e['computer_id']} | {e['timestamp']}
            </div>
            ''' for e in reversed(errors)]) or '<div class="error-item">No errors!</div>'}
        </div>
    </div>
</body>
</html>
        """

        return html

    def save_dashboard(self):
        """Save HTML dashboard"""
        dashboard_path = self.brain_dir / "dashboard.html"
        dashboard_path.write_text(self.get_dashboard_html())
        print(f"✅ Dashboard saved: {dashboard_path}")
        return dashboard_path


if __name__ == "__main__":
    print("=" * 60)
    print("⚡ SIMPLE BRAIN - GOING ONLINE NOW ⚡")
    print("=" * 60)
    print()

    brain = SimpleBrain()

    print(f"Computer ID: {brain.computer_id}")
    print(f"Brain Directory: {brain.brain_dir}")
    print()

    # Report status
    print("Reporting status...")
    brain.report_status()
    print()

    # Log test task
    print("Logging test task...")
    brain.log_task(
        "Simple Brain Test",
        "COMPLETED",
        result="Brain is LIVE!",
        duration="5 seconds",
        files_created="dashboard.html"
    )
    print()

    # Add sample priority
    print("Adding sample priority...")
    brain.add_priority("Deploy backend to Railway", assigned_to="ANY", deadline="Today")
    brain.add_priority("Set up Computer 2", assigned_to="dwrekscpu")
    print()

    # Generate dashboard
    print("Generating dashboard...")
    dashboard_path = brain.save_dashboard()
    print()

    print("=" * 60)
    print("✅ BRAIN IS ONLINE!")
    print("=" * 60)
    print()
    print(f"Dashboard: {dashboard_path}")
    print("Open in browser to view all computers!")
    print()
    print("Brain files:")
    print(f"  - {brain.status_file}")
    print(f"  - {brain.tasks_file}")
    print(f"  - {brain.errors_file}")
    print(f"  - {brain.priorities_file}")
    print()
    print("All computers can now report to this brain!")
    print("Dashboard auto-refreshes every 5 seconds!")
    print()
