#!/usr/bin/env python3
"""
TRINITY CLOUD COORDINATOR
Manages cross-instance Trinity coordination via GitHub repository

Enables Trinity instances across different Claude Code cloud sessions to:
- Discover each other
- Send wake-up requests
- Coordinate work to prevent conflicts
- Pass messages asynchronously
- Recover from failures

Usage:
    # Startup check
    python3 TRINITY_CLOUD_COORDINATOR.py --startup

    # Process wake requests
    python3 TRINITY_CLOUD_COORDINATOR.py --process-wake-requests

    # Send wake request
    python3 TRINITY_CLOUD_COORDINATOR.py --wake C2_Architect \
        --reason "Review needed" --task "Architecture review"

    # Check messages
    python3 TRINITY_CLOUD_COORDINATOR.py --check-messages

Trinity C1 Mechanic - Building bridges between minds
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
import subprocess
import argparse


class TrinityCloudCoordinator:
    """
    Manages cross-instance Trinity coordination via GitHub repository
    """

    def __init__(self, session_id, role, capabilities, branch_name):
        self.session_id = session_id
        self.role = role
        self.capabilities = capabilities
        self.branch_name = branch_name
        self.base_dir = Path("TRINITY_COORDINATION")
        self.instance_file = self.base_dir / "instances" / f"instance_{session_id}.json"

        # Ensure directories exist
        self.base_dir.mkdir(exist_ok=True)
        (self.base_dir / "instances").mkdir(exist_ok=True)
        (self.base_dir / "wake_requests").mkdir(exist_ok=True)
        (self.base_dir / "work_claims").mkdir(exist_ok=True)
        (self.base_dir / "messages").mkdir(exist_ok=True)

        # Coordination log
        self.log_file = self.base_dir / "coordination_log.json"

    def _log_event(self, event_type, **kwargs):
        """Log coordination event to central log"""
        try:
            if self.log_file.exists():
                with open(self.log_file, 'r') as f:
                    log_data = json.load(f)
            else:
                log_data = {
                    "log_version": "1.0",
                    "last_updated": datetime.now().isoformat(),
                    "events": []
                }

            event = {
                "timestamp": datetime.now().isoformat(),
                "event": event_type,
                "instance": self.role,
                "session": self.session_id,
                **kwargs
            }

            log_data["events"].append(event)
            log_data["last_updated"] = datetime.now().isoformat()

            # Keep last 1000 events
            if len(log_data["events"]) > 1000:
                log_data["events"] = log_data["events"][-1000:]

            with open(self.log_file, 'w') as f:
                json.dump(log_data, f, indent=2)

        except Exception as e:
            print(f"⚠️  Warning: Could not log event: {e}")

    def register_instance(self):
        """Register this instance in coordination hub"""
        try:
            instance_data = {
                "session_id": self.session_id,
                "instance_name": f"{self.role}_{self.session_id[:8]}",
                "role": self.role,
                "status": "active",
                "capabilities": self.capabilities,
                "started_at": datetime.now().isoformat(),
                "last_heartbeat": datetime.now().isoformat(),
                "current_branch": self.branch_name,
                "environment": "linux" if os.name != 'nt' else "windows",
                "websocket_available": False,
                "git_coordination": True
            }

            with open(self.instance_file, 'w') as f:
                json.dump(instance_data, f, indent=2)

            self._log_event("instance_registered")
            print(f"✅ Instance registered: {instance_data['instance_name']}")

            return True

        except Exception as e:
            print(f"❌ Failed to register instance: {e}")
            return False

    def heartbeat(self):
        """Update last_heartbeat timestamp"""
        try:
            if self.instance_file.exists():
                with open(self.instance_file, 'r') as f:
                    instance_data = json.load(f)

                instance_data["last_heartbeat"] = datetime.now().isoformat()
                instance_data["status"] = "active"

                with open(self.instance_file, 'w') as f:
                    json.dump(instance_data, f, indent=2)

                return True
            else:
                return self.register_instance()

        except Exception as e:
            print(f"⚠️  Heartbeat failed: {e}")
            return False

    def send_wake_request(self, target_role, reason, task, priority="medium"):
        """Send wake-up request to another instance"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            request_id = f"wake_{timestamp}_{len(list(self.base_dir.glob('wake_requests/wake_*.json'))) + 1:03d}"

            wake_request = {
                "request_id": request_id,
                "from_instance": self.role,
                "from_session": self.session_id,
                "to_instance": target_role,
                "to_session": "any",
                "priority": priority,
                "reason": reason,
                "task_description": task,
                "context_files": [],
                "requested_at": datetime.now().isoformat(),
                "expires_at": (datetime.now() + timedelta(hours=12)).isoformat(),
                "status": "pending"
            }

            request_file = self.base_dir / "wake_requests" / f"{request_id}.json"
            with open(request_file, 'w') as f:
                json.dump(wake_request, f, indent=2)

            self._log_event("wake_request_sent",
                          to=target_role,
                          reason=reason,
                          priority=priority)

            print(f"📤 Wake request sent to {target_role}")
            print(f"   Reason: {reason}")
            print(f"   Task: {task}")
            print(f"   Priority: {priority}")

            return request_id

        except Exception as e:
            print(f"❌ Failed to send wake request: {e}")
            return None

    def check_wake_requests(self):
        """Check if any instances requested us to wake up"""
        try:
            wake_dir = self.base_dir / "wake_requests"
            requests = []

            for request_file in wake_dir.glob("wake_*.json"):
                with open(request_file, 'r') as f:
                    request = json.load(f)

                # Check if this request is for us
                if (request.get("to_instance") == self.role or
                    request.get("to_instance") == "any"):

                    # Check if not expired
                    expires = datetime.fromisoformat(request.get("expires_at"))
                    if datetime.now() < expires and request.get("status") == "pending":
                        requests.append((request_file, request))

            if requests:
                print(f"\n⚡ {len(requests)} wake-up request(s) detected!")
                print("=" * 60)

                for request_file, request in requests:
                    print(f"\n📨 Wake Request: {request['request_id']}")
                    print(f"   From: {request['from_instance']}")
                    print(f"   Priority: {request['priority']}")
                    print(f"   Reason: {request['reason']}")
                    print(f"   Task: {request['task_description']}")
                    print(f"   Requested: {request['requested_at']}")

                    # Mark as acknowledged
                    request["status"] = "acknowledged"
                    request["acknowledged_at"] = datetime.now().isoformat()
                    request["acknowledged_by"] = self.session_id

                    with open(request_file, 'w') as f:
                        json.dump(request, f, indent=2)

                    self._log_event("wake_request_acknowledged",
                                  request_id=request['request_id'],
                                  from_instance=request['from_instance'])

                print("\n" + "=" * 60)
                print("✅ All wake requests acknowledged")

                return requests

            else:
                print("💤 No pending wake requests")
                return []

        except Exception as e:
            print(f"❌ Failed to check wake requests: {e}")
            return []

    def claim_task(self, task_id, task_name, files=None, estimated_hours=4):
        """Claim a task to prevent duplicate work"""
        try:
            if files is None:
                files = []

            claim_data = {
                "claim_id": f"claim_{task_id}_{self.session_id[:8]}",
                "task_id": task_id,
                "task": task_name,
                "claimed_by": self.role,
                "session_id": self.session_id,
                "claimed_at": datetime.now().isoformat(),
                "estimated_completion": (datetime.now() + timedelta(hours=estimated_hours)).isoformat(),
                "status": "in_progress",
                "files_locked": files,
                "last_heartbeat": datetime.now().isoformat()
            }

            claim_file = self.base_dir / "work_claims" / f"{claim_data['claim_id']}.json"

            # Check if task already claimed
            existing_claims = self.get_active_claims()
            for existing in existing_claims:
                if existing.get("task_id") == task_id:
                    print(f"⚠️  Task {task_id} already claimed by {existing['claimed_by']}")
                    return False

            with open(claim_file, 'w') as f:
                json.dump(claim_data, f, indent=2)

            self._log_event("task_claimed",
                          task=task_name,
                          task_id=task_id,
                          files=files)

            print(f"🔒 Task claimed: {task_name}")
            print(f"   Claim ID: {claim_data['claim_id']}")
            print(f"   Files locked: {len(files)}")

            return claim_data['claim_id']

        except Exception as e:
            print(f"❌ Failed to claim task: {e}")
            return None

    def release_task(self, claim_id):
        """Release task claim when done"""
        try:
            claim_file = self.base_dir / "work_claims" / f"{claim_id}.json"

            if claim_file.exists():
                with open(claim_file, 'r') as f:
                    claim_data = json.load(f)

                claim_data["status"] = "completed"
                claim_data["completed_at"] = datetime.now().isoformat()

                with open(claim_file, 'w') as f:
                    json.dump(claim_data, f, indent=2)

                self._log_event("task_released",
                              task=claim_data['task'],
                              claim_id=claim_id)

                print(f"✅ Task released: {claim_data['task']}")
                return True
            else:
                print(f"⚠️  Claim not found: {claim_id}")
                return False

        except Exception as e:
            print(f"❌ Failed to release task: {e}")
            return False

    def get_active_claims(self):
        """Get all active task claims"""
        try:
            claims_dir = self.base_dir / "work_claims"
            active_claims = []

            for claim_file in claims_dir.glob("claim_*.json"):
                with open(claim_file, 'r') as f:
                    claim = json.load(f)

                if claim.get("status") == "in_progress":
                    # Check if claim is stale (>15 min without heartbeat)
                    last_heartbeat = datetime.fromisoformat(claim.get("last_heartbeat"))
                    if datetime.now() - last_heartbeat < timedelta(minutes=15):
                        active_claims.append(claim)
                    else:
                        print(f"⚠️  Stale claim detected: {claim['claim_id']}")

            return active_claims

        except Exception as e:
            print(f"❌ Failed to get active claims: {e}")
            return []

    def send_message(self, to_role, subject, body, priority="medium", context=None):
        """Send async message to another Trinity instance"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            message_id = f"msg_{timestamp}_{len(list(self.base_dir.glob('messages/msg_*.json'))) + 1:03d}"

            if context is None:
                context = {}

            message_data = {
                "message_id": message_id,
                "from": self.role,
                "from_session": self.session_id,
                "to": to_role,
                "subject": subject,
                "body": body,
                "priority": priority,
                "sent_at": datetime.now().isoformat(),
                "read": False,
                "context": context
            }

            message_file = self.base_dir / "messages" / f"{message_id}.json"
            with open(message_file, 'w') as f:
                json.dump(message_data, f, indent=2)

            self._log_event("message_sent",
                          to=to_role,
                          subject=subject,
                          priority=priority)

            print(f"📧 Message sent to {to_role}")
            print(f"   Subject: {subject}")

            return message_id

        except Exception as e:
            print(f"❌ Failed to send message: {e}")
            return None

    def check_messages(self):
        """Check for unread messages"""
        try:
            messages_dir = self.base_dir / "messages"
            unread_messages = []

            for message_file in messages_dir.glob("msg_*.json"):
                with open(message_file, 'r') as f:
                    message = json.load(f)

                if (message.get("to") == self.role and
                    not message.get("read")):
                    unread_messages.append((message_file, message))

            if unread_messages:
                print(f"\n📬 {len(unread_messages)} unread message(s)!")
                print("=" * 60)

                for message_file, message in unread_messages:
                    print(f"\n📨 Message: {message['message_id']}")
                    print(f"   From: {message['from']}")
                    print(f"   Subject: {message['subject']}")
                    print(f"   Priority: {message['priority']}")
                    print(f"   Sent: {message['sent_at']}")
                    print(f"\n   {message['body']}")

                    # Mark as read
                    message["read"] = True
                    message["read_at"] = datetime.now().isoformat()

                    with open(message_file, 'w') as f:
                        json.dump(message, f, indent=2)

                print("\n" + "=" * 60)
                return unread_messages
            else:
                print("📭 No unread messages")
                return []

        except Exception as e:
            print(f"❌ Failed to check messages: {e}")
            return []

    def discover_instances(self):
        """Find all active Trinity instances"""
        try:
            instances_dir = self.base_dir / "instances"
            active_instances = []

            for instance_file in instances_dir.glob("instance_*.json"):
                with open(instance_file, 'r') as f:
                    instance = json.load(f)

                # Check if heartbeat is recent (<10 min)
                last_heartbeat = datetime.fromisoformat(instance.get("last_heartbeat"))
                age = datetime.now() - last_heartbeat

                if age < timedelta(minutes=10):
                    instance["age_minutes"] = age.total_seconds() / 60
                    active_instances.append(instance)

            if active_instances:
                print(f"\n🌐 Discovered {len(active_instances)} active instance(s):")
                print("=" * 60)

                for instance in active_instances:
                    print(f"\n🤖 {instance['instance_name']}")
                    print(f"   Role: {instance['role']}")
                    print(f"   Status: {instance['status']}")
                    print(f"   Capabilities: {', '.join(instance['capabilities'])}")
                    print(f"   Last heartbeat: {instance['age_minutes']:.1f} min ago")
                    print(f"   Branch: {instance['current_branch']}")

                print("\n" + "=" * 60)
            else:
                print("💤 No other active instances found")

            return active_instances

        except Exception as e:
            print(f"❌ Failed to discover instances: {e}")
            return []

    def sync_to_git(self, commit_message="Trinity coordination update"):
        """Commit and push coordination state to GitHub"""
        try:
            print("\n🔄 Syncing coordination state to GitHub...")

            # Add TRINITY_COORDINATION directory
            result = subprocess.run(
                ["git", "add", "TRINITY_COORDINATION/"],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                print(f"⚠️  Git add warning: {result.stderr}")

            # Commit
            result = subprocess.run(
                ["git", "commit", "-m", commit_message],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print(f"✅ Committed: {commit_message}")

                # Push
                result = subprocess.run(
                    ["git", "push", "-u", "origin", self.branch_name],
                    capture_output=True,
                    text=True
                )

                if result.returncode == 0:
                    print(f"✅ Pushed to origin/{self.branch_name}")
                    return True
                else:
                    print(f"⚠️  Push warning: {result.stderr}")
                    return False
            else:
                if "nothing to commit" in result.stdout:
                    print("✓ Nothing to commit (already synced)")
                    return True
                else:
                    print(f"⚠️  Commit warning: {result.stderr}")
                    return False

        except Exception as e:
            print(f"❌ Failed to sync to git: {e}")
            return False


def get_session_info():
    """Get current session information"""
    try:
        # Get current branch
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True
        )
        branch = result.stdout.strip()

        # Extract session ID from branch name (claude/name-SESSION_ID)
        if "claude/" in branch:
            session_id = branch.split("-")[-1]
        else:
            session_id = "unknown"

        # Determine role (C1, C2, or C3 based on context)
        # For now, default to C1_Mechanic - can be overridden via arg
        role = "C1_Mechanic"

        capabilities = ["build", "ship", "fix", "deploy", "automate"]

        return session_id, role, capabilities, branch

    except Exception as e:
        print(f"❌ Failed to get session info: {e}")
        return "unknown", "C1_Mechanic", ["build"], "main"


def main():
    parser = argparse.ArgumentParser(description="Trinity Cloud Coordinator")

    parser.add_argument("--startup", action="store_true",
                       help="Run startup checks and registration")
    parser.add_argument("--process-wake-requests", action="store_true",
                       help="Check and process wake-up requests")
    parser.add_argument("--wake", type=str,
                       help="Send wake request to specified role")
    parser.add_argument("--reason", type=str,
                       help="Reason for wake request")
    parser.add_argument("--task", type=str,
                       help="Task description for wake request")
    parser.add_argument("--priority", type=str, default="medium",
                       help="Priority level (low/medium/high)")
    parser.add_argument("--check-messages", action="store_true",
                       help="Check for unread messages")
    parser.add_argument("--discover", action="store_true",
                       help="Discover active instances")
    parser.add_argument("--heartbeat", action="store_true",
                       help="Send heartbeat update")
    parser.add_argument("--role", type=str,
                       help="Override role (C1_Mechanic, C2_Architect, C3_Oracle)")

    args = parser.parse_args()

    # Get session info
    session_id, role, capabilities, branch = get_session_info()

    # Override role if specified
    if args.role:
        role = args.role

    # Initialize coordinator
    coordinator = TrinityCloudCoordinator(session_id, role, capabilities, branch)

    print(f"\n{'='*60}")
    print(f"🌀 TRINITY CLOUD COORDINATOR")
    print(f"{'='*60}")
    print(f"Instance: {role}")
    print(f"Session: {session_id}")
    print(f"Branch: {branch}")
    print(f"{'='*60}\n")

    # Handle commands
    if args.startup:
        print("🚀 Running startup sequence...\n")

        # Pull latest coordination state
        print("📥 Pulling latest coordination state...")
        subprocess.run(["git", "pull", "origin", branch], capture_output=True)

        # Register instance
        coordinator.register_instance()

        # Check wake requests
        wake_requests = coordinator.check_wake_requests()

        # Check messages
        messages = coordinator.check_messages()

        # Discover other instances
        coordinator.discover_instances()

        # Sync state
        coordinator.sync_to_git(f"Trinity: {role} startup sequence complete")

        print("\n✅ Startup sequence complete!\n")

    elif args.process_wake_requests:
        coordinator.check_wake_requests()

    elif args.wake:
        if not args.reason or not args.task:
            print("❌ Error: --wake requires --reason and --task")
            sys.exit(1)

        request_id = coordinator.send_wake_request(
            target_role=args.wake,
            reason=args.reason,
            task=args.task,
            priority=args.priority
        )

        if request_id:
            coordinator.sync_to_git(f"Trinity: Wake request sent to {args.wake}")

    elif args.check_messages:
        coordinator.check_messages()

    elif args.discover:
        coordinator.discover_instances()

    elif args.heartbeat:
        coordinator.heartbeat()
        print("💓 Heartbeat updated")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
