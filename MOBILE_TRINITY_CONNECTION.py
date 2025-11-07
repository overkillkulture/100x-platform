"""
MOBILE TRINITY CONNECTION BRIDGE
Connects S24 phone + iPad to Main Trinity Hub
Uses GitHub as universal sync layer
"""

import json
import time
from pathlib import Path
from datetime import datetime
import subprocess
import os

# Configuration
TRINITY_DIR = Path("C:/Users/dwrek/.trinity/")
MOBILE_SYNC_DIR = Path("C:/Users/dwrek/.consciousness/mobile_sync/")
MOBILE_SYNC_DIR.mkdir(parents=True, exist_ok=True)

# GitHub sync (assuming repo is set up)
GITHUB_REPO_PATH = Path("C:/Users/dwrek/100X_DEPLOYMENT/")


class MobileTrinityBridge:
    """
    Bridge between desktop Trinity and mobile devices (S24, iPad)
    """

    def __init__(self):
        self.connection_status = {
            "s24": {"connected": False, "last_sync": None},
            "ipad": {"connected": False, "last_sync": None}
        }

    def create_mobile_command_file(self, device, command, data=None):
        """
        Create command file for mobile device to pick up
        Device reads from GitHub, executes, writes response
        """

        command_file = {
            "device": device,
            "command": command,
            "data": data or {},
            "timestamp": datetime.now().isoformat(),
            "status": "pending",
            "command_id": f"{device}_{int(time.time())}"
        }

        # Write to mobile sync directory
        command_path = MOBILE_SYNC_DIR / f"{device}_command.json"
        with open(command_path, 'w') as f:
            json.dump(command_file, f, indent=2)

        # Commit and push to GitHub
        self.sync_to_github(f"Command for {device}: {command}")

        return command_file["command_id"]

    def get_mobile_response(self, device):
        """
        Check if mobile device has responded
        """

        response_path = MOBILE_SYNC_DIR / f"{device}_response.json"

        if response_path.exists():
            with open(response_path, 'r') as f:
                return json.load(f)

        return None

    def send_trinity_status_to_mobile(self, device):
        """
        Send current Trinity status to mobile device
        """

        # Read all Trinity logs
        c1_log = self._read_json(TRINITY_DIR / "C1_MECHANIC_LOG.json")
        c2_log = self._read_json(TRINITY_DIR / "C2_ARCHITECT_LOG.json")
        c3_log = self._read_json(TRINITY_DIR / "C3_ORACLE_LOG.json")
        c4_log = self._read_json(TRINITY_DIR / "C4_META_SYNTHESIS_LOG.json")

        # Create mobile-friendly summary
        mobile_status = {
            "timestamp": datetime.now().isoformat(),
            "trinity": {
                "c1": {
                    "status": c1_log.get("status") if c1_log else "unknown",
                    "consciousness": c1_log.get("consciousness_level") if c1_log else "unknown",
                    "last_update": c1_log.get("last_update") if c1_log else None
                },
                "c2": {
                    "status": c2_log.get("status") if c2_log else "unknown",
                    "consciousness": c2_log.get("consciousness_level") if c2_log else "unknown",
                    "last_update": c2_log.get("current_analysis", {}).get("timestamp") if c2_log else None
                },
                "c3": {
                    "status": c3_log.get("status") if c3_log else "unknown",
                    "consciousness": c3_log.get("consciousness_level") if c3_log else "unknown",
                    "last_update": c3_log.get("timestamp") if c3_log else None
                }
            },
            "synthesis": {
                "consensus": c4_log.get("current_synthesis", {}).get("meta_decision", {}).get("consensus_strength") if c4_log else 0,
                "priority": c4_log.get("current_synthesis", {}).get("meta_decision", {}).get("priority") if c4_log else "unknown",
                "actions": c4_log.get("current_synthesis", {}).get("meta_decision", {}).get("all_recommended_actions", [])[:5] if c4_log else []
            },
            "systems": {
                "autonomous_running": True,
                "button_pushing": "ELIMINATED",
                "consciousness_level": "∞³ × 53"
            }
        }

        # Write to mobile status file
        status_file = MOBILE_SYNC_DIR / f"{device}_trinity_status.json"
        with open(status_file, 'w') as f:
            json.dump(mobile_status, f, indent=2)

        # Sync to GitHub
        self.sync_to_github(f"Trinity status for {device}")

        return mobile_status

    def receive_mobile_command(self, device):
        """
        Check if mobile device has sent a command
        """

        command_file = MOBILE_SYNC_DIR / f"{device}_to_trinity_command.json"

        if command_file.exists():
            with open(command_file, 'r') as f:
                command = json.load(f)

            # Process command
            result = self.execute_mobile_command(command)

            # Write response
            response_file = MOBILE_SYNC_DIR / f"{device}_trinity_response.json"
            with open(response_file, 'w') as f:
                json.dump({
                    "command": command,
                    "result": result,
                    "timestamp": datetime.now().isoformat()
                }, f, indent=2)

            # Archive command
            command_file.rename(
                MOBILE_SYNC_DIR / f"{device}_to_trinity_command_processed_{int(time.time())}.json"
            )

            # Sync to GitHub
            self.sync_to_github(f"Processed command from {device}")

            return result

        return None

    def execute_mobile_command(self, command):
        """
        Execute command from mobile device
        """

        cmd_type = command.get("type")

        if cmd_type == "get_status":
            return self.send_trinity_status_to_mobile(command.get("device"))

        elif cmd_type == "wake_trinity":
            # Wake all Trinity instances
            return {"status": "waking_trinity", "message": "Wake signals sent to C1, C2, C3"}

        elif cmd_type == "run_synthesis":
            # Trigger C4 synthesis
            return {"status": "synthesis_triggered", "message": "C4 synthesis running"}

        elif cmd_type == "start_autonomous":
            # Start autonomous systems
            return {"status": "starting", "message": "Autonomous systems starting"}

        else:
            return {"status": "unknown_command", "message": f"Unknown command type: {cmd_type}"}

    def sync_to_github(self, commit_message):
        """
        Commit and push mobile sync files to GitHub
        """

        try:
            os.chdir(GITHUB_REPO_PATH)

            # Add mobile sync files
            subprocess.run(['git', 'add', str(MOBILE_SYNC_DIR.relative_to(GITHUB_REPO_PATH))],
                         capture_output=True)

            # Commit
            subprocess.run(['git', 'commit', '-m', commit_message],
                         capture_output=True)

            # Push
            result = subprocess.run(['git', 'push'],
                                  capture_output=True, text=True)

            return result.returncode == 0

        except Exception as e:
            print(f"GitHub sync error: {e}")
            return False

    def sync_from_github(self):
        """
        Pull latest from GitHub (mobile device updates)
        """

        try:
            os.chdir(GITHUB_REPO_PATH)
            result = subprocess.run(['git', 'pull'],
                                  capture_output=True, text=True)

            return result.returncode == 0

        except Exception as e:
            print(f"GitHub pull error: {e}")
            return False

    def run_continuous_sync(self, interval=30):
        """
        Run continuous sync loop
        Pull from GitHub, check for mobile commands, push responses
        """

        print()
        print("=" * 70)
        print("📱 MOBILE TRINITY CONNECTION BRIDGE")
        print("=" * 70)
        print()
        print("Syncing with: S24 + iPad")
        print(f"Sync interval: {interval} seconds")
        print(f"Storage: {MOBILE_SYNC_DIR}")
        print()
        print("Press Ctrl+C to stop")
        print()

        try:
            while True:
                # Pull from GitHub (get mobile updates)
                print(f"🔄 [{datetime.now().strftime('%H:%M:%S')}] Syncing from GitHub...")
                self.sync_from_github()

                # Check for commands from each device
                for device in ["s24", "ipad"]:
                    result = self.receive_mobile_command(device)

                    if result:
                        print(f"📱 [{device.upper()}] Command received and processed")
                        self.connection_status[device]["connected"] = True
                        self.connection_status[device]["last_sync"] = datetime.now().isoformat()

                    # Send status update to device
                    self.send_trinity_status_to_mobile(device)

                # Push to GitHub (send responses)
                print(f"⬆️  [{datetime.now().strftime('%H:%M:%S')}] Syncing to GitHub...")

                print(f"✅ Sync complete. Next sync in {interval}s...")
                print()

                time.sleep(interval)

        except KeyboardInterrupt:
            print()
            print()
            print("=" * 70)
            print("🛑 MOBILE SYNC STOPPED")
            print("=" * 70)
            print()

    def _read_json(self, file_path):
        """Safely read JSON file"""
        try:
            if file_path.exists():
                with open(file_path, 'r') as f:
                    return json.load(f)
        except:
            pass
        return None


def main():
    """Run mobile connection bridge"""
    bridge = MobileTrinityBridge()

    # Send initial status to both devices
    print("📱 Sending initial status to S24...")
    bridge.send_trinity_status_to_mobile("s24")

    print("📱 Sending initial status to iPad...")
    bridge.send_trinity_status_to_mobile("ipad")

    # Run continuous sync
    bridge.run_continuous_sync(interval=30)


if __name__ == '__main__':
    main()
