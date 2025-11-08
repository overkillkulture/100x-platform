# MODULE #49: GRAPH DATABASE

In-memory graph database for storing and querying graph-structured data. Perfect for modeling the Figure 8 Infinity Symbol and relationships between 6 AI instances.

## Features

- **Nodes & Edges**: Store entities and relationships with properties
- **Traversals**: BFS, DFS algorithms
- **Pathfinding**: Find shortest paths, all paths, Dijkstra's algorithm
- **Queries**: Find nodes/edges by label and properties
- **Indexes**: Fast lookups for labels and relationships
- **Import/Export**: Save and load graphs as JSON
- **Thread-Safe**: Concurrent access support

## Usage

```python
from graph_db import GraphDatabase

# Create database
db = GraphDatabase()

# Create nodes
db.create_node("user-1", "User", {"name": "Alice", "age": 30})
db.create_node("user-2", "User", {"name": "Bob", "age": 25})
db.create_node("post-1", "Post", {"title": "Hello World"})

# Create edges
db.create_edge("e1", "user-1", "user-2", "FOLLOWS", weight=1.0)
db.create_edge("e2", "user-1", "post-1", "WROTE", weight=1.0)

# Query nodes
users = db.find_nodes(label="User")
alice = db.find_nodes(label="User", properties={"name": "Alice"})

# Get neighbors
friends = db.get_neighbors("user-1", direction="out")

# Update node
db.update_node("user-1", {"verified": True})
```

## Traversals

```python
# Breadth-First Search
visited = db.bfs("user-1", max_depth=3)

# Depth-First Search
visited = db.dfs("user-1", max_depth=3)

# Get all neighbors
neighbors = db.get_neighbors("user-1", direction="both")  # in, out, or both
```

## Pathfinding

```python
# Find shortest path (BFS)
path = db.find_path("user-1", "user-5")
if path:
    print([n.id for n in path.nodes])  # ['user-1', 'user-2', 'user-5']
    print(path.total_weight)  # Sum of edge weights

# Find all paths
all_paths = db.find_all_paths("user-1", "user-5", max_length=5)
for path in all_paths:
    print([n.id for n in path.nodes])

# Dijkstra's shortest paths (weighted)
shortest = db.dijkstra("user-1", "user-5")
for node_id, (distance, path) in shortest.items():
    if distance < float('inf'):
        print(f"{node_id}: distance = {distance}")
```

## Queries

```python
# Find nodes by label
all_users = db.find_nodes(label="User")

# Find nodes by properties
admins = db.find_nodes(label="User", properties={"role": "admin"})

# Find edges
follows = db.find_edges(label="FOLLOWS")
user1_follows = db.find_edges(source_id="user-1")
user1_followers = db.find_edges(target_id="user-1")

# Get node degree
degree = db.get_degree("user-1")
print(degree['in'])    # Incoming edges
print(degree['out'])   # Outgoing edges
print(degree['total']) # Total edges
```

## Figure 8 Example

```python
# Create Figure 8 Infinity Symbol
db = GraphDatabase()

# 6 AI instances across 3 computers
for i in range(1, 7):
    computer = "A" if i <= 2 else "B" if i <= 4 else "C"
    db.create_node(f"instance-{i}", "AIInstance", {"computer": computer})

# Left loop: 1 -> 2 -> 3 -> 1
db.create_edge("e1", "instance-1", "instance-2", "sync")
db.create_edge("e2", "instance-2", "instance-3", "sync")
db.create_edge("e3", "instance-3", "instance-1", "sync")

# Right loop: 1 -> 4 -> 5 -> 6 -> 1
db.create_edge("e4", "instance-1", "instance-4", "sync")
db.create_edge("e5", "instance-4", "instance-5", "sync")
db.create_edge("e6", "instance-5", "instance-6", "sync")
db.create_edge("e7", "instance-6", "instance-1", "sync")

# Traverse the infinity loop
visited = db.bfs("instance-1")
print([n.id for n in visited])
```

## Import/Export

```python
# Export to JSON
db.export_json('graph.json')

# Import from JSON
db2 = GraphDatabase()
db2.import_json('graph.json')
```

## Monitoring

```python
# Get metrics
metrics = db.get_metrics()
print(metrics['node_count'])
print(metrics['edge_count'])
print(metrics['query_count'])
print(metrics['traversal_count'])
```

**#49 COMPLETE** ✅
