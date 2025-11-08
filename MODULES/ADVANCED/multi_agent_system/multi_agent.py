"""MODULE #60: MULTI-AGENT SYSTEM - Coordinate multiple AI agents"""
import time
import json
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum

class AgentType(Enum):
    BUILDER = "builder"
    COORDINATOR = "coordinator"
    TESTER = "tester"
    REVIEWER = "reviewer"
    DEPLOYER = "deployer"

@dataclass
class Agent:
    agent_id: str
    agent_type: AgentType
    capabilities: List[str]
    status: str = "idle"  # idle, busy, error
    current_task: Optional[str] = None
    completed_tasks: int = 0
    failed_tasks: int = 0
    performance_score: float = 100.0

class MultiAgentSystem:
    """Coordinate multiple AI agents for collaborative work"""

    def __init__(self, system_id: str = "main"):
        self.system_id = system_id
        self.agents: Dict[str, Agent] = {}
        self.task_assignments: Dict[str, str] = {}  # task_id -> agent_id

        # Communication
        self.messages: List[Dict[str, Any]] = []

        # Metrics
        self.metrics = {
            'agents_registered': 0,
            'tasks_assigned': 0,
            'messages_sent': 0,
            'collaborations': 0
        }

    def register_agent(self, agent_id: str, agent_type: AgentType,
                      capabilities: List[str]) -> Agent:
        """Register an AI agent"""
        agent = Agent(
            agent_id=agent_id,
            agent_type=agent_type,
            capabilities=capabilities
        )

        self.agents[agent_id] = agent
        self.metrics['agents_registered'] += 1

        return agent

    def assign_task(self, task_id: str, task_type: str,
                   preferred_agent: Optional[str] = None) -> Optional[str]:
        """Assign task to best agent"""
        if preferred_agent and preferred_agent in self.agents:
            agent = self.agents[preferred_agent]
        else:
            agent = self._find_best_agent(task_type)

        if not agent:
            return None

        agent.status = "busy"
        agent.current_task = task_id
        self.task_assignments[task_id] = agent.agent_id

        self.metrics['tasks_assigned'] += 1

        return agent.agent_id

    def complete_task(self, task_id: str, success: bool = True):
        """Mark task as completed"""
        if task_id not in self.task_assignments:
            return False

        agent_id = self.task_assignments[task_id]
        agent = self.agents[agent_id]

        agent.status = "idle"
        agent.current_task = None

        if success:
            agent.completed_tasks += 1
            agent.performance_score = min(100.0, agent.performance_score + 0.5)
        else:
            agent.failed_tasks += 1
            agent.performance_score = max(0.0, agent.performance_score - 2.0)

        del self.task_assignments[task_id]

        return True

    def send_message(self, from_agent: str, to_agent: str, content: Any):
        """Send message between agents"""
        message = {
            'from': from_agent,
            'to': to_agent,
            'content': content,
            'timestamp': time.time()
        }

        self.messages.append(message)
        self.metrics['messages_sent'] += 1

    def broadcast_message(self, from_agent: str, content: Any):
        """Broadcast message to all agents"""
        for agent_id in self.agents:
            if agent_id != from_agent:
                self.send_message(from_agent, agent_id, content)

    def get_messages(self, agent_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get messages for an agent"""
        agent_messages = [
            msg for msg in self.messages
            if msg['to'] == agent_id or msg['to'] == 'all'
        ]

        return agent_messages[-limit:]

    def _find_best_agent(self, task_type: str) -> Optional[Agent]:
        """Find best agent for task"""
        # Find idle agents with capability
        candidates = [
            agent for agent in self.agents.values()
            if agent.status == "idle" and task_type in agent.capabilities
        ]

        if not candidates:
            # Fallback to any idle agent
            candidates = [a for a in self.agents.values() if a.status == "idle"]

        if not candidates:
            return None

        # Select highest performing
        return max(candidates, key=lambda a: a.performance_score)

    def form_team(self, task_id: str, required_capabilities: List[str]) -> List[str]:
        """Form a team of agents for complex task"""
        team = []

        for capability in required_capabilities:
            agent = self._find_best_agent(capability)
            if agent and agent.agent_id not in team:
                team.append(agent.agent_id)

        if len(team) >= 2:
            self.metrics['collaborations'] += 1

        return team

    def get_system_status(self) -> Dict[str, Any]:
        """Get system status"""
        return {
            'system_id': self.system_id,
            'total_agents': len(self.agents),
            'idle_agents': len([a for a in self.agents.values() if a.status == "idle"]),
            'busy_agents': len([a for a in self.agents.values() if a.status == "busy"]),
            'active_tasks': len(self.task_assignments),
            'metrics': self.metrics,
            'agents': [
                {
                    'agent_id': a.agent_id,
                    'type': a.agent_type.value,
                    'status': a.status,
                    'performance': a.performance_score,
                    'completed': a.completed_tasks
                }
                for a in self.agents.values()
            ]
        }


if __name__ == "__main__":
    print("🤖 MODULE #60: MULTI-AGENT SYSTEM")
    print("=" * 60)

    mas = MultiAgentSystem("consciousness-system")

    print("✅ Multi-agent system initialized")

    # Register agents
    print("\n🤖 Registering AI agents...")
    mas.register_agent("builder-1", AgentType.BUILDER, ["code", "build", "git"])
    mas.register_agent("tester-1", AgentType.TESTER, ["test", "validation"])
    mas.register_agent("coordinator-1", AgentType.COORDINATOR, ["coordination", "monitoring"])
    mas.register_agent("reviewer-1", AgentType.REVIEWER, ["code_review", "documentation"])

    print(f"   Registered 4 agents")

    # Assign tasks
    print("\n📋 Assigning tasks...")
    t1 = mas.assign_task("task-1", "code")
    t2 = mas.assign_task("task-2", "test")
    t3 = mas.assign_task("task-3", "coordination")

    print(f"   Task 1 assigned to: {t1}")
    print(f"   Task 2 assigned to: {t2}")
    print(f"   Task 3 assigned to: {t3}")

    # Send messages
    print("\n💬 Inter-agent communication...")
    mas.send_message("builder-1", "tester-1", {"action": "test_module", "module": 60})
    mas.broadcast_message("coordinator-1", {"status": "all_systems_operational"})

    print(f"   Sent {mas.metrics['messages_sent']} messages")

    # Form team
    print("\n👥 Forming team for complex task...")
    team = mas.form_team("complex-task", ["code", "test", "code_review"])
    print(f"   Team formed: {team}")

    # Complete tasks
    print("\n✅ Completing tasks...")
    mas.complete_task("task-1", success=True)
    mas.complete_task("task-2", success=True)

    # Show status
    status = mas.get_system_status()
    print(f"\n📊 System Status:")
    print(f"   Total agents: {status['total_agents']}")
    print(f"   Idle: {status['idle_agents']}")
    print(f"   Busy: {status['busy_agents']}")
    print(f"   Active tasks: {status['active_tasks']}")
    print(f"   Collaborations: {status['metrics']['collaborations']}")

    print("\n🤖 Agent Performance:")
    for agent in status['agents']:
        print(f"   {agent['agent_id']}: {agent['performance']:.1f} "
              f"({agent['completed']} completed)")

    print("\n✅ Multi-Agent System operational!")
    print("🚀 Ready to coordinate AI agents!")
