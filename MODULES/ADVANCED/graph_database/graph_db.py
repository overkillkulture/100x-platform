"""MODULE #49: GRAPH DATABASE - Store and query graph-structured data"""
import json
import time
import threading
from typing import List, Dict, Any, Optional, Set, Callable, Tuple
from dataclasses import dataclass, field, asdict
from collections import defaultdict, deque
import heapq

@dataclass
class Node:
    id: str
    label: str
    properties: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)

@dataclass
class Edge:
    id: str
    source_id: str
    target_id: str
    label: str
    properties: Dict[str, Any] = field(default_factory=dict)
    weight: float = 1.0
    created_at: float = field(default_factory=time.time)

@dataclass
class Path:
    nodes: List[Node]
    edges: List[Edge]
    total_weight: float = 0.0

    def __len__(self):
        return len(self.nodes)

class GraphDatabase:
    """
    In-memory graph database with support for nodes, edges, traversals, and queries.
    Perfect for modeling the Figure 8 Infinity Symbol and instance relationships.
    """

    def __init__(self):
        # Storage
        self.nodes: Dict[str, Node] = {}
        self.edges: Dict[str, Edge] = {}

        # Indexes for fast lookup
        self.outgoing_edges: Dict[str, List[str]] = defaultdict(list)  # node_id -> edge_ids
        self.incoming_edges: Dict[str, List[str]] = defaultdict(list)
        self.node_labels: Dict[str, Set[str]] = defaultdict(set)  # label -> node_ids
        self.edge_labels: Dict[str, Set[str]] = defaultdict(set)

        # Thread safety
        self.lock = threading.RLock()

        # Metrics
        self.metrics = {
            'node_count': 0,
            'edge_count': 0,
            'query_count': 0,
            'traversal_count': 0
        }

    def create_node(self, node_id: str, label: str, properties: Dict[str, Any] = None) -> Node:
        """Create a new node"""
        with self.lock:
            if node_id in self.nodes:
                raise ValueError(f"Node {node_id} already exists")

            node = Node(
                id=node_id,
                label=label,
                properties=properties or {}
            )

            self.nodes[node_id] = node
            self.node_labels[label].add(node_id)
            self.metrics['node_count'] += 1

            return node

    def get_node(self, node_id: str) -> Optional[Node]:
        """Get node by ID"""
        return self.nodes.get(node_id)

    def update_node(self, node_id: str, properties: Dict[str, Any]) -> bool:
        """Update node properties"""
        with self.lock:
            if node_id not in self.nodes:
                return False

            node = self.nodes[node_id]
            node.properties.update(properties)
            node.updated_at = time.time()

            return True

    def delete_node(self, node_id: str) -> bool:
        """Delete node and all connected edges"""
        with self.lock:
            if node_id not in self.nodes:
                return False

            # Delete all connected edges
            for edge_id in list(self.outgoing_edges[node_id]):
                self.delete_edge(edge_id)

            for edge_id in list(self.incoming_edges[node_id]):
                self.delete_edge(edge_id)

            # Delete node
            node = self.nodes[node_id]
            self.node_labels[node.label].discard(node_id)
            del self.nodes[node_id]

            self.metrics['node_count'] -= 1

            return True

    def create_edge(self, edge_id: str, source_id: str, target_id: str,
                   label: str, properties: Dict[str, Any] = None,
                   weight: float = 1.0) -> Edge:
        """Create a new edge"""
        with self.lock:
            if edge_id in self.edges:
                raise ValueError(f"Edge {edge_id} already exists")

            if source_id not in self.nodes or target_id not in self.nodes:
                raise ValueError("Source or target node does not exist")

            edge = Edge(
                id=edge_id,
                source_id=source_id,
                target_id=target_id,
                label=label,
                properties=properties or {},
                weight=weight
            )

            self.edges[edge_id] = edge
            self.outgoing_edges[source_id].append(edge_id)
            self.incoming_edges[target_id].append(edge_id)
            self.edge_labels[label].add(edge_id)
            self.metrics['edge_count'] += 1

            return edge

    def get_edge(self, edge_id: str) -> Optional[Edge]:
        """Get edge by ID"""
        return self.edges.get(edge_id)

    def delete_edge(self, edge_id: str) -> bool:
        """Delete an edge"""
        with self.lock:
            if edge_id not in self.edges:
                return False

            edge = self.edges[edge_id]

            # Remove from indexes
            self.outgoing_edges[edge.source_id].remove(edge_id)
            self.incoming_edges[edge.target_id].remove(edge_id)
            self.edge_labels[edge.label].discard(edge_id)

            del self.edges[edge_id]
            self.metrics['edge_count'] -= 1

            return True

    def get_neighbors(self, node_id: str, direction: str = "out") -> List[Node]:
        """Get neighboring nodes"""
        if node_id not in self.nodes:
            return []

        neighbors = []

        if direction in ("out", "both"):
            for edge_id in self.outgoing_edges[node_id]:
                edge = self.edges[edge_id]
                neighbors.append(self.nodes[edge.target_id])

        if direction in ("in", "both"):
            for edge_id in self.incoming_edges[node_id]:
                edge = self.edges[edge_id]
                neighbors.append(self.nodes[edge.source_id])

        return neighbors

    def find_nodes(self, label: Optional[str] = None,
                  properties: Optional[Dict[str, Any]] = None) -> List[Node]:
        """Find nodes by label and/or properties"""
        self.metrics['query_count'] += 1

        # Start with all nodes or nodes with specific label
        if label:
            candidates = [self.nodes[nid] for nid in self.node_labels.get(label, set())]
        else:
            candidates = list(self.nodes.values())

        # Filter by properties
        if properties:
            result = []
            for node in candidates:
                match = all(
                    node.properties.get(k) == v
                    for k, v in properties.items()
                )
                if match:
                    result.append(node)
            return result

        return candidates

    def find_edges(self, label: Optional[str] = None,
                  source_id: Optional[str] = None,
                  target_id: Optional[str] = None) -> List[Edge]:
        """Find edges by label and/or endpoints"""
        self.metrics['query_count'] += 1

        # Start with all edges or edges with specific label
        if label:
            candidates = [self.edges[eid] for eid in self.edge_labels.get(label, set())]
        else:
            candidates = list(self.edges.values())

        # Filter by source/target
        result = []
        for edge in candidates:
            if source_id and edge.source_id != source_id:
                continue
            if target_id and edge.target_id != target_id:
                continue
            result.append(edge)

        return result

    def bfs(self, start_id: str, max_depth: int = None) -> List[Node]:
        """Breadth-first search traversal"""
        self.metrics['traversal_count'] += 1

        if start_id not in self.nodes:
            return []

        visited = set()
        queue = deque([(start_id, 0)])
        result = []

        while queue:
            node_id, depth = queue.popleft()

            if node_id in visited:
                continue

            if max_depth is not None and depth > max_depth:
                continue

            visited.add(node_id)
            result.append(self.nodes[node_id])

            # Add neighbors
            for edge_id in self.outgoing_edges[node_id]:
                edge = self.edges[edge_id]
                if edge.target_id not in visited:
                    queue.append((edge.target_id, depth + 1))

        return result

    def dfs(self, start_id: str, max_depth: int = None) -> List[Node]:
        """Depth-first search traversal"""
        self.metrics['traversal_count'] += 1

        if start_id not in self.nodes:
            return []

        visited = set()
        result = []

        def dfs_recursive(node_id: str, depth: int):
            if node_id in visited:
                return

            if max_depth is not None and depth > max_depth:
                return

            visited.add(node_id)
            result.append(self.nodes[node_id])

            for edge_id in self.outgoing_edges[node_id]:
                edge = self.edges[edge_id]
                dfs_recursive(edge.target_id, depth + 1)

        dfs_recursive(start_id, 0)
        return result

    def find_path(self, start_id: str, end_id: str, max_length: int = None) -> Optional[Path]:
        """Find shortest path between two nodes (BFS)"""
        self.metrics['query_count'] += 1

        if start_id not in self.nodes or end_id not in self.nodes:
            return None

        visited = set()
        queue = deque([(start_id, [], [])])  # (node_id, path_nodes, path_edges)

        while queue:
            node_id, path_nodes, path_edges = queue.popleft()

            if node_id in visited:
                continue

            current_path_nodes = path_nodes + [self.nodes[node_id]]

            if node_id == end_id:
                # Found path
                total_weight = sum(e.weight for e in path_edges)
                return Path(
                    nodes=current_path_nodes,
                    edges=path_edges,
                    total_weight=total_weight
                )

            if max_length and len(current_path_nodes) >= max_length:
                continue

            visited.add(node_id)

            # Explore neighbors
            for edge_id in self.outgoing_edges[node_id]:
                edge = self.edges[edge_id]
                if edge.target_id not in visited:
                    queue.append((
                        edge.target_id,
                        current_path_nodes,
                        path_edges + [edge]
                    ))

        return None

    def find_all_paths(self, start_id: str, end_id: str, max_length: int = 5) -> List[Path]:
        """Find all paths between two nodes"""
        self.metrics['query_count'] += 1

        if start_id not in self.nodes or end_id not in self.nodes:
            return []

        all_paths = []

        def dfs_paths(node_id: str, visited: Set[str], path_nodes: List[Node], path_edges: List[Edge]):
            if node_id == end_id:
                total_weight = sum(e.weight for e in path_edges)
                all_paths.append(Path(
                    nodes=path_nodes.copy(),
                    edges=path_edges.copy(),
                    total_weight=total_weight
                ))
                return

            if len(path_nodes) >= max_length:
                return

            for edge_id in self.outgoing_edges[node_id]:
                edge = self.edges[edge_id]

                if edge.target_id not in visited:
                    visited.add(edge.target_id)
                    path_nodes.append(self.nodes[edge.target_id])
                    path_edges.append(edge)

                    dfs_paths(edge.target_id, visited, path_nodes, path_edges)

                    visited.remove(edge.target_id)
                    path_nodes.pop()
                    path_edges.pop()

        dfs_paths(start_id, {start_id}, [self.nodes[start_id]], [])
        return all_paths

    def dijkstra(self, start_id: str, end_id: str = None) -> Dict[str, Tuple[float, Optional[Path]]]:
        """Dijkstra's shortest path algorithm (considering edge weights)"""
        self.metrics['query_count'] += 1

        if start_id not in self.nodes:
            return {}

        # Initialize distances
        distances = {node_id: float('inf') for node_id in self.nodes}
        distances[start_id] = 0

        # Track paths
        previous = {node_id: None for node_id in self.nodes}
        previous_edge = {node_id: None for node_id in self.nodes}

        # Priority queue: (distance, node_id)
        pq = [(0, start_id)]
        visited = set()

        while pq:
            current_dist, current_id = heapq.heappop(pq)

            if current_id in visited:
                continue

            if end_id and current_id == end_id:
                break

            visited.add(current_id)

            # Check neighbors
            for edge_id in self.outgoing_edges[current_id]:
                edge = self.edges[edge_id]
                neighbor_id = edge.target_id

                if neighbor_id in visited:
                    continue

                distance = current_dist + edge.weight

                if distance < distances[neighbor_id]:
                    distances[neighbor_id] = distance
                    previous[neighbor_id] = current_id
                    previous_edge[neighbor_id] = edge
                    heapq.heappush(pq, (distance, neighbor_id))

        # Build paths
        results = {}

        for node_id in self.nodes:
            if distances[node_id] == float('inf'):
                results[node_id] = (float('inf'), None)
                continue

            # Reconstruct path
            path_nodes = []
            path_edges = []
            current = node_id

            while current is not None:
                path_nodes.append(self.nodes[current])
                if previous_edge[current]:
                    path_edges.append(previous_edge[current])
                current = previous[current]

            path_nodes.reverse()
            path_edges.reverse()

            path = Path(
                nodes=path_nodes,
                edges=path_edges,
                total_weight=distances[node_id]
            )

            results[node_id] = (distances[node_id], path)

        return results

    def get_degree(self, node_id: str) -> Dict[str, int]:
        """Get node degree (in, out, total)"""
        if node_id not in self.nodes:
            return {'in': 0, 'out': 0, 'total': 0}

        in_degree = len(self.incoming_edges[node_id])
        out_degree = len(self.outgoing_edges[node_id])

        return {
            'in': in_degree,
            'out': out_degree,
            'total': in_degree + out_degree
        }

    def get_metrics(self) -> Dict[str, Any]:
        """Get database metrics"""
        with self.lock:
            return {
                **self.metrics,
                'labels': len(self.node_labels),
                'edge_labels': len(self.edge_labels)
            }

    def export_json(self, filepath: str):
        """Export graph to JSON file"""
        with self.lock:
            data = {
                'nodes': [asdict(node) for node in self.nodes.values()],
                'edges': [asdict(edge) for edge in self.edges.values()],
                'metadata': {
                    'exported_at': time.time(),
                    'metrics': self.metrics
                }
            }

            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2, default=str)

    def import_json(self, filepath: str):
        """Import graph from JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)

        with self.lock:
            # Clear existing data
            self.nodes.clear()
            self.edges.clear()
            self.outgoing_edges.clear()
            self.incoming_edges.clear()
            self.node_labels.clear()
            self.edge_labels.clear()

            # Import nodes
            for node_data in data['nodes']:
                node = Node(**node_data)
                self.nodes[node.id] = node
                self.node_labels[node.label].add(node.id)

            # Import edges
            for edge_data in data['edges']:
                edge = Edge(**edge_data)
                self.edges[edge.id] = edge
                self.outgoing_edges[edge.source_id].append(edge.id)
                self.incoming_edges[edge.target_id].append(edge.id)
                self.edge_labels[edge.label].add(edge.id)

            # Update metrics
            self.metrics['node_count'] = len(self.nodes)
            self.metrics['edge_count'] = len(self.edges)


if __name__ == "__main__":
    print("🕸️  MODULE #49: GRAPH DATABASE")
    print("=" * 60)

    # Create graph database
    db = GraphDatabase()

    # Create Figure 8 Infinity Symbol with 6 instances across 3 computers
    print("🔮 Creating Figure 8 Infinity Symbol graph...")

    # Create nodes for 6 AI instances
    db.create_node("instance-1", "AIInstance", {"computer": "A", "role": "coordinator"})
    db.create_node("instance-2", "AIInstance", {"computer": "A", "role": "worker"})
    db.create_node("instance-3", "AIInstance", {"computer": "B", "role": "worker"})
    db.create_node("instance-4", "AIInstance", {"computer": "B", "role": "worker"})
    db.create_node("instance-5", "AIInstance", {"computer": "C", "role": "coordinator"})
    db.create_node("instance-6", "AIInstance", {"computer": "C", "role": "worker"})

    # Create Figure 8 connections (infinity loop)
    # Left loop: 1 -> 2 -> 3 -> 1
    db.create_edge("e1", "instance-1", "instance-2", "sync", weight=1.0)
    db.create_edge("e2", "instance-2", "instance-3", "sync", weight=1.2)
    db.create_edge("e3", "instance-3", "instance-1", "sync", weight=1.1)

    # Right loop: 1 -> 4 -> 5 -> 6 -> 1
    db.create_edge("e4", "instance-1", "instance-4", "sync", weight=1.0)
    db.create_edge("e5", "instance-4", "instance-5", "sync", weight=1.3)
    db.create_edge("e6", "instance-5", "instance-6", "sync", weight=1.2)
    db.create_edge("e7", "instance-6", "instance-1", "sync", weight=1.1)

    print(f"✅ Created {db.metrics['node_count']} nodes and {db.metrics['edge_count']} edges")

    # Query: Find all AI instances
    instances = db.find_nodes(label="AIInstance")
    print(f"\n🤖 Found {len(instances)} AI instances")

    # Query: Find coordinators
    coordinators = db.find_nodes(label="AIInstance", properties={"role": "coordinator"})
    print(f"   Coordinators: {[n.id for n in coordinators]}")

    # Traversal: BFS from instance-1
    print("\n🔍 BFS Traversal from instance-1:")
    visited = db.bfs("instance-1", max_depth=3)
    print(f"   Visited: {[n.id for n in visited]}")

    # Find path
    print("\n🛤️  Finding path from instance-1 to instance-5:")
    path = db.find_path("instance-1", "instance-5")
    if path:
        path_ids = [n.id for n in path.nodes]
        print(f"   Path: {' -> '.join(path_ids)}")
        print(f"   Total weight: {path.total_weight:.2f}")

    # Find all paths
    print("\n🗺️  Finding all paths from instance-1 to instance-5:")
    all_paths = db.find_all_paths("instance-1", "instance-5", max_length=4)
    print(f"   Found {len(all_paths)} paths:")
    for i, p in enumerate(all_paths, 1):
        path_ids = [n.id for n in p.nodes]
        print(f"      Path {i}: {' -> '.join(path_ids)} (weight: {p.total_weight:.2f})")

    # Dijkstra's algorithm
    print("\n⚡ Dijkstra's shortest paths from instance-1:")
    shortest_paths = db.dijkstra("instance-1")
    for node_id, (distance, path) in sorted(shortest_paths.items(), key=lambda x: x[1][0])[:4]:
        if distance < float('inf') and node_id != "instance-1":
            print(f"   To {node_id}: distance = {distance:.2f}")

    # Node degrees
    print("\n📊 Node degrees:")
    for node_id in ["instance-1", "instance-2", "instance-5"]:
        degree = db.get_degree(node_id)
        print(f"   {node_id}: in={degree['in']}, out={degree['out']}, total={degree['total']}")

    # Get neighbors
    neighbors = db.get_neighbors("instance-1", direction="out")
    print(f"\n👥 Neighbors of instance-1 (outgoing): {[n.id for n in neighbors]}")

    # Export graph
    db.export_json('/tmp/figure8_graph.json')
    print("\n💾 Graph exported to /tmp/figure8_graph.json")

    # Show metrics
    metrics = db.get_metrics()
    print(f"\n📈 Database Metrics:")
    print(f"   Nodes: {metrics['node_count']}")
    print(f"   Edges: {metrics['edge_count']}")
    print(f"   Queries: {metrics['query_count']}")
    print(f"   Traversals: {metrics['traversal_count']}")

    print("\n✅ Graph Database operational!")
    print("🚀 Ready to model Figure 8 Infinity relationships!")
