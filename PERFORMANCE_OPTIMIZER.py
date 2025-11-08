"""
PERFORMANCE OPTIMIZER
Profile code, find bottlenecks, suggest optimizations
"""

import time
import functools
from typing import Callable, Dict, List
from dataclasses import dataclass

@dataclass
class ProfileResult:
    function_name: str
    calls: int
    total_time: float
    avg_time: float
    max_time: float
    min_time: float

class PerformanceOptimizer:
    def __init__(self):
        self.profiles: Dict[str, List[float]] = {}

    def profile(self, func: Callable) -> Callable:
        """Decorator to profile function performance"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            duration = time.time() - start

            func_name = func.__name__
            if func_name not in self.profiles:
                self.profiles[func_name] = []
            self.profiles[func_name].append(duration)

            return result
        return wrapper

    def get_report(self) -> List[ProfileResult]:
        """Generate performance report"""
        results = []

        for func_name, timings in self.profiles.items():
            if timings:
                result = ProfileResult(
                    function_name=func_name,
                    calls=len(timings),
                    total_time=sum(timings),
                    avg_time=sum(timings) / len(timings),
                    max_time=max(timings),
                    min_time=min(timings)
                )
                results.append(result)

        # Sort by total time
        results.sort(key=lambda x: x.total_time, reverse=True)
        return results

    def suggest_optimizations(self) -> List[str]:
        """Suggest performance optimizations"""
        suggestions = []
        results = self.get_report()

        for result in results:
            if result.avg_time > 1.0:
                suggestions.append(
                    f"⚠️  {result.function_name} is slow (avg: {result.avg_time:.3f}s) - "
                    f"Consider caching or optimization"
                )
            if result.max_time > result.avg_time * 10:
                suggestions.append(
                    f"⚠️  {result.function_name} has inconsistent performance - "
                    f"Max time {result.max_time:.3f}s vs avg {result.avg_time:.3f}s"
                )

        return suggestions

    def print_report(self):
        """Print formatted report"""
        print("=" * 70)
        print("PERFORMANCE OPTIMIZER - PROFILING REPORT")
        print("=" * 70)
        print()

        results = self.get_report()

        for result in results:
            print(f"Function: {result.function_name}")
            print(f"  Calls: {result.calls}")
            print(f"  Total Time: {result.total_time:.3f}s")
            print(f"  Avg Time: {result.avg_time:.3f}s")
            print(f"  Min/Max: {result.min_time:.3f}s / {result.max_time:.3f}s")
            print()

        suggestions = self.suggest_optimizations()
        if suggestions:
            print("OPTIMIZATION SUGGESTIONS:")
            for suggestion in suggestions:
                print(f"  {suggestion}")
            print()

        print("=" * 70)


if __name__ == "__main__":
    optimizer = PerformanceOptimizer()

    @optimizer.profile
    def slow_function():
        time.sleep(0.1)
        return "done"

    @optimizer.profile
    def fast_function():
        return sum(range(1000))

    # Run functions
    for _ in range(10):
        slow_function()
        fast_function()

    optimizer.print_report()
    print("✅ Performance Optimizer working!")
