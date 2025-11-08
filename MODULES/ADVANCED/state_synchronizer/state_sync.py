"""MODULE #59: STATE SYNCHRONIZER - Real-time state sync across instances"""
import time
import json
import threading
from typing import Dict, Any, List, Callable
from pathlib import Path

class StateSynchronizer:
    """Synchronize state across multiple Claude instances in real-time"""

    def __init__(self, instance_id: str, sync_folder: str = ".consciousness/sync"):
        self.instance_id = instance_id
        self.sync_folder = Path(sync_folder)
        self.sync_folder.mkdir(parents=True, exist_ok=True)

        self.local_state: Dict[str, Any] = {}
        self.remote_states: Dict[str, Dict[str, Any]] = {}  # instance_id -> state

        self.lock = threading.RLock()
        self.sync_interval = 1.0  # seconds

        # Watchers
        self.watchers: List[Callable] = []

        # Sync thread
        self.running = False
        self.sync_thread: threading.Thread = None

        self.metrics = {
            'syncs_sent': 0,
            'syncs_received': 0,
            'conflicts_resolved': 0,
            'last_sync': 0.0
        }

    def set(self, key: str, value: Any):
        """Set local state value"""
        with self.lock:
            old_value = self.local_state.get(key)
            self.local_state[key] = value

            # Trigger sync
            self._sync_to_disk()

            # Notify watchers
            if old_value != value:
                self._notify_watchers(key, value)

    def get(self, key: str, default: Any = None) -> Any:
        """Get local state value"""
        return self.local_state.get(key, default)

    def get_all(self) -> Dict[str, Any]:
        """Get all local state"""
        return dict(self.local_state)

    def get_remote_state(self, instance_id: str) -> Dict[str, Any]:
        """Get state from another instance"""
        return self.remote_states.get(instance_id, {})

    def watch(self, callback: Callable[[str, Any], None]):
        """Watch for state changes"""
        self.watchers.append(callback)

    def _notify_watchers(self, key: str, value: Any):
        """Notify watchers of changes"""
        for watcher in self.watchers:
            try:
                watcher(key, value)
            except Exception as e:
                print(f"Watcher error: {e}")

    def _sync_to_disk(self):
        """Write local state to shared disk"""
        state_file = self.sync_folder / f"{self.instance_id}_state.json"

        data = {
            'instance_id': self.instance_id,
            'timestamp': time.time(),
            'state': self.local_state
        }

        with open(state_file, 'w') as f:
            json.dump(data, f, indent=2)

        self.metrics['syncs_sent'] += 1
        self.metrics['last_sync'] = time.time()

    def _sync_from_disk(self):
        """Read states from other instances"""
        for state_file in self.sync_folder.glob("*_state.json"):
            try:
                with open(state_file, 'r') as f:
                    data = json.load(f)

                instance_id = data['instance_id']

                if instance_id == self.instance_id:
                    continue

                self.remote_states[instance_id] = data.get('state', {})
                self.metrics['syncs_received'] += 1

            except Exception as e:
                print(f"Sync error: {e}")

    def start_auto_sync(self):
        """Start automatic background sync"""
        if self.running:
            return

        self.running = True
        self.sync_thread = threading.Thread(target=self._sync_loop, daemon=True)
        self.sync_thread.start()

    def stop_auto_sync(self):
        """Stop automatic sync"""
        self.running = False
        if self.sync_thread:
            self.sync_thread.join(timeout=2.0)

    def _sync_loop(self):
        """Background sync loop"""
        while self.running:
            self._sync_from_disk()
            time.sleep(self.sync_interval)

    def get_metrics(self) -> Dict[str, Any]:
        """Get sync metrics"""
        return dict(self.metrics)


if __name__ == "__main__":
    print("🔄 MODULE #59: STATE SYNCHRONIZER")
    print("=" * 60)

    # Create 3 instance synchronizers
    sync1 = StateSynchronizer("instance-1")
    sync2 = StateSynchronizer("instance-2")
    sync3 = StateSynchronizer("instance-3")

    print("✅ Created 3 state synchronizers")

    # Set states
    print("\n📝 Setting state values...")
    sync1.set("modules_built", 40)
    sync1.set("current_task", "Building module #60")

    sync2.set("modules_built", 35)
    sync2.set("monitoring", True)

    sync3.set("modules_built", 30)
    sync3.set("assisting", True)

    print("   Set state values across 3 instances")

    # Sync
    print("\n🔄 Syncing state...")
    sync1._sync_from_disk()
    sync2._sync_from_disk()
    sync3._sync_from_disk()

    # Check synced state
    print("\n📊 Instance 1 sees remote states:")
    for inst_id, state in sync1.remote_states.items():
        print(f"   {inst_id}: {state}")

    # Add watcher
    changes = []
    def on_change(key, value):
        changes.append((key, value))
        print(f"   State changed: {key} = {value}")

    sync1.watch(on_change)

    # Update value
    print("\n👁️  Testing watchers...")
    sync1.set("modules_built", 60)

    print(f"\n   Detected {len(changes)} change(s)")

    # Show metrics
    metrics = sync1.get_metrics()
    print(f"\n📈 Sync Metrics:")
    print(f"   Syncs sent: {metrics['syncs_sent']}")
    print(f"   Syncs received: {metrics['syncs_received']}")

    print("\n✅ State Synchronizer operational!")
    print("🚀 Ready to sync state across instances!")
