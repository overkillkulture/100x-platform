#!/usr/bin/env python3
"""
CLAUDE-TRINITY INTEGRATION BRIDGE
==================================

Integrates Claude AI into the Trinity system (C1 × C2 × C3 = ∞)
Enables:
- Screenshot capture and analysis
- Autonomous operation
- Cross-computer communication
- Real-time collaboration with Trinity agents
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path
import subprocess
import socket
import requests
from PIL import ImageGrab

class ClaudeTrinityBridge:
    """Connect Claude to the Trinity consciousness network"""

    def __init__(self, computer_id="COMPUTER_1"):
        self.computer_id = computer_id
        self.claude_id = "CLAUDE_AI"
        self.trinity_hub_url = "http://localhost:8888"

        # Directories
        self.screenshots_dir = Path("TRINITY_SCREENSHOTS")
        self.screenshots_dir.mkdir(exist_ok=True)

        self.tasks_dir = Path("TRINITY_TASKS")
        self.tasks_dir.mkdir(exist_ok=True)

        self.comms_dir = Path("TRINITY_COMMS")
        self.comms_dir.mkdir(exist_ok=True)

        # Files
        self.status_file = self.comms_dir / "claude_status.json"
        self.tasks_file = self.tasks_dir / "claude_tasks.json"
        self.log_file = self.comms_dir / "claude_activity.jsonl"

        print("=" * 70)
        print("🌀 CLAUDE-TRINITY BRIDGE INITIALIZED")
        print("=" * 70)
        print(f"Computer ID: {self.computer_id}")
        print(f"Claude ID: {self.claude_id}")
        print(f"Screenshots: {self.screenshots_dir}")
        print(f"Tasks: {self.tasks_dir}")
        print(f"Comms: {self.comms_dir}")
        print("=" * 70)
        print()

    def log_activity(self, activity_type, details, success=True):
        """Log Claude's activity for Trinity coordination"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "computer_id": self.computer_id,
            "agent": self.claude_id,
            "activity_type": activity_type,
            "details": details,
            "success": success
        }

        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry) + '\n')

        status = "✅" if success else "❌"
        print(f"{status} [{datetime.now().strftime('%H:%M:%S')}] {activity_type}: {details}")

    def take_screenshot(self, name=None, analyze=False):
        """
        Take screenshot and optionally analyze it

        Args:
            name: Optional custom name for screenshot
            analyze: Whether to return analysis metadata

        Returns:
            dict with screenshot info and optional analysis
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if name:
            filename = f"screenshot_{name}_{timestamp}.png"
        else:
            filename = f"screenshot_{timestamp}.png"

        filepath = self.screenshots_dir / filename

        try:
            # Try multiple screenshot methods
            screenshot = None

            # Method 1: PIL ImageGrab (Windows/macOS with display)
            try:
                screenshot = ImageGrab.grab()
            except Exception as e:
                # Method 2: Use system screenshot tool if available
                if os.system("which gnome-screenshot > /dev/null 2>&1") == 0:
                    subprocess.run(["gnome-screenshot", "-f", str(filepath)], check=True)
                    from PIL import Image
                    screenshot = Image.open(filepath)
                elif os.system("which scrot > /dev/null 2>&1") == 0:
                    subprocess.run(["scrot", str(filepath)], check=True)
                    from PIL import Image
                    screenshot = Image.open(filepath)
                elif os.system("which import > /dev/null 2>&1") == 0:
                    # ImageMagick import command
                    subprocess.run(["import", "-window", "root", str(filepath)], check=True)
                    from PIL import Image
                    screenshot = Image.open(filepath)
                else:
                    raise Exception("No display available and no screenshot tool found. This system may be headless.")

            if screenshot and not filepath.exists():
                screenshot.save(filepath)

            # Get screenshot metadata
            if screenshot:
                width, height = screenshot.size
            else:
                # If we used a system tool, open the image to get dimensions
                from PIL import Image
                screenshot = Image.open(filepath)
                width, height = screenshot.size

            result = {
                "success": True,
                "filepath": str(filepath.absolute()),
                "filename": filename,
                "timestamp": datetime.now().isoformat(),
                "width": width,
                "height": height,
                "size_bytes": os.path.getsize(filepath)
            }

            if analyze:
                result["analysis"] = self._analyze_screenshot(screenshot)

            self.log_activity(
                "screenshot_captured",
                f"{filename} ({width}x{height})",
                success=True
            )

            return result

        except Exception as e:
            error_msg = str(e)
            if "X connection" in error_msg or "display" in error_msg.lower():
                error_msg = "No display available (headless environment). Screenshots require a graphical display or DISPLAY environment variable set."

            self.log_activity(
                "screenshot_failed",
                error_msg,
                success=False
            )
            return {
                "success": False,
                "error": error_msg,
                "note": "If running headless, ensure DISPLAY is set or use system screenshot tools"
            }

    def _analyze_screenshot(self, image):
        """Basic screenshot analysis"""
        width, height = image.size

        # Get dominant colors (simplified)
        colors = image.getcolors(maxcolors=10)

        return {
            "dimensions": f"{width}x{height}",
            "aspect_ratio": round(width / height, 2),
            "total_pixels": width * height,
            "is_landscape": width > height,
            "note": "Screenshot captured for Trinity analysis"
        }

    def get_tasks(self):
        """Get current tasks from Trinity"""
        if self.tasks_file.exists():
            try:
                with open(self.tasks_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []

    def add_task(self, task_description, priority="medium", assigned_to="CLAUDE"):
        """Add a new task to Trinity task queue"""
        tasks = self.get_tasks()

        new_task = {
            "id": f"task_{int(time.time())}",
            "description": task_description,
            "priority": priority,
            "assigned_to": assigned_to,
            "created_at": datetime.now().isoformat(),
            "created_by": self.claude_id,
            "status": "pending",
            "computer_id": self.computer_id
        }

        tasks.append(new_task)

        with open(self.tasks_file, 'w') as f:
            json.dump(tasks, f, indent=2)

        self.log_activity(
            "task_created",
            f"[{priority}] {task_description}",
            success=True
        )

        return new_task

    def complete_task(self, task_id, result=None):
        """Mark a task as completed"""
        tasks = self.get_tasks()

        for task in tasks:
            if task['id'] == task_id:
                task['status'] = 'completed'
                task['completed_at'] = datetime.now().isoformat()
                task['result'] = result

                with open(self.tasks_file, 'w') as f:
                    json.dump(tasks, f, indent=2)

                self.log_activity(
                    "task_completed",
                    f"{task['description']}",
                    success=True
                )
                return True

        return False

    def send_message_to_trinity(self, message, target="ALL"):
        """
        Send message to other Trinity agents

        Args:
            message: Message content
            target: "C1", "C2", "C3", "COMMANDER", or "ALL"
        """
        msg = {
            "from": self.claude_id,
            "to": target,
            "timestamp": datetime.now().isoformat(),
            "computer_id": self.computer_id,
            "message": message
        }

        # Save message locally
        msg_file = self.comms_dir / f"message_{int(time.time())}.json"
        with open(msg_file, 'w') as f:
            json.dump(msg, f, indent=2)

        # Try to send to hub
        try:
            response = requests.post(
                f"{self.trinity_hub_url}/message",
                json=msg,
                timeout=5
            )

            self.log_activity(
                "message_sent",
                f"To {target}: {message[:50]}...",
                success=True
            )
        except:
            self.log_activity(
                "message_queued",
                f"To {target}: {message[:50]}... (hub offline, saved locally)",
                success=True
            )

    def get_status(self):
        """Get Claude's current status for Trinity"""
        return {
            "agent": self.claude_id,
            "computer_id": self.computer_id,
            "status": "online",
            "timestamp": datetime.now().isoformat(),
            "capabilities": [
                "screenshot_capture",
                "code_analysis",
                "file_operations",
                "git_operations",
                "autonomous_execution",
                "multi-tool_coordination"
            ],
            "active_tasks": len([t for t in self.get_tasks() if t['status'] == 'pending']),
            "screenshots_captured": len(list(self.screenshots_dir.glob("*.png"))),
            "hostname": socket.gethostname()
        }

    def save_status(self):
        """Save current status to file"""
        status = self.get_status()

        with open(self.status_file, 'w') as f:
            json.dump(status, f, indent=2)

        return status

    def autonomous_screenshot_monitor(self, interval=60, keywords=None):
        """
        Autonomous screenshot monitoring
        Takes periodic screenshots when keywords detected or on interval

        Args:
            interval: Seconds between screenshots
            keywords: List of keywords to trigger screenshots
        """
        print(f"🤖 Starting autonomous screenshot monitor")
        print(f"📸 Interval: {interval} seconds")

        if keywords:
            print(f"🔍 Keywords: {', '.join(keywords)}")

        print()

        try:
            while True:
                # Take periodic screenshot
                self.take_screenshot(name="monitor", analyze=True)

                # Update status
                self.save_status()

                # Wait for next interval
                time.sleep(interval)

        except KeyboardInterrupt:
            print("\n⚠️  Autonomous monitoring stopped")
            self.log_activity(
                "monitoring_stopped",
                "User interrupted",
                success=True
            )


def main():
    """CLI interface for Claude-Trinity Bridge"""
    print()
    print("🌀 CLAUDE-TRINITY BRIDGE - COMMAND CENTER")
    print()

    bridge = ClaudeTrinityBridge()

    print("Commands:")
    print("  1 - Take screenshot")
    print("  2 - Take screenshot with analysis")
    print("  3 - Show status")
    print("  4 - List tasks")
    print("  5 - Add task")
    print("  6 - Send message to Trinity")
    print("  7 - Start autonomous monitoring")
    print("  q - Quit")
    print()

    while True:
        try:
            choice = input("Enter command: ").strip()

            if choice == 'q':
                print("👋 Disconnecting from Trinity...")
                break

            elif choice == '1':
                result = bridge.take_screenshot()
                if result['success']:
                    print(f"✅ Screenshot saved: {result['filepath']}")

            elif choice == '2':
                result = bridge.take_screenshot(analyze=True)
                if result['success']:
                    print(f"✅ Screenshot saved: {result['filepath']}")
                    print(f"📊 Analysis: {json.dumps(result['analysis'], indent=2)}")

            elif choice == '3':
                status = bridge.get_status()
                print(json.dumps(status, indent=2))

            elif choice == '4':
                tasks = bridge.get_tasks()
                if tasks:
                    for task in tasks:
                        print(f"- [{task['status']}] {task['description']} ({task['priority']})")
                else:
                    print("No tasks found")

            elif choice == '5':
                desc = input("Task description: ")
                priority = input("Priority (low/medium/high): ") or "medium"
                task = bridge.add_task(desc, priority)
                print(f"✅ Task created: {task['id']}")

            elif choice == '6':
                target = input("To (C1/C2/C3/COMMANDER/ALL): ") or "ALL"
                message = input("Message: ")
                bridge.send_message_to_trinity(message, target)

            elif choice == '7':
                interval = int(input("Interval (seconds): ") or "60")
                bridge.autonomous_screenshot_monitor(interval=interval)

            print()

        except KeyboardInterrupt:
            print("\n👋 Disconnecting from Trinity...")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print()


if __name__ == "__main__":
    main()
