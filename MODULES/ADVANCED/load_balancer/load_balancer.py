"""MODULE #48: LOAD BALANCER - Distribute requests across 6 AI instances"""
import time
import random
import hashlib
import threading
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
import heapq

class BalancingStrategy(Enum):
    ROUND_ROBIN = "round_robin"
    LEAST_CONNECTIONS = "least_connections"
    WEIGHTED_ROUND_ROBIN = "weighted_round_robin"
    IP_HASH = "ip_hash"
    LEAST_RESPONSE_TIME = "least_response_time"
    RANDOM = "random"
    RESOURCE_BASED = "resource_based"

class BackendStatus(Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    DRAINING = "draining"  # No new connections, finish existing

@dataclass
class Backend:
    id: str
    host: str
    port: int
    weight: int = 1  # For weighted algorithms
    status: BackendStatus = BackendStatus.HEALTHY
    active_connections: int = 0
    total_requests: int = 0
    failed_requests: int = 0
    total_response_time: float = 0.0
    avg_response_time: float = 0.0
    last_health_check: float = 0.0
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def record_request(self, response_time: float, success: bool = True):
        """Record request metrics"""
        self.total_requests += 1

        if success:
            self.total_response_time += response_time
            self.avg_response_time = self.total_response_time / self.total_requests
        else:
            self.failed_requests += 1

    def get_score(self) -> float:
        """Calculate backend score for resource-based balancing"""
        if self.status != BackendStatus.HEALTHY:
            return float('inf')  # Don't select unhealthy backends

        # Lower score = better
        connection_factor = self.active_connections * 0.3
        response_time_factor = self.avg_response_time * 0.3
        cpu_factor = self.cpu_usage * 0.2
        memory_factor = self.memory_usage * 0.2

        return connection_factor + response_time_factor + cpu_factor + memory_factor

@dataclass
class Request:
    request_id: str
    client_ip: str
    path: str
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)

class LoadBalancer:
    """
    Intelligent load balancer for distributing requests across 6 AI instances.
    Supports multiple balancing strategies, health checks, and sticky sessions.
    """

    def __init__(self, strategy: BalancingStrategy = BalancingStrategy.ROUND_ROBIN):
        self.strategy = strategy
        self.backends: Dict[str, Backend] = {}
        self.backend_list: List[Backend] = []

        # Strategy state
        self.round_robin_index = 0
        self.sticky_sessions: Dict[str, str] = {}  # session_id -> backend_id

        # Health checking
        self.health_check_interval = 10.0  # seconds
        self.health_check_timeout = 5.0
        self.health_checker_thread: Optional[threading.Thread] = None
        self.running = False

        # Metrics
        self.lock = threading.Lock()
        self.metrics = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'total_backends': 0,
            'healthy_backends': 0
        }

    def add_backend(self, backend_id: str, host: str, port: int,
                   weight: int = 1, metadata: Dict[str, Any] = None) -> Backend:
        """Add a backend server"""
        backend = Backend(
            id=backend_id,
            host=host,
            port=port,
            weight=weight,
            metadata=metadata or {}
        )

        with self.lock:
            self.backends[backend_id] = backend
            self.backend_list = list(self.backends.values())
            self.metrics['total_backends'] = len(self.backends)
            self.metrics['healthy_backends'] = len([b for b in self.backends.values()
                                                   if b.status == BackendStatus.HEALTHY])

        return backend

    def remove_backend(self, backend_id: str) -> bool:
        """Remove a backend server"""
        with self.lock:
            if backend_id not in self.backends:
                return False

            # Set to draining first
            self.backends[backend_id].status = BackendStatus.DRAINING

            # Wait for active connections to finish
            # In real implementation, would wait here

            del self.backends[backend_id]
            self.backend_list = list(self.backends.values())
            self.metrics['total_backends'] = len(self.backends)

            return True

    def select_backend(self, request: Request, session_id: Optional[str] = None) -> Optional[Backend]:
        """Select backend based on strategy"""
        with self.lock:
            # Check sticky session first
            if session_id and session_id in self.sticky_sessions:
                backend_id = self.sticky_sessions[session_id]
                if backend_id in self.backends:
                    backend = self.backends[backend_id]
                    if backend.status == BackendStatus.HEALTHY:
                        return backend

            # Get healthy backends
            healthy = [b for b in self.backend_list if b.status == BackendStatus.HEALTHY]

            if not healthy:
                return None

            # Apply strategy
            if self.strategy == BalancingStrategy.ROUND_ROBIN:
                backend = self._round_robin(healthy)
            elif self.strategy == BalancingStrategy.LEAST_CONNECTIONS:
                backend = self._least_connections(healthy)
            elif self.strategy == BalancingStrategy.WEIGHTED_ROUND_ROBIN:
                backend = self._weighted_round_robin(healthy)
            elif self.strategy == BalancingStrategy.IP_HASH:
                backend = self._ip_hash(healthy, request.client_ip)
            elif self.strategy == BalancingStrategy.LEAST_RESPONSE_TIME:
                backend = self._least_response_time(healthy)
            elif self.strategy == BalancingStrategy.RANDOM:
                backend = self._random(healthy)
            elif self.strategy == BalancingStrategy.RESOURCE_BASED:
                backend = self._resource_based(healthy)
            else:
                backend = self._round_robin(healthy)

            # Create sticky session if requested
            if session_id and backend:
                self.sticky_sessions[session_id] = backend.id

            return backend

    def _round_robin(self, backends: List[Backend]) -> Backend:
        """Simple round-robin selection"""
        backend = backends[self.round_robin_index % len(backends)]
        self.round_robin_index += 1
        return backend

    def _least_connections(self, backends: List[Backend]) -> Backend:
        """Select backend with least active connections"""
        return min(backends, key=lambda b: b.active_connections)

    def _weighted_round_robin(self, backends: List[Backend]) -> Backend:
        """Weighted round-robin (higher weight = more requests)"""
        # Create weighted list
        weighted = []
        for backend in backends:
            weighted.extend([backend] * backend.weight)

        if not weighted:
            return backends[0]

        backend = weighted[self.round_robin_index % len(weighted)]
        self.round_robin_index += 1
        return backend

    def _ip_hash(self, backends: List[Backend], client_ip: str) -> Backend:
        """Consistent hashing based on client IP"""
        hash_val = int(hashlib.md5(client_ip.encode()).hexdigest(), 16)
        index = hash_val % len(backends)
        return backends[index]

    def _least_response_time(self, backends: List[Backend]) -> Backend:
        """Select backend with lowest average response time"""
        # Filter out backends with no requests yet
        with_requests = [b for b in backends if b.total_requests > 0]

        if not with_requests:
            return backends[0]

        return min(with_requests, key=lambda b: b.avg_response_time)

    def _random(self, backends: List[Backend]) -> Backend:
        """Random selection"""
        return random.choice(backends)

    def _resource_based(self, backends: List[Backend]) -> Backend:
        """Select based on resource usage (CPU, memory, connections)"""
        return min(backends, key=lambda b: b.get_score())

    def acquire_connection(self, backend: Backend):
        """Mark connection as active"""
        with self.lock:
            backend.active_connections += 1

    def release_connection(self, backend: Backend, response_time: float, success: bool = True):
        """Release connection and record metrics"""
        with self.lock:
            backend.active_connections -= 1
            backend.record_request(response_time, success)

            self.metrics['total_requests'] += 1
            if success:
                self.metrics['successful_requests'] += 1
            else:
                self.metrics['failed_requests'] += 1

    def health_check(self, backend: Backend) -> bool:
        """
        Perform health check on backend.
        In real implementation, would make HTTP request or TCP connection.
        """
        # Simulate health check
        backend.last_health_check = time.time()

        # Simple simulation: mark unhealthy if too many failures
        if backend.total_requests > 0:
            failure_rate = backend.failed_requests / backend.total_requests
            if failure_rate > 0.5:  # More than 50% failures
                return False

        return True

    def perform_health_checks(self):
        """Perform health checks on all backends"""
        with self.lock:
            for backend in self.backends.values():
                if backend.status == BackendStatus.DRAINING:
                    continue

                is_healthy = self.health_check(backend)

                if is_healthy and backend.status != BackendStatus.HEALTHY:
                    backend.status = BackendStatus.HEALTHY
                elif not is_healthy and backend.status != BackendStatus.UNHEALTHY:
                    backend.status = BackendStatus.UNHEALTHY

            self.metrics['healthy_backends'] = len([b for b in self.backends.values()
                                                   if b.status == BackendStatus.HEALTHY])

    def start_health_checker(self):
        """Start background health checking"""
        if self.running:
            return

        self.running = True
        self.health_checker_thread = threading.Thread(
            target=self._health_check_loop,
            daemon=True
        )
        self.health_checker_thread.start()

    def stop_health_checker(self):
        """Stop background health checking"""
        self.running = False
        if self.health_checker_thread:
            self.health_checker_thread.join(timeout=5.0)

    def _health_check_loop(self):
        """Background health check loop"""
        while self.running:
            self.perform_health_checks()
            time.sleep(self.health_check_interval)

    def update_backend_resources(self, backend_id: str, cpu: float, memory: float):
        """Update backend resource usage for resource-based balancing"""
        with self.lock:
            if backend_id in self.backends:
                self.backends[backend_id].cpu_usage = cpu
                self.backends[backend_id].memory_usage = memory

    def get_backend_stats(self, backend_id: str) -> Optional[Dict[str, Any]]:
        """Get statistics for a backend"""
        backend = self.backends.get(backend_id)
        if not backend:
            return None

        return {
            'id': backend.id,
            'host': backend.host,
            'port': backend.port,
            'status': backend.status.value,
            'active_connections': backend.active_connections,
            'total_requests': backend.total_requests,
            'failed_requests': backend.failed_requests,
            'success_rate': (
                (backend.total_requests - backend.failed_requests) / backend.total_requests
                if backend.total_requests > 0 else 0
            ),
            'avg_response_time': backend.avg_response_time,
            'cpu_usage': backend.cpu_usage,
            'memory_usage': backend.memory_usage
        }

    def get_all_stats(self) -> Dict[str, Any]:
        """Get statistics for all backends"""
        with self.lock:
            return {
                'metrics': self.metrics,
                'backends': {
                    backend_id: self.get_backend_stats(backend_id)
                    for backend_id in self.backends
                }
            }

    def set_strategy(self, strategy: BalancingStrategy):
        """Change balancing strategy"""
        with self.lock:
            self.strategy = strategy
            self.round_robin_index = 0  # Reset state


if __name__ == "__main__":
    print("⚖️  MODULE #48: LOAD BALANCER")
    print("=" * 60)

    # Create load balancer with round-robin strategy
    lb = LoadBalancer(strategy=BalancingStrategy.ROUND_ROBIN)

    # Add 6 backends (representing 6 AI instances across 3 computers)
    lb.add_backend("computer-a-instance-1", "192.168.1.1", 8001, weight=2)
    lb.add_backend("computer-a-instance-2", "192.168.1.1", 8002, weight=2)
    lb.add_backend("computer-b-instance-3", "192.168.1.2", 8003, weight=1)
    lb.add_backend("computer-b-instance-4", "192.168.1.2", 8004, weight=1)
    lb.add_backend("computer-c-instance-5", "192.168.1.3", 8005, weight=3)
    lb.add_backend("computer-c-instance-6", "192.168.1.3", 8006, weight=3)

    print(f"✅ Added {lb.metrics['total_backends']} backends")

    # Simulate requests with round-robin
    print("\n🔄 Testing ROUND ROBIN strategy:")
    for i in range(6):
        req = Request(f"req-{i}", f"192.168.1.{100+i}", "/api/test")
        backend = lb.select_backend(req)
        print(f"   Request {i} -> {backend.id}")

    # Test least connections
    print("\n📊 Testing LEAST CONNECTIONS strategy:")
    lb.set_strategy(BalancingStrategy.LEAST_CONNECTIONS)

    # Simulate some connections
    lb.acquire_connection(lb.backends["computer-a-instance-1"])
    lb.acquire_connection(lb.backends["computer-a-instance-1"])
    lb.acquire_connection(lb.backends["computer-b-instance-3"])

    for i in range(4):
        req = Request(f"req-{i}", f"192.168.1.{100+i}", "/api/test")
        backend = lb.select_backend(req)
        print(f"   Request {i} -> {backend.id} (connections: {backend.active_connections})")

    # Test IP hash (sticky sessions)
    print("\n🔒 Testing IP HASH strategy (sticky sessions):")
    lb.set_strategy(BalancingStrategy.IP_HASH)

    test_ip = "192.168.1.100"
    for i in range(3):
        req = Request(f"req-{i}", test_ip, "/api/test")
        backend = lb.select_backend(req)
        print(f"   Request {i} from {test_ip} -> {backend.id}")

    # Simulate request completion
    print("\n⏱️  Simulating request completions:")
    backend1 = lb.backends["computer-a-instance-1"]
    backend2 = lb.backends["computer-c-instance-5"]

    lb.release_connection(backend1, response_time=0.05, success=True)
    lb.release_connection(backend1, response_time=0.03, success=True)
    lb.release_connection(backend2, response_time=0.10, success=True)

    print(f"   {backend1.id}: avg response = {backend1.avg_response_time:.3f}s")
    print(f"   {backend2.id}: avg response = {backend2.avg_response_time:.3f}s")

    # Test least response time strategy
    print("\n⚡ Testing LEAST RESPONSE TIME strategy:")
    lb.set_strategy(BalancingStrategy.LEAST_RESPONSE_TIME)

    for i in range(3):
        req = Request(f"req-{i}", f"192.168.1.{100+i}", "/api/test")
        backend = lb.select_backend(req)
        print(f"   Request {i} -> {backend.id} (avg time: {backend.avg_response_time:.3f}s)")

    # Show overall stats
    stats = lb.get_all_stats()
    print(f"\n📈 Overall Statistics:")
    print(f"   Total requests: {stats['metrics']['total_requests']}")
    print(f"   Successful: {stats['metrics']['successful_requests']}")
    print(f"   Failed: {stats['metrics']['failed_requests']}")
    print(f"   Healthy backends: {stats['metrics']['healthy_backends']}/{stats['metrics']['total_backends']}")

    print("\n✅ Load Balancer operational!")
    print("🚀 Ready to distribute load across 6 AI instances!")
