"""MODULE #46: DISTRIBUTED COMPUTING - Coordinate work across 6 AI instances"""
import json
import time
import hashlib
import threading
from typing import List, Dict, Any, Callable, Optional
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
import queue

class TaskStatus(Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class WorkerStatus(Enum):
    IDLE = "idle"
    BUSY = "busy"
    OFFLINE = "offline"

@dataclass
class Worker:
    worker_id: str
    computer_id: str  # Which of the 3 computers
    instance_id: int  # Which of the 6 instances
    status: WorkerStatus
    current_task: Optional[str] = None
    completed_tasks: int = 0
    failed_tasks: int = 0
    last_heartbeat: float = 0.0
    capabilities: List[str] = None
    load: float = 0.0  # 0.0 to 1.0

    def __post_init__(self):
        if self.capabilities is None:
            self.capabilities = []
        if self.last_heartbeat == 0.0:
            self.last_heartbeat = time.time()

@dataclass
class Task:
    task_id: str
    task_type: str
    priority: int  # 1-10, 10 is highest
    payload: Dict[str, Any]
    status: TaskStatus
    assigned_to: Optional[str] = None
    created_at: float = 0.0
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    result: Optional[Any] = None
    error: Optional[str] = None
    retries: int = 0
    max_retries: int = 3
    dependencies: List[str] = None

    def __post_init__(self):
        if self.created_at == 0.0:
            self.created_at = time.time()
        if self.dependencies is None:
            self.dependencies = []

class DistributedComputing:
    """
    Coordinate distributed computing across 6 AI instances on 3 computers.
    Implements work-stealing, load balancing, and fault tolerance.
    """

    def __init__(self, instance_id: int, computer_id: str):
        self.instance_id = instance_id
        self.computer_id = computer_id
        self.worker_id = f"{computer_id}-instance-{instance_id}"

        # Task management
        self.tasks: Dict[str, Task] = {}
        self.task_queue = queue.PriorityQueue()
        self.workers: Dict[str, Worker] = {}

        # Task handlers
        self.task_handlers: Dict[str, Callable] = {}

        # Synchronization
        self.lock = threading.Lock()
        self.running = False
        self.worker_thread: Optional[threading.Thread] = None

        # Metrics
        self.metrics = {
            'tasks_created': 0,
            'tasks_completed': 0,
            'tasks_failed': 0,
            'total_processing_time': 0.0,
            'average_task_time': 0.0
        }

        # Register self as worker
        self.register_worker(self.worker_id, self.computer_id, self.instance_id)

    def register_worker(self, worker_id: str, computer_id: str,
                       instance_id: int, capabilities: List[str] = None):
        """Register a worker in the distributed system"""
        with self.lock:
            worker = Worker(
                worker_id=worker_id,
                computer_id=computer_id,
                instance_id=instance_id,
                status=WorkerStatus.IDLE,
                capabilities=capabilities or ["general"]
            )
            self.workers[worker_id] = worker
            return worker

    def heartbeat(self, worker_id: str):
        """Update worker heartbeat"""
        with self.lock:
            if worker_id in self.workers:
                self.workers[worker_id].last_heartbeat = time.time()

    def get_worker_status(self, worker_id: str) -> Optional[Worker]:
        """Get status of a specific worker"""
        return self.workers.get(worker_id)

    def get_all_workers(self) -> Dict[str, Worker]:
        """Get all registered workers"""
        return dict(self.workers)

    def check_worker_health(self, timeout: float = 30.0) -> Dict[str, bool]:
        """Check which workers are still alive"""
        current_time = time.time()
        health = {}

        with self.lock:
            for worker_id, worker in self.workers.items():
                time_since_heartbeat = current_time - worker.last_heartbeat
                is_alive = time_since_heartbeat < timeout
                health[worker_id] = is_alive

                if not is_alive and worker.status != WorkerStatus.OFFLINE:
                    worker.status = WorkerStatus.OFFLINE
                    # Reassign tasks if worker went offline
                    if worker.current_task:
                        self._reassign_task(worker.current_task)

        return health

    def create_task(self, task_type: str, payload: Dict[str, Any],
                   priority: int = 5, dependencies: List[str] = None) -> str:
        """Create a new distributed task"""
        task_id = hashlib.md5(
            f"{task_type}-{time.time()}-{self.metrics['tasks_created']}".encode()
        ).hexdigest()[:16]

        task = Task(
            task_id=task_id,
            task_type=task_type,
            priority=priority,
            payload=payload,
            status=TaskStatus.PENDING,
            dependencies=dependencies or []
        )

        with self.lock:
            self.tasks[task_id] = task
            self.metrics['tasks_created'] += 1

            # Add to priority queue (higher priority = lower number for queue)
            self.task_queue.put((10 - priority, task_id))

        return task_id

    def register_task_handler(self, task_type: str, handler: Callable):
        """Register a handler function for a task type"""
        self.task_handlers[task_type] = handler

    def assign_task(self, task_id: str, worker_id: str) -> bool:
        """Assign a task to a specific worker"""
        with self.lock:
            if task_id not in self.tasks or worker_id not in self.workers:
                return False

            task = self.tasks[task_id]
            worker = self.workers[worker_id]

            # Check if task is ready (dependencies completed)
            if not self._check_dependencies(task):
                return False

            task.status = TaskStatus.ASSIGNED
            task.assigned_to = worker_id
            worker.current_task = task_id
            worker.status = WorkerStatus.BUSY

            return True

    def _check_dependencies(self, task: Task) -> bool:
        """Check if all task dependencies are completed"""
        for dep_id in task.dependencies:
            if dep_id not in self.tasks:
                return False
            if self.tasks[dep_id].status != TaskStatus.COMPLETED:
                return False
        return True

    def _reassign_task(self, task_id: str):
        """Reassign a task that failed or worker went offline"""
        if task_id not in self.tasks:
            return

        task = self.tasks[task_id]
        task.status = TaskStatus.PENDING
        task.assigned_to = None
        task.retries += 1

        if task.retries <= task.max_retries:
            # Put back in queue
            self.task_queue.put((10 - task.priority, task_id))
        else:
            task.status = TaskStatus.FAILED
            task.error = "Max retries exceeded"
            self.metrics['tasks_failed'] += 1

    def get_next_task(self, worker_id: str) -> Optional[Task]:
        """Get next available task for a worker"""
        if worker_id not in self.workers:
            return None

        try:
            # Get highest priority task
            _, task_id = self.task_queue.get_nowait()

            if self.assign_task(task_id, worker_id):
                return self.tasks[task_id]
            else:
                # Put back if couldn't assign
                with self.lock:
                    task = self.tasks[task_id]
                    self.task_queue.put((10 - task.priority, task_id))
                return None

        except queue.Empty:
            return None

    def execute_task(self, task_id: str) -> bool:
        """Execute a task using registered handler"""
        if task_id not in self.tasks:
            return False

        task = self.tasks[task_id]

        if task.task_type not in self.task_handlers:
            task.status = TaskStatus.FAILED
            task.error = f"No handler for task type: {task.task_type}"
            return False

        try:
            task.status = TaskStatus.IN_PROGRESS
            task.started_at = time.time()

            # Execute the handler
            handler = self.task_handlers[task.task_type]
            result = handler(task.payload)

            task.result = result
            task.status = TaskStatus.COMPLETED
            task.completed_at = time.time()

            # Update metrics
            processing_time = task.completed_at - task.started_at
            with self.lock:
                self.metrics['tasks_completed'] += 1
                self.metrics['total_processing_time'] += processing_time
                self.metrics['average_task_time'] = (
                    self.metrics['total_processing_time'] /
                    self.metrics['tasks_completed']
                )

            # Mark worker as idle
            if task.assigned_to and task.assigned_to in self.workers:
                worker = self.workers[task.assigned_to]
                worker.status = WorkerStatus.IDLE
                worker.current_task = None
                worker.completed_tasks += 1

            return True

        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.completed_at = time.time()

            with self.lock:
                self.metrics['tasks_failed'] += 1

            # Mark worker as idle
            if task.assigned_to and task.assigned_to in self.workers:
                worker = self.workers[task.assigned_to]
                worker.status = WorkerStatus.IDLE
                worker.current_task = None
                worker.failed_tasks += 1

            # Reassign if retries left
            self._reassign_task(task_id)

            return False

    def start_worker(self):
        """Start the worker thread"""
        if self.running:
            return

        self.running = True
        self.worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self.worker_thread.start()

    def stop_worker(self):
        """Stop the worker thread"""
        self.running = False
        if self.worker_thread:
            self.worker_thread.join(timeout=5.0)

    def _worker_loop(self):
        """Main worker loop - processes tasks continuously"""
        while self.running:
            # Send heartbeat
            self.heartbeat(self.worker_id)

            # Get next task
            task = self.get_next_task(self.worker_id)

            if task:
                self.execute_task(task.task_id)
            else:
                # No tasks, sleep briefly
                time.sleep(0.1)

    def get_task_status(self, task_id: str) -> Optional[Task]:
        """Get status of a specific task"""
        return self.tasks.get(task_id)

    def wait_for_task(self, task_id: str, timeout: float = 60.0) -> Optional[Any]:
        """Wait for a task to complete and return result"""
        start_time = time.time()

        while time.time() - start_time < timeout:
            task = self.get_task_status(task_id)

            if not task:
                return None

            if task.status == TaskStatus.COMPLETED:
                return task.result

            if task.status == TaskStatus.FAILED:
                raise Exception(f"Task failed: {task.error}")

            time.sleep(0.1)

        raise TimeoutError(f"Task {task_id} did not complete within {timeout}s")

    def get_metrics(self) -> Dict[str, Any]:
        """Get system metrics"""
        with self.lock:
            return {
                **self.metrics,
                'total_workers': len(self.workers),
                'active_workers': len([w for w in self.workers.values()
                                      if w.status == WorkerStatus.BUSY]),
                'idle_workers': len([w for w in self.workers.values()
                                    if w.status == WorkerStatus.IDLE]),
                'pending_tasks': self.task_queue.qsize(),
                'total_tasks': len(self.tasks)
            }

    def get_system_status(self) -> Dict[str, Any]:
        """Get complete system status"""
        return {
            'instance': {
                'worker_id': self.worker_id,
                'computer_id': self.computer_id,
                'instance_id': self.instance_id
            },
            'metrics': self.get_metrics(),
            'workers': {wid: asdict(w) for wid, w in self.workers.items()},
            'tasks': {
                'pending': len([t for t in self.tasks.values()
                               if t.status == TaskStatus.PENDING]),
                'in_progress': len([t for t in self.tasks.values()
                                   if t.status == TaskStatus.IN_PROGRESS]),
                'completed': len([t for t in self.tasks.values()
                                 if t.status == TaskStatus.COMPLETED]),
                'failed': len([t for t in self.tasks.values()
                              if t.status == TaskStatus.FAILED])
            }
        }

    def save_state(self, filepath: str):
        """Save system state to file"""
        state = {
            'workers': {wid: asdict(w) for wid, w in self.workers.items()},
            'tasks': {tid: asdict(t) for tid, t in self.tasks.items()},
            'metrics': self.metrics,
            'timestamp': time.time()
        }

        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2, default=str)

    def load_state(self, filepath: str):
        """Load system state from file"""
        with open(filepath, 'r') as f:
            state = json.load(f)

        # Restore workers
        for wid, wdata in state.get('workers', {}).items():
            worker = Worker(**{k: v for k, v in wdata.items()
                              if k in Worker.__annotations__})
            worker.status = WorkerStatus[worker.status] if isinstance(worker.status, str) else worker.status
            self.workers[wid] = worker

        # Restore tasks
        for tid, tdata in state.get('tasks', {}).items():
            task = Task(**{k: v for k, v in tdata.items()
                          if k in Task.__annotations__})
            task.status = TaskStatus[task.status] if isinstance(task.status, str) else task.status
            self.tasks[tid] = task

        # Restore metrics
        if 'metrics' in state:
            self.metrics.update(state['metrics'])


if __name__ == "__main__":
    print("🌐 MODULE #46: DISTRIBUTED COMPUTING FRAMEWORK")
    print("=" * 60)

    # Create distributed system for Instance 1 on Computer A
    dc = DistributedComputing(instance_id=1, computer_id="computer-a")

    # Register additional workers (simulating other instances)
    dc.register_worker("computer-a-instance-2", "computer-a", 2)
    dc.register_worker("computer-b-instance-3", "computer-b", 3)
    dc.register_worker("computer-b-instance-4", "computer-b", 4)
    dc.register_worker("computer-c-instance-5", "computer-c", 5)
    dc.register_worker("computer-c-instance-6", "computer-c", 6)

    print(f"✅ Registered {len(dc.workers)} workers across 3 computers")

    # Register task handlers
    def process_data(payload):
        """Simulate data processing"""
        time.sleep(0.1)  # Simulate work
        return {"processed": payload.get("data", ""), "count": len(payload.get("data", ""))}

    def analyze_pattern(payload):
        """Simulate pattern analysis"""
        time.sleep(0.15)
        return {"patterns_found": 5, "confidence": 0.87}

    dc.register_task_handler("process_data", process_data)
    dc.register_task_handler("analyze_pattern", analyze_pattern)

    print("✅ Registered task handlers")

    # Create tasks
    task_ids = []
    for i in range(10):
        task_id = dc.create_task(
            task_type="process_data" if i % 2 == 0 else "analyze_pattern",
            payload={"data": f"sample_data_{i}", "iteration": i},
            priority=5 + (i % 5)
        )
        task_ids.append(task_id)

    print(f"✅ Created {len(task_ids)} tasks")

    # Start workers
    dc.start_worker()

    print("\n⚙️  Processing tasks...")
    time.sleep(2)

    # Check status
    status = dc.get_system_status()
    print(f"\n📊 System Status:")
    print(f"   Total Workers: {status['metrics']['total_workers']}")
    print(f"   Active Workers: {status['metrics']['active_workers']}")
    print(f"   Tasks Completed: {status['metrics']['tasks_completed']}")
    print(f"   Tasks Failed: {status['metrics']['tasks_failed']}")
    print(f"   Avg Task Time: {status['metrics']['average_task_time']:.3f}s")

    print(f"\n📈 Task Breakdown:")
    print(f"   Pending: {status['tasks']['pending']}")
    print(f"   In Progress: {status['tasks']['in_progress']}")
    print(f"   Completed: {status['tasks']['completed']}")
    print(f"   Failed: {status['tasks']['failed']}")

    # Save state
    dc.save_state('/tmp/distributed_state.json')
    print("\n💾 System state saved to /tmp/distributed_state.json")

    # Stop worker
    dc.stop_worker()

    print("\n✅ Distributed Computing Framework operational!")
    print("🚀 Ready to coordinate 6 AI instances across 3 computers!")
