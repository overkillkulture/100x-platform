"""MODULE #47: REAL-TIME SYNC ENGINE - Synchronize state across 6 instances"""
import json
import time
import threading
import hashlib
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict, field
from enum import Enum
from collections import defaultdict
import copy

class OperationType(Enum):
    SET = "set"
    UPDATE = "update"
    DELETE = "delete"
    APPEND = "append"
    INCREMENT = "increment"

class ConflictResolution(Enum):
    LAST_WRITE_WINS = "last_write_wins"
    FIRST_WRITE_WINS = "first_write_wins"
    MERGE = "merge"
    CUSTOM = "custom"

@dataclass
class Operation:
    op_id: str
    op_type: OperationType
    path: str  # e.g., "users.123.name"
    value: Any
    timestamp: float
    instance_id: int
    version: int
    dependencies: List[str] = field(default_factory=list)

@dataclass
class SyncState:
    data: Dict[str, Any]
    version: int
    last_modified: float
    checksum: str

class RealtimeSyncEngine:
    """
    Real-time state synchronization across 6 AI instances.
    Features: Operational Transformation, Conflict Resolution, Vector Clocks, CRDT-like semantics.
    """

    def __init__(self, instance_id: int, conflict_resolution: ConflictResolution = ConflictResolution.LAST_WRITE_WINS):
        self.instance_id = instance_id
        self.conflict_resolution = conflict_resolution

        # State management
        self.state: Dict[str, Any] = {}
        self.version = 0
        self.vector_clock: Dict[int, int] = defaultdict(int)  # Track versions per instance

        # Operation log
        self.operations: List[Operation] = []
        self.operation_index: Dict[str, Operation] = {}

        # Synchronization
        self.pending_operations: List[Operation] = []
        self.lock = threading.RLock()
        self.sync_callbacks: List[Callable] = []

        # Conflict handlers
        self.conflict_handlers: Dict[str, Callable] = {}

        # Metrics
        self.metrics = {
            'operations_applied': 0,
            'conflicts_resolved': 0,
            'sync_events': 0,
            'last_sync': 0.0
        }

    def get_value(self, path: str, default: Any = None) -> Any:
        """Get value at path (e.g., 'users.123.name')"""
        with self.lock:
            keys = path.split('.')
            current = self.state

            for key in keys:
                if isinstance(current, dict) and key in current:
                    current = current[key]
                else:
                    return default

            return current

    def set_value(self, path: str, value: Any) -> str:
        """Set value at path and create operation"""
        with self.lock:
            # Create operation
            op = self._create_operation(OperationType.SET, path, value)

            # Apply locally
            self._apply_operation(op)

            # Add to pending for sync
            self.pending_operations.append(op)

            return op.op_id

    def update_value(self, path: str, updates: Dict[str, Any]) -> str:
        """Update dictionary at path with new values"""
        with self.lock:
            current = self.get_value(path, {})

            if not isinstance(current, dict):
                raise ValueError(f"Cannot update non-dict value at {path}")

            merged = {**current, **updates}
            return self.set_value(path, merged)

    def delete_value(self, path: str) -> str:
        """Delete value at path"""
        with self.lock:
            op = self._create_operation(OperationType.DELETE, path, None)
            self._apply_operation(op)
            self.pending_operations.append(op)
            return op.op_id

    def append_value(self, path: str, value: Any) -> str:
        """Append to list at path"""
        with self.lock:
            current = self.get_value(path, [])

            if not isinstance(current, list):
                raise ValueError(f"Cannot append to non-list value at {path}")

            current.append(value)
            return self.set_value(path, current)

    def increment_value(self, path: str, delta: float = 1.0) -> str:
        """Increment numeric value at path"""
        with self.lock:
            current = self.get_value(path, 0)

            if not isinstance(current, (int, float)):
                raise ValueError(f"Cannot increment non-numeric value at {path}")

            return self.set_value(path, current + delta)

    def _create_operation(self, op_type: OperationType, path: str, value: Any) -> Operation:
        """Create new operation"""
        self.version += 1
        self.vector_clock[self.instance_id] += 1

        op_id = hashlib.md5(
            f"{self.instance_id}-{self.version}-{path}-{time.time()}".encode()
        ).hexdigest()[:16]

        op = Operation(
            op_id=op_id,
            op_type=op_type,
            path=path,
            value=value,
            timestamp=time.time(),
            instance_id=self.instance_id,
            version=self.version
        )

        return op

    def _apply_operation(self, op: Operation):
        """Apply operation to local state"""
        keys = op.path.split('.')

        if op.op_type == OperationType.SET:
            self._set_nested(self.state, keys, op.value)
        elif op.op_type == OperationType.DELETE:
            self._delete_nested(self.state, keys)
        elif op.op_type == OperationType.APPEND:
            current = self._get_nested(self.state, keys, [])
            if isinstance(current, list):
                current.append(op.value)
        elif op.op_type == OperationType.INCREMENT:
            current = self._get_nested(self.state, keys, 0)
            if isinstance(current, (int, float)):
                self._set_nested(self.state, keys, current + op.value)

        # Record operation
        self.operations.append(op)
        self.operation_index[op.op_id] = op
        self.metrics['operations_applied'] += 1

    def _set_nested(self, data: Dict, keys: List[str], value: Any):
        """Set value in nested dictionary"""
        for key in keys[:-1]:
            if key not in data or not isinstance(data[key], dict):
                data[key] = {}
            data = data[key]

        data[keys[-1]] = value

    def _delete_nested(self, data: Dict, keys: List[str]):
        """Delete value in nested dictionary"""
        for key in keys[:-1]:
            if key not in data:
                return
            data = data[key]

        if keys[-1] in data:
            del data[keys[-1]]

    def _get_nested(self, data: Dict, keys: List[str], default: Any = None) -> Any:
        """Get value from nested dictionary"""
        for key in keys:
            if isinstance(data, dict) and key in data:
                data = data[key]
            else:
                return default
        return data

    def receive_operations(self, operations: List[Dict[str, Any]]):
        """Receive and apply operations from other instances"""
        with self.lock:
            for op_data in operations:
                # Reconstruct operation
                op = Operation(
                    op_id=op_data['op_id'],
                    op_type=OperationType[op_data['op_type']],
                    path=op_data['path'],
                    value=op_data['value'],
                    timestamp=op_data['timestamp'],
                    instance_id=op_data['instance_id'],
                    version=op_data['version'],
                    dependencies=op_data.get('dependencies', [])
                )

                # Skip if already applied
                if op.op_id in self.operation_index:
                    continue

                # Check for conflicts
                conflicting_ops = self._find_conflicts(op)

                if conflicting_ops:
                    op = self._resolve_conflict(op, conflicting_ops)
                    self.metrics['conflicts_resolved'] += 1

                # Apply operation
                self._apply_operation(op)

                # Update vector clock
                self.vector_clock[op.instance_id] = max(
                    self.vector_clock[op.instance_id],
                    op.version
                )

            self.metrics['sync_events'] += 1
            self.metrics['last_sync'] = time.time()

            # Trigger callbacks
            for callback in self.sync_callbacks:
                try:
                    callback(self.state)
                except Exception as e:
                    print(f"Sync callback error: {e}")

    def _find_conflicts(self, op: Operation) -> List[Operation]:
        """Find operations that conflict with given operation"""
        conflicts = []

        for existing_op in self.operations:
            # Same path?
            if existing_op.path != op.path:
                continue

            # Different instance?
            if existing_op.instance_id == op.instance_id:
                continue

            # Happened around same time?
            time_diff = abs(existing_op.timestamp - op.timestamp)
            if time_diff < 1.0:  # Within 1 second = potential conflict
                conflicts.append(existing_op)

        return conflicts

    def _resolve_conflict(self, new_op: Operation, conflicts: List[Operation]) -> Operation:
        """Resolve conflict between operations"""
        if self.conflict_resolution == ConflictResolution.LAST_WRITE_WINS:
            # Keep operation with latest timestamp
            all_ops = conflicts + [new_op]
            return max(all_ops, key=lambda op: op.timestamp)

        elif self.conflict_resolution == ConflictResolution.FIRST_WRITE_WINS:
            # Keep operation with earliest timestamp
            all_ops = conflicts + [new_op]
            return min(all_ops, key=lambda op: op.timestamp)

        elif self.conflict_resolution == ConflictResolution.MERGE:
            # Merge values if possible
            if new_op.op_type == OperationType.SET:
                merged_value = new_op.value

                for conflict in conflicts:
                    if isinstance(merged_value, dict) and isinstance(conflict.value, dict):
                        merged_value = {**conflict.value, **merged_value}

                new_op.value = merged_value

            return new_op

        elif self.conflict_resolution == ConflictResolution.CUSTOM:
            # Use custom handler if registered
            if new_op.path in self.conflict_handlers:
                handler = self.conflict_handlers[new_op.path]
                return handler(new_op, conflicts)

            # Fallback to last write wins
            return max(conflicts + [new_op], key=lambda op: op.timestamp)

        return new_op

    def register_conflict_handler(self, path: str, handler: Callable):
        """Register custom conflict resolution handler for path"""
        self.conflict_handlers[path] = handler

    def get_pending_operations(self, clear: bool = True) -> List[Dict[str, Any]]:
        """Get operations pending sync to other instances"""
        with self.lock:
            pending = [asdict(op) for op in self.pending_operations]

            # Convert enums to strings
            for op_dict in pending:
                op_dict['op_type'] = op_dict['op_type'].value if hasattr(op_dict['op_type'], 'value') else op_dict['op_type']

            if clear:
                self.pending_operations.clear()

            return pending

    def on_sync(self, callback: Callable):
        """Register callback to be called when state is updated"""
        self.sync_callbacks.append(callback)

    def get_state_snapshot(self) -> SyncState:
        """Get complete state snapshot"""
        with self.lock:
            state_json = json.dumps(self.state, sort_keys=True)
            checksum = hashlib.md5(state_json.encode()).hexdigest()

            return SyncState(
                data=copy.deepcopy(self.state),
                version=self.version,
                last_modified=time.time(),
                checksum=checksum
            )

    def apply_state_snapshot(self, snapshot: SyncState):
        """Apply complete state snapshot"""
        with self.lock:
            self.state = copy.deepcopy(snapshot.data)
            self.version = snapshot.version

    def get_vector_clock(self) -> Dict[int, int]:
        """Get current vector clock"""
        return dict(self.vector_clock)

    def is_causally_ready(self, op: Operation) -> bool:
        """Check if operation is causally ready to apply"""
        # Check if we have all dependencies
        for dep_id in op.dependencies:
            if dep_id not in self.operation_index:
                return False

        # Check vector clock
        if op.instance_id in self.vector_clock:
            if op.version <= self.vector_clock[op.instance_id]:
                return False  # Already applied

        return True

    def get_metrics(self) -> Dict[str, Any]:
        """Get sync engine metrics"""
        with self.lock:
            return {
                **self.metrics,
                'state_size': len(json.dumps(self.state)),
                'operation_count': len(self.operations),
                'pending_operations': len(self.pending_operations),
                'vector_clock': dict(self.vector_clock),
                'version': self.version
            }

    def export_state(self, filepath: str):
        """Export state to JSON file"""
        snapshot = self.get_state_snapshot()

        export_data = {
            'state': snapshot.data,
            'version': snapshot.version,
            'checksum': snapshot.checksum,
            'vector_clock': dict(self.vector_clock),
            'timestamp': time.time()
        }

        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)

    def import_state(self, filepath: str):
        """Import state from JSON file"""
        with open(filepath, 'r') as f:
            import_data = json.load(f)

        snapshot = SyncState(
            data=import_data['state'],
            version=import_data['version'],
            last_modified=import_data['timestamp'],
            checksum=import_data['checksum']
        )

        self.apply_state_snapshot(snapshot)

        # Update vector clock
        if 'vector_clock' in import_data:
            for instance_id, version in import_data['vector_clock'].items():
                self.vector_clock[int(instance_id)] = version


if __name__ == "__main__":
    print("🔄 MODULE #47: REAL-TIME SYNC ENGINE")
    print("=" * 60)

    # Create sync engines for 3 instances
    sync1 = RealtimeSyncEngine(instance_id=1)
    sync2 = RealtimeSyncEngine(instance_id=2)
    sync3 = RealtimeSyncEngine(instance_id=3)

    print("✅ Created 3 sync engines (simulating 3 instances)")

    # Instance 1 sets some data
    sync1.set_value("users.alice.name", "Alice Smith")
    sync1.set_value("users.alice.score", 100)
    sync1.set_value("config.theme", "dark")

    print("\n📝 Instance 1 created initial data:")
    print(f"   users.alice.name = {sync1.get_value('users.alice.name')}")
    print(f"   users.alice.score = {sync1.get_value('users.alice.score')}")
    print(f"   config.theme = {sync1.get_value('config.theme')}")

    # Sync to instance 2
    pending = sync1.get_pending_operations()
    sync2.receive_operations(pending)

    print("\n🔄 Synced to Instance 2:")
    print(f"   users.alice.name = {sync2.get_value('users.alice.name')}")
    print(f"   users.alice.score = {sync2.get_value('users.alice.score')}")

    # Instance 2 makes update
    sync2.increment_value("users.alice.score", 50)

    print("\n➕ Instance 2 incremented score by 50")
    print(f"   Instance 2 score = {sync2.get_value('users.alice.score')}")

    # Sync back to instance 1
    pending = sync2.get_pending_operations()
    sync1.receive_operations(pending)

    print(f"   Instance 1 score = {sync1.get_value('users.alice.score')}")

    # Test conflict - both instances update same value
    sync1.set_value("users.alice.status", "online")
    sync2.set_value("users.alice.status", "busy")

    print("\n⚠️  Conflict: Both instances set 'status' to different values")

    # Sync (last write wins)
    pending1 = sync1.get_pending_operations()
    pending2 = sync2.get_pending_operations()

    sync2.receive_operations(pending1)
    sync1.receive_operations(pending2)

    print(f"   Instance 1 status = {sync1.get_value('users.alice.status')}")
    print(f"   Instance 2 status = {sync2.get_value('users.alice.status')}")
    print(f"   Conflicts resolved: {sync1.metrics['conflicts_resolved']}")

    # Show metrics
    metrics = sync1.get_metrics()
    print(f"\n📊 Metrics:")
    print(f"   Operations applied: {metrics['operations_applied']}")
    print(f"   Conflicts resolved: {metrics['conflicts_resolved']}")
    print(f"   Sync events: {metrics['sync_events']}")
    print(f"   State version: {metrics['version']}")

    # Export/import test
    sync1.export_state('/tmp/sync_state.json')
    print("\n💾 State exported to /tmp/sync_state.json")

    sync3.import_state('/tmp/sync_state.json')
    print(f"✅ Instance 3 imported state:")
    print(f"   users.alice.name = {sync3.get_value('users.alice.name')}")
    print(f"   users.alice.score = {sync3.get_value('users.alice.score')}")

    print("\n✅ Real-Time Sync Engine operational!")
    print("🚀 Ready to sync state across 6 AI instances!")
