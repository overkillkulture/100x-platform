"""MODULE #58: TASK ORCHESTRATOR - Complex workflow orchestration"""
import time
import json
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum

class TaskState(Enum):
    PENDING = "pending"
    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"

@dataclass
class WorkflowTask:
    task_id: str
    name: str
    action: str
    params: Dict[str, Any]
    dependencies: List[str] = field(default_factory=list)
    state: TaskState = TaskState.PENDING
    result: Optional[Any] = None
    error: Optional[str] = None
    started_at: Optional[float] = None
    completed_at: Optional[float] = None

class TaskOrchestrator:
    """Orchestrate complex multi-step workflows"""

    def __init__(self, orchestrator_id: str = "main"):
        self.orchestrator_id = orchestrator_id
        self.workflows: Dict[str, List[WorkflowTask]] = {}
        self.task_handlers: Dict[str, Callable] = {}

        self.metrics = {
            'workflows_created': 0,
            'tasks_completed': 0,
            'tasks_failed': 0,
            'total_execution_time': 0.0
        }

    def create_workflow(self, workflow_id: str, tasks: List[Dict[str, Any]]) -> str:
        """Create a new workflow"""
        workflow_tasks = []

        for task_def in tasks:
            task = WorkflowTask(
                task_id=task_def['task_id'],
                name=task_def['name'],
                action=task_def['action'],
                params=task_def.get('params', {}),
                dependencies=task_def.get('dependencies', [])
            )
            workflow_tasks.append(task)

        self.workflows[workflow_id] = workflow_tasks
        self.metrics['workflows_created'] += 1

        return workflow_id

    def register_handler(self, action: str, handler: Callable):
        """Register task action handler"""
        self.task_handlers[action] = handler

    def execute_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Execute a workflow"""
        if workflow_id not in self.workflows:
            return {'success': False, 'error': 'Workflow not found'}

        workflow = self.workflows[workflow_id]
        start_time = time.time()
        results = {}

        while not self._is_workflow_complete(workflow):
            # Find ready tasks
            ready_tasks = self._get_ready_tasks(workflow)

            if not ready_tasks:
                # Check if workflow is stuck
                pending = [t for t in workflow if t.state == TaskState.PENDING]
                if pending:
                    for task in pending:
                        task.state = TaskState.FAILED
                        task.error = "Dependencies not satisfied"
                        self.metrics['tasks_failed'] += 1
                break

            # Execute ready tasks
            for task in ready_tasks:
                task.state = TaskState.RUNNING
                task.started_at = time.time()

                try:
                    # Execute task
                    if task.action in self.task_handlers:
                        result = self.task_handlers[task.action](task.params)
                        task.result = result
                        task.state = TaskState.COMPLETED
                        self.metrics['tasks_completed'] += 1
                    else:
                        raise Exception(f"No handler for action: {task.action}")

                except Exception as e:
                    task.state = TaskState.FAILED
                    task.error = str(e)
                    self.metrics['tasks_failed'] += 1

                task.completed_at = time.time()
                results[task.task_id] = {
                    'state': task.state.value,
                    'result': task.result,
                    'error': task.error,
                    'duration': task.completed_at - task.started_at
                }

        execution_time = time.time() - start_time
        self.metrics['total_execution_time'] += execution_time

        return {
            'workflow_id': workflow_id,
            'success': all(t.state == TaskState.COMPLETED for t in workflow),
            'execution_time': execution_time,
            'results': results
        }

    def _is_workflow_complete(self, workflow: List[WorkflowTask]) -> bool:
        """Check if workflow is complete"""
        return all(t.state in [TaskState.COMPLETED, TaskState.FAILED, TaskState.SKIPPED]
                  for t in workflow)

    def _get_ready_tasks(self, workflow: List[WorkflowTask]) -> List[WorkflowTask]:
        """Get tasks that are ready to execute"""
        ready = []

        for task in workflow:
            if task.state != TaskState.PENDING:
                continue

            # Check if dependencies are satisfied
            deps_satisfied = all(
                self._find_task(workflow, dep_id).state == TaskState.COMPLETED
                for dep_id in task.dependencies
            )

            if deps_satisfied:
                ready.append(task)

        return ready

    def _find_task(self, workflow: List[WorkflowTask], task_id: str) -> Optional[WorkflowTask]:
        """Find task by ID"""
        for task in workflow:
            if task.task_id == task_id:
                return task
        return None

    def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """Get workflow status"""
        if workflow_id not in self.workflows:
            return {}

        workflow = self.workflows[workflow_id]

        return {
            'workflow_id': workflow_id,
            'total_tasks': len(workflow),
            'completed': len([t for t in workflow if t.state == TaskState.COMPLETED]),
            'failed': len([t for t in workflow if t.state == TaskState.FAILED]),
            'running': len([t for t in workflow if t.state == TaskState.RUNNING]),
            'pending': len([t for t in workflow if t.state == TaskState.PENDING]),
            'tasks': [
                {
                    'task_id': t.task_id,
                    'name': t.name,
                    'state': t.state.value,
                    'error': t.error
                }
                for t in workflow
            ]
        }


if __name__ == "__main__":
    print("🎭 MODULE #58: TASK ORCHESTRATOR")
    print("=" * 60)

    orch = TaskOrchestrator()

    print("✅ Orchestrator initialized")

    # Register handlers
    def build_module(params):
        return f"Built module #{params['module']}"

    def test_module(params):
        return f"Tested module #{params['module']}"

    def deploy_module(params):
        return f"Deployed module #{params['module']}"

    orch.register_handler("build", build_module)
    orch.register_handler("test", test_module)
    orch.register_handler("deploy", deploy_module)

    print("✅ Registered 3 task handlers")

    # Create workflow
    print("\n📋 Creating deployment workflow...")
    workflow = [
        {'task_id': 't1', 'name': 'Build Module 56', 'action': 'build', 'params': {'module': 56}},
        {'task_id': 't2', 'name': 'Build Module 57', 'action': 'build', 'params': {'module': 57}},
        {'task_id': 't3', 'name': 'Test Module 56', 'action': 'test', 'params': {'module': 56}, 'dependencies': ['t1']},
        {'task_id': 't4', 'name': 'Test Module 57', 'action': 'test', 'params': {'module': 57}, 'dependencies': ['t2']},
        {'task_id': 't5', 'name': 'Deploy', 'action': 'deploy', 'params': {'module': 56}, 'dependencies': ['t3', 't4']}
    ]

    orch.create_workflow("deploy-workflow", workflow)

    # Execute workflow
    print("\n⚙️  Executing workflow...")
    result = orch.execute_workflow("deploy-workflow")

    print(f"\n📊 Workflow Results:")
    print(f"   Success: {result['success']}")
    print(f"   Execution time: {result['execution_time']:.3f}s")
    print(f"   Tasks completed: {len(result['results'])}")

    # Show task results
    print(f"\n✅ Task Results:")
    for task_id, task_result in result['results'].items():
        print(f"   {task_id}: {task_result['state']} - {task_result.get('result', 'N/A')}")

    print("\n✅ Task Orchestrator operational!")
    print("🚀 Ready to orchestrate complex workflows!")
