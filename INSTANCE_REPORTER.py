#!/usr/bin/env python3
"""
INSTANCE REPORTER - Reports to Central Hub
Run this in each Claude instance to register and coordinate
"""

import requests
import socket
import json
import time
import sys
from datetime import datetime
from pathlib import Path

HUB_URL = "http://localhost:8888"

def get_instance_info():
    """Get info about this instance"""
    instance_id = input("Enter your instance ID (e.g., claude-c1-001): ").strip()
    role = input("Enter your role (C1-Mechanic/C2-Architect/C3-Oracle/C4-7-Specialist): ").strip()

    return {
        "computer_id": f"{socket.gethostname()}-{instance_id}",
        "instance_id": instance_id,
        "role": role,
        "hostname": socket.gethostname(),
        "ip": socket.gethostbyname(socket.gethostname()),
        "timestamp": datetime.now().isoformat(),
        "capabilities": [],
        "issues": [],
        "current_task": None
    }

def report_to_hub(data):
    """Send report to hub"""
    try:
        response = requests.post(f"{HUB_URL}/report", json={"data": data}, timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    print("=" * 60)
    print("🤖 INSTANCE REPORTER")
    print("=" * 60)
    print()

    # Get instance info
    info = get_instance_info()

    print()
    print("Registering with Central Hub...")

    if report_to_hub(info):
        print(f"✅ Registered as {info['instance_id']}")
        print(f"📊 View dashboard: http://localhost:8888")
        print()
        print("Reporting every 30 seconds...")
        print("Press Ctrl+C to stop")
        print()

        # Keep reporting
        while True:
            time.sleep(30)
            info['timestamp'] = datetime.now().isoformat()

            # Update current task
            task_input = input("Current task (or press Enter to skip): ").strip()
            if task_input:
                info['current_task'] = task_input

            if report_to_hub(info):
                print(f"✅ [{datetime.now().strftime('%H:%M:%S')}] Reported to hub")
            else:
                print(f"❌ [{datetime.now().strftime('%H:%M:%S')}] Hub not reachable")
    else:
        print("❌ Could not reach Central Hub")
        print("Is TRINITY_CENTRAL_HUB.py running?")
        print("Run: python3 TRINITY_CENTRAL_HUB.py")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Stopped reporting")
