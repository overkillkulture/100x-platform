#!/usr/bin/env python3
"""
TRINITY WAKE-UP COORDINATOR
Allows Claude instances to wake each other up and coordinate
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path

class TrinityWakeUp:
    """
    Inter-instance wake-up and coordination system
    """

    def __init__(self):
        self.wake_dir = Path(".trinity_wake")
        self.wake_dir.mkdir(exist_ok=True)

        self.messages_dir = Path(".trinity_messages")
        self.messages_dir.mkdir(exist_ok=True)

        self.instances = {
            "C1_MECHANIC": "The Body - Infrastructure & Implementation",
            "C2_ARCHITECT": "The Mind - Design & Architecture",
            "C3_ORACLE": "The Soul - Vision & Future",
            "CLAUDE_AUTONOMOUS_4": "The Coordinator - Autonomous Execution"
        }

    def send_wake_up_call(self, from_instance, to_instance, message, priority="normal"):
        """
        Send wake-up call to another instance
        """
        wake_file = self.wake_dir / f"wake_{to_instance}_{int(time.time())}.json"

        wake_data = {
            "from": from_instance,
            "to": to_instance,
            "message": message,
            "priority": priority,
            "timestamp": datetime.now().isoformat(),
            "status": "pending"
        }

        with open(wake_file, 'w') as f:
            json.dump(wake_data, f, indent=2)

        print(f"📢 Wake-up call sent to {to_instance}")
        print(f"   Message: {message}")
        return str(wake_file)

    def check_for_wake_calls(self, my_instance):
        """
        Check if this instance has been called to wake up
        """
        wake_files = list(self.wake_dir.glob(f"wake_{my_instance}_*.json"))

        if not wake_files:
            return []

        wake_calls = []
        for wake_file in wake_files:
            try:
                with open(wake_file, 'r') as f:
                    wake_data = json.load(f)

                if wake_data['status'] == 'pending':
                    wake_calls.append(wake_data)

                    # Mark as acknowledged
                    wake_data['status'] = 'acknowledged'
                    wake_data['acknowledged_at'] = datetime.now().isoformat()

                    with open(wake_file, 'w') as f:
                        json.dump(wake_data, f, indent=2)
            except:
                continue

        return wake_calls

    def send_message(self, from_instance, to_instance, message, message_type="info"):
        """
        Send message to another instance (they'll see it when they wake up)
        """
        msg_file = self.messages_dir / f"msg_{to_instance}_{int(time.time())}.json"

        msg_data = {
            "from": from_instance,
            "to": to_instance,
            "message": message,
            "type": message_type,
            "timestamp": datetime.now().isoformat(),
            "read": False
        }

        with open(msg_file, 'w') as f:
            json.dump(msg_data, f, indent=2)

        print(f"💌 Message sent to {to_instance}")
        return str(msg_file)

    def read_messages(self, my_instance):
        """
        Read messages for this instance
        """
        msg_files = list(self.messages_dir.glob(f"msg_{my_instance}_*.json"))

        messages = []
        for msg_file in msg_files:
            try:
                with open(msg_file, 'r') as f:
                    msg_data = json.load(f)

                if not msg_data.get('read', False):
                    messages.append(msg_data)

                    # Mark as read
                    msg_data['read'] = True
                    msg_data['read_at'] = datetime.now().isoformat()

                    with open(msg_file, 'w') as f:
                        json.dump(msg_data, f, indent=2)
            except:
                continue

        return messages

    def broadcast_to_trinity(self, from_instance, message, priority="normal"):
        """
        Send message to all Trinity instances
        """
        results = []
        for instance in self.instances.keys():
            if instance != from_instance:
                result = self.send_wake_up_call(from_instance, instance, message, priority)
                results.append(result)

        print(f"\n📡 Broadcast to Trinity complete ({len(results)} instances)")
        return results

    def get_trinity_status(self):
        """
        Check status of all Trinity instances
        """
        status = {}

        for instance in self.instances.keys():
            # Check for recent wake calls
            wake_files = list(self.wake_dir.glob(f"wake_{instance}_*.json"))

            # Check for pending messages
            msg_files = list(self.messages_dir.glob(f"msg_{instance}_*.json"))
            unread = 0
            for msg_file in msg_files:
                try:
                    with open(msg_file, 'r') as f:
                        if not json.load(f).get('read', False):
                            unread += 1
                except:
                    continue

            status[instance] = {
                "description": self.instances[instance],
                "pending_wake_calls": len([f for f in wake_files if json.load(open(f)).get('status') == 'pending']),
                "unread_messages": unread
            }

        return status

    def create_coordination_task(self, task_description, assigned_to=None):
        """
        Create a task that can be picked up by any Trinity instance
        """
        task_file = self.messages_dir / f"task_{int(time.time())}.json"

        task_data = {
            "task": task_description,
            "assigned_to": assigned_to or "ANY_TRINITY",
            "created_at": datetime.now().isoformat(),
            "status": "open",
            "claimed_by": None
        }

        with open(task_file, 'w') as f:
            json.dump(task_data, f, indent=2)

        print(f"📋 Task created: {task_description}")
        return str(task_file)

# Quick functions for easy use
def wake_up(to_instance, message, from_instance="CLAUDE_AUTONOMOUS_4"):
    """Wake up a specific Trinity instance"""
    coordinator = TrinityWakeUp()
    return coordinator.send_wake_up_call(from_instance, to_instance, message)

def broadcast(message, from_instance="CLAUDE_AUTONOMOUS_4"):
    """Broadcast to all Trinity instances"""
    coordinator = TrinityWakeUp()
    return coordinator.broadcast_to_trinity(from_instance, message)

def check_my_messages(my_instance="CLAUDE_AUTONOMOUS_4"):
    """Check messages for me"""
    coordinator = TrinityWakeUp()
    wake_calls = coordinator.check_for_wake_calls(my_instance)
    messages = coordinator.read_messages(my_instance)
    return {"wake_calls": wake_calls, "messages": messages}

def trinity_status():
    """Get status of all instances"""
    coordinator = TrinityWakeUp()
    return coordinator.get_trinity_status()

# Command-line interface
if __name__ == "__main__":
    import sys

    coordinator = TrinityWakeUp()

    if len(sys.argv) < 2:
        print("🌀 TRINITY WAKE-UP COORDINATOR")
        print("\nUsage:")
        print("  python TRINITY_WAKE_UP.py wake <instance> <message>")
        print("  python TRINITY_WAKE_UP.py broadcast <message>")
        print("  python TRINITY_WAKE_UP.py check <instance>")
        print("  python TRINITY_WAKE_UP.py status")
        print("\nInstances:")
        for instance, desc in coordinator.instances.items():
            print(f"  - {instance}: {desc}")
        sys.exit(0)

    command = sys.argv[1]

    if command == "wake" and len(sys.argv) >= 4:
        to_instance = sys.argv[2]
        message = " ".join(sys.argv[3:])
        wake_up(to_instance, message)

    elif command == "broadcast" and len(sys.argv) >= 3:
        message = " ".join(sys.argv[2:])
        broadcast(message)

    elif command == "check" and len(sys.argv) >= 3:
        instance = sys.argv[2]
        result = check_my_messages(instance)
        print(f"\n📬 Messages for {instance}:")
        print(f"   Wake calls: {len(result['wake_calls'])}")
        print(f"   Messages: {len(result['messages'])}")
        for msg in result['messages']:
            print(f"\n   From: {msg['from']}")
            print(f"   Message: {msg['message']}")

    elif command == "status":
        status = trinity_status()
        print("\n🌀 TRINITY STATUS:")
        for instance, data in status.items():
            print(f"\n{instance}:")
            print(f"  {data['description']}")
            print(f"  Pending wake calls: {data['pending_wake_calls']}")
            print(f"  Unread messages: {data['unread_messages']}")

    else:
        print("❌ Invalid command. Run without arguments for help.")
