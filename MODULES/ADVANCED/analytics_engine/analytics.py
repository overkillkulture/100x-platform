"""MODULE #41: ANALYTICS ENGINE - Track metrics, KPIs, conversions"""
import time
from typing import Dict, List
from collections import defaultdict
from dataclasses import dataclass
import json

@dataclass
class Metric:
    name: str
    value: float
    timestamp: float
    tags: Dict[str, str]

class AnalyticsEngine:
    def __init__(self):
        self.metrics: List[Metric] = []
        self.counters: Dict[str, int] = defaultdict(int)
        self.timers: Dict[str, List[float]] = defaultdict(list)

    def track_event(self, event: str, value: float = 1, tags: Dict = None):
        """Track an event"""
        metric = Metric(event, value, time.time(), tags or {})
        self.metrics.append(metric)
        self.counters[event] += 1

    def track_timing(self, operation: str, duration: float):
        """Track timing metrics"""
        self.timers[operation].append(duration)

    def get_kpis(self) -> Dict:
        """Get key performance indicators"""
        return {
            'total_events': len(self.metrics),
            'unique_events': len(self.counters),
            'avg_timings': {k: sum(v)/len(v) for k, v in self.timers.items() if v},
            'top_events': sorted(self.counters.items(), key=lambda x: x[1], reverse=True)[:5]
        }

    def funnel_analysis(self, steps: List[str]) -> Dict:
        """Analyze conversion funnel"""
        funnel = {}
        for i, step in enumerate(steps):
            count = self.counters.get(step, 0)
            funnel[step] = {
                'count': count,
                'conversion': count / self.counters.get(steps[0], 1) if i > 0 else 1.0
            }
        return funnel

if __name__ == "__main__":
    analytics = AnalyticsEngine()
    analytics.track_event("page_view", tags={"page": "home"})
    analytics.track_event("signup", value=1)
    analytics.track_timing("api_call", 0.25)
    print("KPIs:", analytics.get_kpis())
    print("✅ Analytics Engine working!")
