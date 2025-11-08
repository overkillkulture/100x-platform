# MODULE #48: LOAD BALANCER

Intelligent load balancer to distribute requests across 6 AI instances. Supports 7 balancing strategies, health checks, sticky sessions, and comprehensive metrics.

## Features

- **7 Balancing Strategies**:
  - Round Robin: Distribute evenly in sequence
  - Least Connections: Send to backend with fewest active connections
  - Weighted Round Robin: Distribute based on backend weights
  - IP Hash: Consistent hashing for sticky sessions
  - Least Response Time: Send to fastest backend
  - Random: Random selection
  - Resource-Based: Select based on CPU, memory, and load

- **Health Checking**: Automatic backend health monitoring
- **Sticky Sessions**: Route same client to same backend
- **Connection Tracking**: Monitor active connections per backend
- **Metrics**: Track requests, response times, success rates
- **Graceful Draining**: Remove backends without dropping connections

## Usage

```python
from load_balancer import LoadBalancer, BalancingStrategy, Request

# Create load balancer
lb = LoadBalancer(strategy=BalancingStrategy.LEAST_CONNECTIONS)

# Add backends (6 AI instances)
lb.add_backend("instance-1", "192.168.1.1", 8001, weight=2)
lb.add_backend("instance-2", "192.168.1.1", 8002, weight=1)
lb.add_backend("instance-3", "192.168.1.2", 8003, weight=1)

# Select backend for request
request = Request("req-123", "192.168.1.100", "/api/process")
backend = lb.select_backend(request)

print(f"Routing to {backend.host}:{backend.port}")

# Track connection lifecycle
lb.acquire_connection(backend)
# ... process request ...
lb.release_connection(backend, response_time=0.05, success=True)
```

## Balancing Strategies

```python
# Round Robin (default)
lb = LoadBalancer(BalancingStrategy.ROUND_ROBIN)

# Least Connections (best for long-running requests)
lb = LoadBalancer(BalancingStrategy.LEAST_CONNECTIONS)

# Weighted (give more requests to powerful instances)
lb = LoadBalancer(BalancingStrategy.WEIGHTED_ROUND_ROBIN)
lb.add_backend("powerful-server", "192.168.1.1", 8001, weight=5)
lb.add_backend("normal-server", "192.168.1.2", 8002, weight=1)

# IP Hash (sticky sessions)
lb = LoadBalancer(BalancingStrategy.IP_HASH)

# Least Response Time (best for performance)
lb = LoadBalancer(BalancingStrategy.LEAST_RESPONSE_TIME)

# Resource-Based (consider CPU, memory, connections)
lb = LoadBalancer(BalancingStrategy.RESOURCE_BASED)
lb.update_backend_resources("instance-1", cpu=0.6, memory=0.7)
```

## Health Checking

```python
# Start automatic health checks
lb.start_health_checker()

# Manually check health
lb.perform_health_checks()

# Stop health checking
lb.stop_health_checker()

# Remove unhealthy backend
lb.remove_backend("instance-1")
```

## Sticky Sessions

```python
# Select with session ID
request = Request("req-123", "192.168.1.100", "/api/user")
backend = lb.select_backend(request, session_id="user-session-abc")

# Future requests with same session_id go to same backend
request2 = Request("req-124", "192.168.1.100", "/api/user")
backend2 = lb.select_backend(request2, session_id="user-session-abc")
# backend2 == backend
```

## Monitoring

```python
# Get backend stats
stats = lb.get_backend_stats("instance-1")
print(stats['success_rate'])
print(stats['avg_response_time'])

# Get all stats
all_stats = lb.get_all_stats()
print(all_stats['metrics']['total_requests'])
print(all_stats['metrics']['healthy_backends'])
```

## Dynamic Configuration

```python
# Change strategy at runtime
lb.set_strategy(BalancingStrategy.LEAST_CONNECTIONS)

# Update resource usage
lb.update_backend_resources("instance-1", cpu=0.8, memory=0.6)

# Add/remove backends dynamically
lb.add_backend("instance-7", "192.168.1.4", 8007)
lb.remove_backend("instance-1")  # Graceful draining
```

**#48 COMPLETE** ✅
