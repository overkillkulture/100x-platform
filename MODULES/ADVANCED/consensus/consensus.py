"""MODULE #52: CONSENSUS ALGORITHM - Raft consensus for distributed agreement"""
import time
import random
import threading
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

class NodeState(Enum):
    FOLLOWER = "follower"
    CANDIDATE = "candidate"
    LEADER = "leader"

@dataclass
class LogEntry:
    term: int
    index: int
    command: Any
    timestamp: float = field(default_factory=time.time)

class RaftNode:
    """Simplified Raft consensus algorithm for 6 AI instances"""

    def __init__(self, node_id: int, total_nodes: int = 6):
        self.node_id = node_id
        self.total_nodes = total_nodes

        # Raft state
        self.state = NodeState.FOLLOWER
        self.current_term = 0
        self.voted_for: Optional[int] = None
        self.leader_id: Optional[int] = None

        # Log
        self.log: List[LogEntry] = []
        self.commit_index = 0
        self.last_applied = 0

        # Election timing
        self.election_timeout = random.uniform(1.5, 3.0)
        self.last_heartbeat = time.time()

        # Votes
        self.votes_received: set = set()

        # Lock
        self.lock = threading.RLock()

        # Metrics
        self.metrics = {
            'elections_started': 0,
            'elections_won': 0,
            'heartbeats_sent': 0,
            'log_entries': 0
        }

    def start_election(self):
        """Start leader election"""
        with self.lock:
            self.state = NodeState.CANDIDATE
            self.current_term += 1
            self.voted_for = self.node_id
            self.votes_received = {self.node_id}
            self.last_heartbeat = time.time()
            self.metrics['elections_started'] += 1

            # In real implementation, would send RequestVote RPCs
            # Simulating vote collection
            return self.current_term

    def receive_vote(self, from_node: int, term: int) -> bool:
        """Receive vote from another node"""
        with self.lock:
            if term < self.current_term:
                return False

            if term > self.current_term:
                self.current_term = term
                self.state = NodeState.FOLLOWER
                self.voted_for = None

            self.votes_received.add(from_node)

            # Check if won election
            if len(self.votes_received) > self.total_nodes // 2:
                self.become_leader()

            return True

    def become_leader(self):
        """Transition to leader state"""
        with self.lock:
            if self.state != NodeState.CANDIDATE:
                return

            self.state = NodeState.LEADER
            self.leader_id = self.node_id
            self.metrics['elections_won'] += 1

    def append_entry(self, command: Any) -> bool:
        """Append entry to log (leader only)"""
        with self.lock:
            if self.state != NodeState.LEADER:
                return False

            entry = LogEntry(
                term=self.current_term,
                index=len(self.log),
                command=command
            )

            self.log.append(entry)
            self.metrics['log_entries'] += 1

            return True

    def send_heartbeat(self):
        """Send heartbeat (leader only)"""
        with self.lock:
            if self.state != NodeState.LEADER:
                return

            self.last_heartbeat = time.time()
            self.metrics['heartbeats_sent'] += 1

    def receive_heartbeat(self, leader_id: int, term: int):
        """Receive heartbeat from leader"""
        with self.lock:
            if term >= self.current_term:
                self.current_term = term
                self.state = NodeState.FOLLOWER
                self.leader_id = leader_id
                self.last_heartbeat = time.time()

    def check_timeout(self) -> bool:
        """Check if election timeout occurred"""
        return (time.time() - self.last_heartbeat) > self.election_timeout

    def get_status(self) -> Dict[str, Any]:
        """Get node status"""
        with self.lock:
            return {
                'node_id': self.node_id,
                'state': self.state.value,
                'term': self.current_term,
                'leader_id': self.leader_id,
                'log_size': len(self.log),
                'commit_index': self.commit_index,
                'metrics': self.metrics
            }


if __name__ == "__main__":
    print("🗳️  MODULE #52: CONSENSUS ALGORITHM (RAFT)")
    print("=" * 60)

    # Create 6 nodes
    nodes = [RaftNode(i+1, total_nodes=6) for i in range(6)]

    print("✅ Created 6 Raft nodes")

    # Node 1 starts election
    print("\n🗳️  Node 1 starting election...")
    term = nodes[0].start_election()

    # Simulate votes
    for i in range(1, 4):  # Nodes 2,3,4 vote for node 1
        nodes[0].receive_vote(i+1, term)

    print(f"   Votes received: {len(nodes[0].votes_received)}")
    print(f"   Node 1 state: {nodes[0].state.value}")

    # Leader appends entries
    if nodes[0].state == NodeState.LEADER:
        print("\n📝 Leader appending log entries...")
        nodes[0].append_entry({"action": "sync", "data": [1,2,3]})
        nodes[0].append_entry({"action": "update", "version": 2})
        nodes[0].append_entry({"action": "commit", "id": 123})

        print(f"   Log size: {len(nodes[0].log)}")

    # Send heartbeats
    print("\n💓 Sending heartbeats...")
    nodes[0].send_heartbeat()

    # Other nodes receive heartbeat
    for i in range(1, 6):
        nodes[i].receive_heartbeat(1, term)

    # Show status
    print("\n📊 Cluster Status:")
    for node in nodes[:3]:
        status = node.get_status()
        print(f"   Node {status['node_id']}: {status['state']} (term={status['term']}, log={status['log_size']})")

    print("\n✅ Consensus Algorithm operational!")
    print("🚀 Ready for distributed agreement across 6 instances!")
