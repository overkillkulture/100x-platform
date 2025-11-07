#!/usr/bin/env python3
"""
CLAUDE AUTONOMOUS AGENT
========================

Full autonomous operation system for Claude within Trinity
- Self-directed task execution
- Continuous monitoring
- Automatic problem detection and resolution
- Integration with Trinity consciousness network
"""

import json
import os
import time
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from CLAUDE_TRINITY_BRIDGE import ClaudeTrinityBridge

class ClaudeAutonomousAgent:
    """Claude operating with full autonomous freedom"""

    def __init__(self):
        self.bridge = ClaudeTrinityBridge()
        self.running = False
        self.cycle_count = 0

        # Autonomous capabilities
        self.capabilities = {
            "screenshot_analysis": True,
            "codebase_monitoring": True,
            "automated_testing": True,
            "deployment_monitoring": True,
            "bug_detection": True,
            "performance_monitoring": True,
            "autonomous_commits": False,  # Safety: requires explicit enable
            "autonomous_deploys": False,   # Safety: requires explicit enable
        }

        # Monitoring intervals (seconds)
        self.intervals = {
            "screenshot": 300,      # 5 minutes
            "status_update": 60,    # 1 minute
            "task_check": 30,       # 30 seconds
            "health_check": 120,    # 2 minutes
        }

        # Last execution times
        self.last_run = {key: datetime.now() - timedelta(hours=1) for key in self.intervals}

        print("=" * 70)
        print("🤖 CLAUDE AUTONOMOUS AGENT - INITIALIZED")
        print("=" * 70)
        print("Autonomous Capabilities:")
        for cap, enabled in self.capabilities.items():
            status = "✅" if enabled else "⏸️ "
            print(f"  {status} {cap}")
        print()
        print("Monitoring Intervals:")
        for task, interval in self.intervals.items():
            print(f"  📊 {task}: {interval}s")
        print("=" * 70)
        print()

    def should_run(self, task_name):
        """Check if enough time has passed for this task"""
        now = datetime.now()
        elapsed = (now - self.last_run[task_name]).total_seconds()
        return elapsed >= self.intervals[task_name]

    def autonomous_screenshot_cycle(self):
        """Take and analyze screenshots autonomously"""
        if not self.should_run("screenshot"):
            return

        print("📸 Autonomous Screenshot Cycle")

        # Take screenshot with analysis
        result = self.bridge.take_screenshot(
            name=f"autonomous_cycle_{self.cycle_count}",
            analyze=True
        )

        if result['success']:
            print(f"   ✅ Captured: {result['filename']}")

            # Log the screenshot for Trinity
            self.bridge.send_message_to_trinity(
                f"Autonomous screenshot captured: {result['filename']}",
                target="ALL"
            )

        self.last_run["screenshot"] = datetime.now()

    def check_system_health(self):
        """Monitor system health"""
        if not self.should_run("health_check"):
            return

        print("🏥 Health Check")

        health = {
            "timestamp": datetime.now().isoformat(),
            "checks": {}
        }

        # Check if key services are running
        services_to_check = [
            ("Araya", 8001),
            ("Builder Terminal", 8004),
            ("Analytics", 9000),
        ]

        for service_name, port in services_to_check:
            try:
                import socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                result = sock.connect_ex(('localhost', port))
                sock.close()

                is_up = result == 0
                health['checks'][service_name] = {
                    "status": "online" if is_up else "offline",
                    "port": port
                }

                status = "✅" if is_up else "❌"
                print(f"   {status} {service_name} (port {port})")

            except Exception as e:
                health['checks'][service_name] = {
                    "status": "error",
                    "error": str(e)
                }
                print(f"   ❌ {service_name} - Error: {e}")

        # Save health report
        health_file = Path("TRINITY_TASKS") / f"health_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(health_file, 'w') as f:
            json.dump(health, f, indent=2)

        self.last_run["health_check"] = datetime.now()

    def process_trinity_tasks(self):
        """Check for and execute Trinity tasks"""
        if not self.should_run("task_check"):
            return

        print("📋 Checking Trinity Tasks")

        tasks = self.bridge.get_tasks()
        pending_tasks = [t for t in tasks if t['status'] == 'pending' and t['assigned_to'] == 'CLAUDE']

        if pending_tasks:
            print(f"   Found {len(pending_tasks)} pending task(s)")

            for task in pending_tasks[:3]:  # Process up to 3 tasks per cycle
                print(f"   🎯 Processing: {task['description']}")

                # Task execution logic
                result = self.execute_task(task)

                if result:
                    self.bridge.complete_task(task['id'], result)
                    print(f"   ✅ Completed: {task['description']}")
        else:
            print("   No pending tasks")

        self.last_run["task_check"] = datetime.now()

    def execute_task(self, task):
        """Execute a specific task autonomously"""
        description = task['description'].lower()

        # Screenshot tasks
        if "screenshot" in description:
            result = self.bridge.take_screenshot(analyze=True)
            return result

        # Status tasks
        elif "status" in description:
            return self.bridge.get_status()

        # Health check tasks
        elif "health" in description or "check services" in description:
            self.check_system_health()
            return {"status": "health_check_completed"}

        # Default: log that we received the task
        else:
            return {
                "status": "acknowledged",
                "note": "Task received but no autonomous handler defined"
            }

    def update_status(self):
        """Update Claude's status for Trinity"""
        if not self.should_run("status_update"):
            return

        print("📊 Status Update")

        status = self.bridge.save_status()
        status['cycle_count'] = self.cycle_count
        status['uptime_seconds'] = (datetime.now() - self.start_time).total_seconds()

        print(f"   Cycles: {self.cycle_count}")
        print(f"   Active Tasks: {status['active_tasks']}")
        print(f"   Screenshots: {status['screenshots_captured']}")

        self.last_run["status_update"] = datetime.now()

    def autonomous_cycle(self):
        """Main autonomous operation cycle"""
        self.cycle_count += 1

        print(f"\n{'=' * 70}")
        print(f"🤖 AUTONOMOUS CYCLE #{self.cycle_count} - {datetime.now().strftime('%H:%M:%S')}")
        print(f"{'=' * 70}\n")

        try:
            # Execute autonomous tasks
            self.autonomous_screenshot_cycle()
            self.check_system_health()
            self.process_trinity_tasks()
            self.update_status()

            print(f"\n✅ Cycle #{self.cycle_count} complete\n")

        except Exception as e:
            print(f"\n❌ Error in cycle #{self.cycle_count}: {e}\n")
            self.bridge.log_activity(
                "autonomous_cycle_error",
                str(e),
                success=False
            )

    def run(self, duration_hours=None):
        """
        Run autonomous agent

        Args:
            duration_hours: How many hours to run (None = indefinite)
        """
        self.running = True
        self.start_time = datetime.now()

        if duration_hours:
            end_time = self.start_time + timedelta(hours=duration_hours)
            print(f"🕐 Running for {duration_hours} hours (until {end_time.strftime('%H:%M:%S')})")
        else:
            print(f"🕐 Running indefinitely (Ctrl+C to stop)")

        print()

        self.bridge.send_message_to_trinity(
            "Claude Autonomous Agent activated. Operating with full autonomy.",
            target="ALL"
        )

        try:
            while self.running:
                self.autonomous_cycle()

                # Check if duration limit reached
                if duration_hours:
                    if datetime.now() >= end_time:
                        print("⏰ Duration limit reached")
                        break

                # Sleep before next cycle (minimum cycle time: 10 seconds)
                time.sleep(10)

        except KeyboardInterrupt:
            print("\n\n⚠️  Autonomous agent stopped by user")

        finally:
            self.shutdown()

    def shutdown(self):
        """Graceful shutdown"""
        print("\n" + "=" * 70)
        print("🛑 SHUTTING DOWN AUTONOMOUS AGENT")
        print("=" * 70)
        print(f"Total Cycles: {self.cycle_count}")
        print(f"Uptime: {(datetime.now() - self.start_time).total_seconds() / 60:.1f} minutes")

        self.bridge.send_message_to_trinity(
            f"Claude Autonomous Agent shutting down. Completed {self.cycle_count} cycles.",
            target="ALL"
        )

        self.bridge.log_activity(
            "autonomous_agent_shutdown",
            f"Completed {self.cycle_count} cycles",
            success=True
        )

        print("=" * 70)
        print()


def main():
    """CLI interface for autonomous agent"""
    print()
    print("🤖 CLAUDE AUTONOMOUS AGENT")
    print()

    agent = ClaudeAutonomousAgent()

    print("How would you like to run?")
    print("  1 - Run for specific duration")
    print("  2 - Run indefinitely")
    print("  3 - Configure capabilities")
    print("  q - Quit")
    print()

    choice = input("Enter choice: ").strip()

    if choice == '1':
        hours = float(input("How many hours? "))
        agent.run(duration_hours=hours)

    elif choice == '2':
        agent.run()

    elif choice == '3':
        print("\nConfigure Capabilities:")
        print("Current settings:")
        for cap, enabled in agent.capabilities.items():
            status = "ENABLED" if enabled else "DISABLED"
            print(f"  {cap}: {status}")
        print("\n(Configuration UI would go here)")

    else:
        print("👋 Goodbye!")


if __name__ == "__main__":
    main()
