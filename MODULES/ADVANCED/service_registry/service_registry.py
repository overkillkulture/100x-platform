"""MODULE #54: SERVICE REGISTRY - Service discovery for 6 AI instances"""
import time
import threading
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

@dataclass
class ServiceInstance:
    service_name: str
    instance_id: str
    host: str
    port: int
    metadata: Dict[str, Any] = field(default_factory=dict)
    health_check_url: Optional[str] = None
    registered_at: float = field(default_factory=time.time)
    last_heartbeat: float = field(default_factory=time.time)

    def is_healthy(self, timeout: float = 30.0) -> bool:
        return (time.time() - self.last_heartbeat) < timeout

class ServiceRegistry:
    """Service discovery registry for distributed AI instances"""

    def __init__(self):
        self.services: Dict[str, List[ServiceInstance]] = {}
        self.lock = threading.RLock()
        self.metrics = {
            'total_services': 0,
            'total_instances': 0,
            'registrations': 0,
            'deregistrations': 0
        }

    def register(self, service_name: str, instance_id: str, host: str, port: int,
                metadata: Dict[str, Any] = None, health_check_url: str = None) -> ServiceInstance:
        """Register service instance"""
        instance = ServiceInstance(
            service_name=service_name,
            instance_id=instance_id,
            host=host,
            port=port,
            metadata=metadata or {},
            health_check_url=health_check_url
        )

        with self.lock:
            if service_name not in self.services:
                self.services[service_name] = []
                self.metrics['total_services'] += 1

            self.services[service_name].append(instance)
            self.metrics['total_instances'] += 1
            self.metrics['registrations'] += 1

        return instance

    def deregister(self, service_name: str, instance_id: str) -> bool:
        """Deregister service instance"""
        with self.lock:
            if service_name not in self.services:
                return False

            instances = self.services[service_name]
            original_count = len(instances)

            self.services[service_name] = [
                inst for inst in instances if inst.instance_id != instance_id
            ]

            if len(self.services[service_name]) < original_count:
                self.metrics['total_instances'] -= 1
                self.metrics['deregistrations'] += 1

                if not self.services[service_name]:
                    del self.services[service_name]
                    self.metrics['total_services'] -= 1

                return True

        return False

    def discover(self, service_name: str, healthy_only: bool = True) -> List[ServiceInstance]:
        """Discover instances of a service"""
        with self.lock:
            instances = self.services.get(service_name, [])

            if healthy_only:
                return [inst for inst in instances if inst.is_healthy()]

            return list(instances)

    def heartbeat(self, service_name: str, instance_id: str) -> bool:
        """Update instance heartbeat"""
        with self.lock:
            instances = self.services.get(service_name, [])

            for inst in instances:
                if inst.instance_id == instance_id:
                    inst.last_heartbeat = time.time()
                    return True

        return False

    def get_all_services(self) -> List[str]:
        """Get all registered service names"""
        return list(self.services.keys())

    def get_instance(self, service_name: str, instance_id: str) -> Optional[ServiceInstance]:
        """Get specific instance"""
        with self.lock:
            instances = self.services.get(service_name, [])

            for inst in instances:
                if inst.instance_id == instance_id:
                    return inst

        return None

    def get_metrics(self) -> Dict[str, Any]:
        """Get registry metrics"""
        return dict(self.metrics)


if __name__ == "__main__":
    print("🔍 MODULE #54: SERVICE REGISTRY")
    print("=" * 60)

    registry = ServiceRegistry()

    print("✅ Service registry created")

    # Register 6 AI instances
    print("\n📝 Registering 6 AI instances...")
    registry.register("ai-instance", "instance-1", "192.168.1.1", 8001,
                     {"role": "coordinator", "computer": "A"})
    registry.register("ai-instance", "instance-2", "192.168.1.1", 8002,
                     {"role": "worker", "computer": "A"})
    registry.register("ai-instance", "instance-3", "192.168.1.2", 8003,
                     {"role": "worker", "computer": "B"})
    registry.register("ai-instance", "instance-4", "192.168.1.2", 8004,
                     {"role": "worker", "computer": "B"})
    registry.register("ai-instance", "instance-5", "192.168.1.3", 8005,
                     {"role": "coordinator", "computer": "C"})
    registry.register("ai-instance", "instance-6", "192.168.1.3", 8006,
                     {"role": "worker", "computer": "C"})

    print(f"   Registered 6 instances")

    # Discover instances
    print("\n🔍 Discovering AI instances...")
    instances = registry.discover("ai-instance")
    print(f"   Found {len(instances)} healthy instances")

    for inst in instances[:3]:
        print(f"   - {inst.instance_id} at {inst.host}:{inst.port} "
              f"({inst.metadata['role']})")

    # Send heartbeat
    print("\n💓 Sending heartbeat from instance-1...")
    registry.heartbeat("ai-instance", "instance-1")

    # Get metrics
    metrics = registry.get_metrics()
    print(f"\n📊 Registry Metrics:")
    print(f"   Total services: {metrics['total_services']}")
    print(f"   Total instances: {metrics['total_instances']}")
    print(f"   Registrations: {metrics['registrations']}")

    print("\n✅ Service Registry operational!")
    print("🚀 Ready for service discovery across 6 instances!")
