"""MODULE #53: CIRCUIT BREAKER - Fault tolerance for distributed calls"""
import time
import threading
from typing import Callable, Any, Optional
from dataclasses import dataclass
from enum import Enum

class CircuitState(Enum):
    CLOSED = "closed"        # Normal operation
    OPEN = "open"            # Failures exceeded, blocking calls
    HALF_OPEN = "half_open"  # Testing if service recovered

@dataclass
class CircuitBreakerConfig:
    failure_threshold: int = 5
    success_threshold: int = 2
    timeout: float = 60.0  # seconds
    half_open_timeout: float = 30.0

class CircuitBreaker:
    """Circuit breaker pattern for fault-tolerant distributed calls"""

    def __init__(self, name: str, config: Optional[CircuitBreakerConfig] = None):
        self.name = name
        self.config = config or CircuitBreakerConfig()

        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time: Optional[float] = None

        self.lock = threading.RLock()

        self.metrics = {
            'total_calls': 0,
            'successful_calls': 0,
            'failed_calls': 0,
            'rejected_calls': 0,
            'state_changes': 0
        }

    def call(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with circuit breaker protection"""
        with self.lock:
            self.metrics['total_calls'] += 1

            # Check if circuit is open
            if self.state == CircuitState.OPEN:
                if self._should_attempt_reset():
                    self._transition_to_half_open()
                else:
                    self.metrics['rejected_calls'] += 1
                    raise Exception(f"Circuit breaker '{self.name}' is OPEN")

        # Execute function
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result

        except Exception as e:
            self._on_failure()
            raise e

    def _on_success(self):
        """Handle successful call"""
        with self.lock:
            self.metrics['successful_calls'] += 1
            self.failure_count = 0

            if self.state == CircuitState.HALF_OPEN:
                self.success_count += 1

                if self.success_count >= self.config.success_threshold:
                    self._transition_to_closed()

    def _on_failure(self):
        """Handle failed call"""
        with self.lock:
            self.metrics['failed_calls'] += 1
            self.failure_count += 1
            self.last_failure_time = time.time()

            if self.state == CircuitState.HALF_OPEN:
                self._transition_to_open()

            elif self.state == CircuitState.CLOSED:
                if self.failure_count >= self.config.failure_threshold:
                    self._transition_to_open()

    def _should_attempt_reset(self) -> bool:
        """Check if should attempt to reset circuit"""
        if self.last_failure_time is None:
            return False

        elapsed = time.time() - self.last_failure_time
        return elapsed >= self.config.timeout

    def _transition_to_open(self):
        """Transition to OPEN state"""
        self.state = CircuitState.OPEN
        self.metrics['state_changes'] += 1

    def _transition_to_half_open(self):
        """Transition to HALF_OPEN state"""
        self.state = CircuitState.HALF_OPEN
        self.success_count = 0
        self.metrics['state_changes'] += 1

    def _transition_to_closed(self):
        """Transition to CLOSED state"""
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.metrics['state_changes'] += 1

    def reset(self):
        """Manually reset circuit breaker"""
        with self.lock:
            self.state = CircuitState.CLOSED
            self.failure_count = 0
            self.success_count = 0
            self.last_failure_time = None

    def get_status(self) -> dict:
        """Get circuit breaker status"""
        return {
            'name': self.name,
            'state': self.state.value,
            'failure_count': self.failure_count,
            'metrics': self.metrics
        }


if __name__ == "__main__":
    print("⚡ MODULE #53: CIRCUIT BREAKER")
    print("=" * 60)

    # Create circuit breaker
    config = CircuitBreakerConfig(failure_threshold=3, timeout=5.0)
    cb = CircuitBreaker("api-service", config)

    print("✅ Circuit breaker created (threshold=3 failures)")

    # Simulate service calls
    def flaky_service(should_fail=False):
        if should_fail:
            raise Exception("Service unavailable")
        return "Success"

    # Successful calls
    print("\n✅ Making successful calls...")
    for i in range(3):
        try:
            result = cb.call(flaky_service, should_fail=False)
            print(f"   Call {i+1}: {result}")
        except Exception as e:
            print(f"   Call {i+1}: Failed - {e}")

    # Failing calls
    print("\n❌ Making failing calls...")
    for i in range(5):
        try:
            result = cb.call(flaky_service, should_fail=True)
            print(f"   Call {i+1}: {result}")
        except Exception as e:
            print(f"   Call {i+1}: {str(e)[:50]}")

    # Show status
    status = cb.get_status()
    print(f"\n📊 Circuit Breaker Status:")
    print(f"   State: {status['state'].upper()}")
    print(f"   Total calls: {status['metrics']['total_calls']}")
    print(f"   Successful: {status['metrics']['successful_calls']}")
    print(f"   Failed: {status['metrics']['failed_calls']}")
    print(f"   Rejected: {status['metrics']['rejected_calls']}")

    print("\n✅ Circuit Breaker operational!")
    print("🚀 Ready to protect distributed calls!")
