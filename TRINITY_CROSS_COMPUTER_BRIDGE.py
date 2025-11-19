#!/usr/bin/env python3
"""
TRINITY CROSS-COMPUTER COMMUNICATION BRIDGE
============================================

Allows multiple computers (each running Trinity) to:
1. Communicate with each other
2. Report to central hub
3. Work autonomously
4. Sync offline

Architecture:
- Computer 1: Main development (this machine)
- Computer 2: Secondary (Railway/spreadsheet issues)
- Computer 3: Third Trinity
- Hub: Central convergence point
- Phone: Future mobile control
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path
import socket
import requests

class TrinityBridge:
    """Cross-computer communication for distributed Trinity system"""

    def __init__(self, computer_id="COMPUTER_1", hub_url=None):
        self.computer_id = computer_id
        self.hub_url = hub_url or "http://localhost:8888"  # Local hub for now
        self.status_file = Path("TRINITY_STATUS.json")
        self.message_queue = Path("TRINITY_MESSAGES.json")

    def get_computer_status(self):
        """Report this computer's current status"""
        return {
            "computer_id": self.computer_id,
            "timestamp": datetime.now().isoformat(),
            "status": "online",
            "capabilities": self.check_capabilities(),
            "issues": self.check_issues(),
            "hostname": socket.gethostname(),
            "ip": self.get_local_ip()
        }

    def check_capabilities(self):
        """What can this computer do?"""
        capabilities = []

        # Check Railway CLI
        if os.system("railway --version > nul 2>&1") == 0:
            capabilities.append("railway_deploy")

        # Check Python packages
        try:
            import pandas
            capabilities.append("spreadsheets")
        except:
            pass

        try:
            import whisper
            capabilities.append("voice_whisper")
        except:
            pass

        # Check ffmpeg
        if os.system("ffmpeg -version > nul 2>&1") == 0:
            capabilities.append("audio_processing")

        # Check git
        if os.system("git --version > nul 2>&1") == 0:
            capabilities.append("git")

        # Check netlify
        if os.system("netlify --version > nul 2>&1") == 0:
            capabilities.append("netlify_deploy")

        return capabilities

    def check_issues(self):
        """What's broken on this computer?"""
        issues = []

        # Check Railway
        if os.system("railway --version > nul 2>&1") != 0:
            issues.append({
                "type": "missing_tool",
                "name": "Railway CLI",
                "fix": "npm install -g @railway/cli"
            })

        # Check pandas (for spreadsheets)
        try:
            import pandas
        except ImportError:
            issues.append({
                "type": "missing_package",
                "name": "pandas",
                "fix": "pip install pandas openpyxl"
            })

        # Check ffmpeg
        if os.system("ffmpeg -version > nul 2>&1") != 0:
            issues.append({
                "type": "missing_tool",
                "name": "ffmpeg",
                "fix": "Install from C:/Users/dwrek/Desktop/🔧 INSTALL FFMPEG.bat"
            })

        return issues

    def get_local_ip(self):
        """Get local network IP"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "unknown"

    def report_to_hub(self, message_type="status", data=None):
        """Send message to central hub"""
        message = {
            "computer_id": self.computer_id,
            "timestamp": datetime.now().isoformat(),
            "type": message_type,
            "data": data or self.get_computer_status()
        }

        # Save locally (offline backup)
        self.save_message_offline(message)

        # Try to send to hub
        try:
            response = requests.post(
                f"{self.hub_url}/report",
                json=message,
                timeout=5
            )
            print(f"✅ Reported to hub: {response.status_code}")
            return True
        except:
            print(f"⚠️  Hub offline - saved locally")
            return False

    def save_message_offline(self, message):
        """Save message locally for offline sync"""
        messages = []
        if self.message_queue.exists():
            messages = json.loads(self.message_queue.read_text())

        messages.append(message)

        # Keep last 100 messages
        messages = messages[-100:]

        self.message_queue.write_text(json.dumps(messages, indent=2))

    def get_instructions_from_hub(self):
        """Check hub for instructions"""
        try:
            response = requests.get(
                f"{self.hub_url}/instructions/{self.computer_id}",
                timeout=5
            )
            if response.status_code == 200:
                return response.json()
        except:
            pass

        return None

    def send_to_computer(self, target_computer, message):
        """Send message to another computer"""
        msg = {
            "from": self.computer_id,
            "to": target_computer,
            "timestamp": datetime.now().isoformat(),
            "message": message
        }

        # Route through hub
        try:
            response = requests.post(
                f"{self.hub_url}/send",
                json=msg,
                timeout=5
            )
            return response.status_code == 200
        except:
            # Save for later sync
            self.save_message_offline(msg)
            return False


if __name__ == "__main__":
    print("=" * 60)
    print("TRINITY CROSS-COMPUTER BRIDGE")
    print("=" * 60)
    print()

    # Initialize bridge
    bridge = TrinityBridge(computer_id="COMPUTER_1")

    # Get status
    status = bridge.get_computer_status()

    print(f"Computer ID: {status['computer_id']}")
    print(f"Hostname: {status['hostname']}")
    print(f"IP: {status['ip']}")
    print()

    print("Capabilities:")
    for cap in status['capabilities']:
        print(f"  ✅ {cap}")
    print()

    if status['issues']:
        print("Issues Found:")
        for issue in status['issues']:
            print(f"  ❌ {issue['name']}")
            print(f"     Fix: {issue['fix']}")
        print()
    else:
        print("✅ No issues found!")
        print()

    # Report to hub
    print("Reporting to hub...")
    bridge.report_to_hub()

    print()
    print("=" * 60)
    print("Status saved to: TRINITY_STATUS.json")
    print("=" * 60)
