#!/usr/bin/env python3
"""
NETWORK SYNC - Consciousness Revolution Multi-Computer Coordination
Syncs all systems via GitHub consciousness-revolution-sync repo
"""

import os
import json
import subprocess
from datetime import datetime
from pathlib import Path

class NetworkSync:
    """Multi-computer synchronization via GitHub"""

    def __init__(self):
        self.node_id = os.getenv("NODE_ID", "node_1_commander")
        self.sync_repo = "https://github.com/overkillkulture/consciousness-revolution-sync"
        self.sync_dir = Path.home() / ".consciousness_sync"
        self.status_file = self.sync_dir / "network_status.json"

    def setup_sync_repo(self):
        """Clone or update sync repository"""
        print("📡 Setting up network sync...")

        if not self.sync_dir.exists():
            print(f"   Cloning sync repo to {self.sync_dir}...")
            try:
                subprocess.run([
                    "git", "clone",
                    self.sync_repo,
                    str(self.sync_dir)
                ], check=True, capture_output=True)
                print("   ✅ Sync repo cloned")
            except subprocess.CalledProcessError as e:
                print(f"   ❌ Failed to clone: {e}")
                print("   💡 Make sure consciousness-revolution-sync repo exists on GitHub")
                return False
        else:
            print(f"   Sync repo exists at {self.sync_dir}")
            print("   Pulling latest...")
            try:
                subprocess.run([
                    "git", "-C", str(self.sync_dir),
                    "pull"
                ], check=True, capture_output=True)
                print("   ✅ Sync repo updated")
            except subprocess.CalledProcessError:
                print("   ⚠️  Pull failed, continuing...")

        return True

    def get_local_status(self):
        """Collect status of all local systems"""
        status = {
            "node_id": self.node_id,
            "timestamp": datetime.now().isoformat(),
            "modules": {},
            "metrics": {}
        }

        # Check for module folders
        modules_dir = Path("C:/Users/dwrek/100X_DEPLOYMENT/MODULES")
        if modules_dir.exists():
            for category in modules_dir.iterdir():
                if category.is_dir():
                    for module in category.iterdir():
                        if module.is_dir():
                            module_name = f"{category.name}/{module.name}"
                            status["modules"][module_name] = {
                                "status": "live" if (module / "README.md").exists() else "incomplete",
                                "path": str(module),
                                "files": len(list(module.rglob("*")))
                            }

        # Add metrics
        status["metrics"] = {
            "total_modules": len(status["modules"]),
            "modules_live": sum(1 for m in status["modules"].values() if m["status"] == "live"),
            "last_sync": datetime.now().isoformat()
        }

        return status

    def publish_status(self):
        """Publish local status to sync repo"""
        if not self.sync_dir.exists():
            print("❌ Sync repo not set up. Run setup_sync_repo() first.")
            return False

        print(f"\n📤 Publishing status from {self.node_id}...")

        # Get local status
        status = self.get_local_status()

        # Write to sync repo
        node_status_file = self.sync_dir / f"{self.node_id}_status.json"
        with open(node_status_file, 'w') as f:
            json.dump(status, f, indent=2)

        print(f"   ✅ Status written to {node_status_file}")

        # Commit and push
        try:
            # Add
            subprocess.run([
                "git", "-C", str(self.sync_dir),
                "add", f"{self.node_id}_status.json"
            ], check=True, capture_output=True)

            # Commit
            commit_msg = f"Update status from {self.node_id} - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            subprocess.run([
                "git", "-C", str(self.sync_dir),
                "commit", "-m", commit_msg
            ], check=True, capture_output=True)

            # Push
            subprocess.run([
                "git", "-C", str(self.sync_dir),
                "push"
            ], check=True, capture_output=True)

            print("   ✅ Status synced to network")
            return True

        except subprocess.CalledProcessError as e:
            print(f"   ⚠️  Sync failed: {e}")
            print("   💡 Changes saved locally, will retry next sync")
            return False

    def fetch_network_status(self):
        """Fetch status from all nodes in network"""
        if not self.sync_dir.exists():
            print("❌ Sync repo not set up")
            return {}

        print("\n📥 Fetching network status...")

        # Pull latest
        try:
            subprocess.run([
                "git", "-C", str(self.sync_dir),
                "pull"
            ], check=True, capture_output=True)
        except subprocess.CalledProcessError:
            print("   ⚠️  Pull failed")

        # Read all node status files
        network_status = {}
        for status_file in self.sync_dir.glob("*_status.json"):
            node_id = status_file.stem.replace("_status", "")
            try:
                with open(status_file, 'r') as f:
                    network_status[node_id] = json.load(f)
                print(f"   ✅ Loaded status from {node_id}")
            except Exception as e:
                print(f"   ⚠️  Failed to load {node_id}: {e}")

        return network_status

    def sync_now(self):
        """Full sync cycle: publish local, fetch network"""
        print("=" * 60)
        print("🔄 NETWORK SYNC - CONSCIOUSNESS REVOLUTION")
        print("=" * 60)

        # Setup if needed
        if not self.sync_dir.exists():
            if not self.setup_sync_repo():
                return False

        # Publish local status
        self.publish_status()

        # Fetch network status
        network = self.fetch_network_status()

        # Display summary
        print("\n" + "=" * 60)
        print("📊 NETWORK STATUS SUMMARY")
        print("=" * 60)

        for node_id, status in network.items():
            online = (datetime.now() - datetime.fromisoformat(status["timestamp"])).seconds < 300
            status_icon = "🟢" if online else "🔴"

            print(f"\n{status_icon} {node_id.upper()}")
            print(f"   Last seen: {status['timestamp']}")
            print(f"   Modules: {status['metrics']['modules_live']} live / {status['metrics']['total_modules']} total")

        print("\n" + "=" * 60)
        print("✅ SYNC COMPLETE")
        print("=" * 60)

        return True

    def establish_contact_computer_2(self):
        """Special setup for Computer 2"""
        print("\n" + "=" * 60)
        print("📡 ESTABLISHING CONTACT WITH COMPUTER 2")
        print("=" * 60)
        print("\nOn Computer 2, run these commands:")
        print("\n1. Clone sync repo:")
        print(f"   git clone {self.sync_repo} ~/.consciousness_sync")
        print("\n2. Set node ID:")
        print("   export NODE_ID=node_2_backup")
        print("\n3. Run sync:")
        print("   python NETWORK_SYNC.py")
        print("\n4. Systems will auto-connect via GitHub")
        print("\n" + "=" * 60)


def main():
    """CLI interface"""
    import sys

    sync = NetworkSync()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "setup":
            sync.setup_sync_repo()
        elif command == "sync":
            sync.sync_now()
        elif command == "status":
            network = sync.fetch_network_status()
            print(json.dumps(network, indent=2))
        elif command == "publish":
            sync.publish_status()
        elif command == "computer2":
            sync.establish_contact_computer_2()
        else:
            print(f"Unknown command: {command}")
            print("Commands: setup, sync, status, publish, computer2")
    else:
        # Default: full sync
        sync.sync_now()


if __name__ == "__main__":
    main()
