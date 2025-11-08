"""
MODULE #33: API GATEWAY
Built: 2025-11-08
Rate limiting, authentication, routing for APIs.
"""

import time
from typing import Dict, Callable, Optional
from collections import defaultdict


class RateLimiter:
    """Token bucket rate limiter"""

    def __init__(self, rate: int, per: float):
        self.rate = rate  # requests
        self.per = per    # seconds
        self.buckets = defaultdict(lambda: {'tokens': rate, 'last': time.time()})

    def allow(self, key: str) -> bool:
        """Check if request allowed"""
        bucket = self.buckets[key]
        now = time.time()

        # Refill tokens
        elapsed = now - bucket['last']
        bucket['tokens'] = min(self.rate, bucket['tokens'] + elapsed * (self.rate / self.per))
        bucket['last'] = now

        # Check if can consume
        if bucket['tokens'] >= 1:
            bucket['tokens'] -= 1
            return True

        return False


class APIGateway:
    """API Gateway with routing and rate limiting"""

    def __init__(self):
        self.routes: Dict[str, Callable] = {}
        self.rate_limiter = RateLimiter(rate=100, per=60)  # 100 req/min
        self.metrics = defaultdict(int)

    def route(self, path: str):
        """Register route"""
        def decorator(func):
            self.routes[path] = func
            return func
        return decorator

    def handle(self, path: str, user_id: str, **kwargs):
        """Handle API request"""

        # Rate limiting
        if not self.rate_limiter.allow(user_id):
            self.metrics['rate_limited'] += 1
            return {'error': 'Rate limit exceeded'}

        # Routing
        if path not in self.routes:
            self.metrics['not_found'] += 1
            return {'error': 'Not found'}

        # Execute
        self.metrics['success'] += 1
        return self.routes[path](**kwargs)


# Demo
if __name__ == "__main__":
    gateway = APIGateway()

    @gateway.route("/hello")
    def hello(name="World"):
        return {'message': f'Hello {name}'}

    # Test
    print(gateway.handle("/hello", "user1", name="Alice"))
    print(gateway.handle("/unknown", "user1"))
    print(f"Metrics: {dict(gateway.metrics)}")
