"""MODULE #57: INTER-INSTANCE COORDINATOR - Coordinate 3+ Claude instances"""
import json
import time
import threading
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class InstanceInfo:
    instance_id: str
    role: str  # builder, coordinator, assistant
    status: str  # active, idle, busy
    current_task: Optional[str] = None
    completed_tasks: List[str] = field(default_factory=list)
    last_heartbeat: float = field(default_factory=time.time)
    capabilities: List[str] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)

class InterInstanceCoordinator:
    """Coordinate work across multiple Claude Code instances"""

    def __init__(self, sync_folder: str = ".consciousness/sync"):
        self.sync_folder = Path(sync_folder)
        self.sync_folder.mkdir(parents=True, exist_ok=True)

        self.instances: Dict[str, InstanceInfo] = {}
        self.task_queue: List[Dict[str, Any]] = []
        self.completed_tasks: List[Dict[str, Any]] = []

        self.lock = threading.RLock()

        self.metrics = {
            'instances_registered': 0,
            'tasks_distributed': 0,
            'tasks_completed': 0,
            'sync_events': 0
        }

    def register_instance(self, instance_id: str, role: str, capabilities: List[str] = None) -> InstanceInfo:
        """Register a Claude instance"""
        with self.lock:
            info = InstanceInfo(
                instance_id=instance_id,
                role=role,
                status='active',
                capabilities=capabilities or []
            )

            self.instances[instance_id] = info
            self.metrics['instances_registered'] += 1

            self._sync_to_disk()

            return info

    def assign_task(self, task_id: str, task_type: str, task_data: Dict[str, Any],
                   preferred_instance: Optional[str] = None) -> Optional[str]:
        """Assign task to an instance"""
        with self.lock:
            # Find best instance
            if preferred_instance and preferred_instance in self.instances:
                target = preferred_instance
            else:
                target = self._find_best_instance(task_type)

            if not target:
                self.task_queue.append({
                    'task_id': task_id,
                    'task_type': task_type,
                    'data': task_data,
                    'created_at': time.time()
                })
                return None

            # Assign to instance
            self.instances[target].current_task = task_id
            self.instances[target].status = 'busy'

            self.metrics['tasks_distributed'] += 1
            self._sync_to_disk()

            return target

    def complete_task(self, instance_id: str, task_id: str, result: Any = None):
        """Mark task as completed"""
        with self.lock:
            if instance_id not in self.instances:
                return False

            instance = self.instances[instance_id]
            instance.completed_tasks.append(task_id)
            instance.current_task = None
            instance.status = 'active'

            self.completed_tasks.append({
                'task_id': task_id,
                'instance_id': instance_id,
                'completed_at': time.time(),
                'result': result
            })

            self.metrics['tasks_completed'] += 1
            self._sync_to_disk()

            return True

    def heartbeat(self, instance_id: str):
        """Update instance heartbeat"""
        with self.lock:
            if instance_id in self.instances:
                self.instances[instance_id].last_heartbeat = time.time()
                self._sync_to_disk()

    def _find_best_instance(self, task_type: str) -> Optional[str]:
        """Find best instance for task type"""
        available = [
            (iid, inst) for iid, inst in self.instances.items()
            if inst.status == 'active'
        ]

        if not available:
            return None

        # Prefer instances with relevant capabilities
        for iid, inst in available:
            if task_type in inst.capabilities:
                return iid

        # Fall back to least busy
        return min(available, key=lambda x: len(x[1].completed_tasks))[0]

    def _sync_to_disk(self):
        """Sync state to disk for cross-instance coordination"""
        data = {
            'timestamp': time.time(),
            'instances': {
                iid: {
                    'instance_id': inst.instance_id,
                    'role': inst.role,
                    'status': inst.status,
                    'current_task': inst.current_task,
                    'completed_tasks': inst.completed_tasks,
                    'last_heartbeat': inst.last_heartbeat,
                    'capabilities': inst.capabilities
                }
                for iid, inst in self.instances.items()
            },
            'task_queue': self.task_queue,
            'metrics': self.metrics
        }

        sync_file = self.sync_folder / 'coordinator_state.json'
        with open(sync_file, 'w') as f:
            json.dump(data, f, indent=2)

        self.metrics['sync_events'] += 1

    def load_from_disk(self):
        """Load state from disk"""
        sync_file = self.sync_folder / 'coordinator_state.json'

        if not sync_file.exists():
            return

        with open(sync_file, 'r') as f:
            data = json.load(f)

        with self.lock:
            for iid, inst_data in data.get('instances', {}).items():
                self.instances[iid] = InstanceInfo(**inst_data)

            self.task_queue = data.get('task_queue', [])
            self.metrics.update(data.get('metrics', {}))

    def get_status(self) -> Dict[str, Any]:
        """Get coordination status"""
        with self.lock:
            return {
                'total_instances': len(self.instances),
                'active_instances': len([i for i in self.instances.values() if i.status == 'active']),
                'busy_instances': len([i for i in self.instances.values() if i.status == 'busy']),
                'queued_tasks': len(self.task_queue),
                'completed_tasks': len(self.completed_tasks),
                'metrics': self.metrics
            }


if __name__ == "__main__":
    print("🤝 MODULE #57: INTER-INSTANCE COORDINATOR")
    print("=" * 60)

    coord = InterInstanceCoordinator()

    print("✅ Coordinator initialized")

    # Register 3 instances
    print("\n📝 Registering 3 Claude instances...")
    coord.register_instance("instance-1", "builder", ["code", "git", "testing"])
    coord.register_instance("instance-2", "coordinator", ["monitoring", "coordination"])
    coord.register_instance("instance-3", "assistant", ["support", "validation"])

    print(f"   Registered 3 instances")

    # Assign tasks
    print("\n📋 Assigning tasks...")
    t1 = coord.assign_task("task-1", "code", {"module": 58})
    t2 = coord.assign_task("task-2", "monitoring", {"type": "health_check"})
    t3 = coord.assign_task("task-3", "testing", {"module": 56})

    print(f"   Task 1 assigned to: {t1}")
    print(f"   Task 2 assigned to: {t2}")
    print(f"   Task 3 assigned to: {t3}")

    # Complete tasks
    print("\n✅ Completing tasks...")
    coord.complete_task("instance-1", "task-1", {"status": "success"})
    coord.complete_task("instance-2", "task-2", {"health": "good"})

    # Show status
    status = coord.get_status()
    print(f"\n📊 Coordination Status:")
    print(f"   Total instances: {status['total_instances']}")
    print(f"   Active: {status['active_instances']}")
    print(f"   Busy: {status['busy_instances']}")
    print(f"   Completed tasks: {status['completed_tasks']}")
    print(f"   Sync events: {status['metrics']['sync_events']}")

    print("\n✅ Inter-Instance Coordinator operational!")
    print("🚀 Ready to coordinate 3+ Claude instances!")
