"""
MODULE #32: CACHE SYSTEM
Built: 2025-11-08
High-performance caching with TTL and LRU eviction.
"""

import time
from typing import Any, Optional
from collections import OrderedDict


class Cache:
    """Fast cache with TTL and LRU"""

    def __init__(self, max_size: int = 1000, default_ttl: float = 3600):
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.data = OrderedDict()
        self.timestamps = {}
        self.hits = 0
        self.misses = 0

    def get(self, key: str) -> Optional[Any]:
        """Get cached value"""
        if key not in self.data:
            self.misses += 1
            return None

        # Check TTL
        if time.time() - self.timestamps[key] > self.default_ttl:
            self.delete(key)
            self.misses += 1
            return None

        # LRU: move to end
        self.data.move_to_end(key)
        self.hits += 1
        return self.data[key]

    def set(self, key: str, value: Any, ttl: Optional[float] = None):
        """Set cached value"""
        if key in self.data:
            self.data.move_to_end(key)
        else:
            if len(self.data) >= self.max_size:
                # Evict oldest
                self.data.popitem(last=False)

        self.data[key] = value
        self.timestamps[key] = time.time()

    def delete(self, key: str):
        """Delete from cache"""
        if key in self.data:
            del self.data[key]
            del self.timestamps[key]

    def stats(self):
        """Get cache statistics"""
        total = self.hits + self.misses
        hit_rate = self.hits / total if total > 0 else 0
        return {
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': hit_rate,
            'size': len(self.data)
        }


# Demo
if __name__ == "__main__":
    cache = Cache(max_size=3, default_ttl=10)

    cache.set("key1", "value1")
    cache.set("key2", "value2")

    print(f"Get key1: {cache.get('key1')}")
    print(f"Get key3: {cache.get('key3')}")
    print(f"Stats: {cache.stats()}")
