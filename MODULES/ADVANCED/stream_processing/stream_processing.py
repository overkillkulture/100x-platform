"""MODULE #50: STREAM PROCESSING ENGINE - Real-time data stream processing"""
import time
import threading
from typing import List, Dict, Any, Callable, Optional
from dataclasses import dataclass, field
from collections import deque, defaultdict
from enum import Enum
import json

class WindowType(Enum):
    TUMBLING = "tumbling"  # Non-overlapping fixed windows
    SLIDING = "sliding"    # Overlapping windows
    SESSION = "session"    # Activity-based windows

@dataclass
class StreamEvent:
    id: str
    timestamp: float
    data: Dict[str, Any]
    key: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Window:
    start_time: float
    end_time: float
    events: List[StreamEvent] = field(default_factory=list)
    aggregates: Dict[str, Any] = field(default_factory=dict)

    def add_event(self, event: StreamEvent):
        self.events.append(event)

    def contains(self, timestamp: float) -> bool:
        return self.start_time <= timestamp < self.end_time

class StreamProcessor:
    """
    Real-time stream processing engine with windowing, filtering, and aggregation.
    Perfect for processing continuous data from 6 AI instances.
    """

    def __init__(self, name: str):
        self.name = name

        # Event storage
        self.events: deque = deque(maxlen=10000)  # Keep last 10k events

        # Processing pipeline
        self.filters: List[Callable] = []
        self.mappers: List[Callable] = []
        self.reducers: List[Callable] = []
        self.sinks: List[Callable] = []

        # Windowing
        self.windows: Dict[str, Window] = {}
        self.window_type: Optional[WindowType] = None
        self.window_size: float = 0
        self.slide_interval: float = 0
        self.session_timeout: float = 300.0  # 5 minutes

        # State
        self.state: Dict[str, Any] = {}
        self.lock = threading.RLock()

        # Metrics
        self.metrics = {
            'events_received': 0,
            'events_processed': 0,
            'events_filtered': 0,
            'windows_created': 0,
            'processing_errors': 0
        }

    def emit(self, event_id: str, data: Dict[str, Any], key: Optional[str] = None):
        """Emit an event into the stream"""
        with self.lock:
            event = StreamEvent(
                id=event_id,
                timestamp=time.time(),
                data=data,
                key=key
            )

            self.events.append(event)
            self.metrics['events_received'] += 1

            # Process event through pipeline
            self._process_event(event)

    def _process_event(self, event: StreamEvent):
        """Process event through the pipeline"""
        try:
            # Apply filters
            for filter_func in self.filters:
                if not filter_func(event):
                    self.metrics['events_filtered'] += 1
                    return

            # Apply mappers (transformations)
            current_event = event
            for mapper_func in self.mappers:
                current_event = mapper_func(current_event)

            # Add to windows if windowing is enabled
            if self.window_type:
                self._add_to_windows(current_event)

            # Apply sinks (output)
            for sink_func in self.sinks:
                sink_func(current_event)

            self.metrics['events_processed'] += 1

        except Exception as e:
            self.metrics['processing_errors'] += 1
            print(f"Processing error: {e}")

    def filter(self, predicate: Callable[[StreamEvent], bool]):
        """Add a filter to the pipeline"""
        self.filters.append(predicate)
        return self

    def map(self, transform: Callable[[StreamEvent], StreamEvent]):
        """Add a transformation to the pipeline"""
        self.mappers.append(transform)
        return self

    def sink(self, output: Callable[[StreamEvent], None]):
        """Add an output sink to the pipeline"""
        self.sinks.append(output)
        return self

    def tumbling_window(self, window_size: float):
        """Set up tumbling (non-overlapping) windows"""
        self.window_type = WindowType.TUMBLING
        self.window_size = window_size
        return self

    def sliding_window(self, window_size: float, slide_interval: float):
        """Set up sliding (overlapping) windows"""
        self.window_type = WindowType.SLIDING
        self.window_size = window_size
        self.slide_interval = slide_interval
        return self

    def session_window(self, timeout: float):
        """Set up session windows (activity-based)"""
        self.window_type = WindowType.SESSION
        self.session_timeout = timeout
        return self

    def _add_to_windows(self, event: StreamEvent):
        """Add event to appropriate window(s)"""
        with self.lock:
            if self.window_type == WindowType.TUMBLING:
                self._add_to_tumbling_window(event)
            elif self.window_type == WindowType.SLIDING:
                self._add_to_sliding_windows(event)
            elif self.window_type == WindowType.SESSION:
                self._add_to_session_window(event)

    def _add_to_tumbling_window(self, event: StreamEvent):
        """Add event to tumbling window"""
        # Calculate window start
        window_index = int(event.timestamp // self.window_size)
        window_start = window_index * self.window_size
        window_end = window_start + self.window_size

        window_key = f"tumbling-{window_index}"

        if window_key not in self.windows:
            self.windows[window_key] = Window(
                start_time=window_start,
                end_time=window_end
            )
            self.metrics['windows_created'] += 1

        self.windows[window_key].add_event(event)

    def _add_to_sliding_windows(self, event: StreamEvent):
        """Add event to all applicable sliding windows"""
        current_time = event.timestamp

        # Create windows that should contain this event
        window_count = int(self.window_size / self.slide_interval)

        for i in range(window_count):
            window_start = (int(current_time // self.slide_interval) - i) * self.slide_interval
            window_end = window_start + self.window_size

            if window_start <= current_time < window_end:
                window_key = f"sliding-{window_start}"

                if window_key not in self.windows:
                    self.windows[window_key] = Window(
                        start_time=window_start,
                        end_time=window_end
                    )
                    self.metrics['windows_created'] += 1

                self.windows[window_key].add_event(event)

    def _add_to_session_window(self, event: StreamEvent):
        """Add event to session window (grouped by key)"""
        key = event.key or "default"
        session_key = f"session-{key}"

        # Find or create session window
        if session_key in self.windows:
            window = self.windows[session_key]

            # Check if event is within timeout
            if event.timestamp - window.end_time > self.session_timeout:
                # Start new session
                self.windows[session_key] = Window(
                    start_time=event.timestamp,
                    end_time=event.timestamp
                )
                self.metrics['windows_created'] += 1
            else:
                # Extend session
                window.end_time = event.timestamp

        else:
            # Create new session
            self.windows[session_key] = Window(
                start_time=event.timestamp,
                end_time=event.timestamp
            )
            self.metrics['windows_created'] += 1

        self.windows[session_key].add_event(event)

    def get_windows(self, active_only: bool = False) -> List[Window]:
        """Get all windows"""
        with self.lock:
            if active_only:
                current_time = time.time()
                return [w for w in self.windows.values()
                       if w.end_time > current_time]
            return list(self.windows.values())

    def aggregate_window(self, window: Window, aggregators: Dict[str, Callable]) -> Dict[str, Any]:
        """
        Aggregate events in a window using provided aggregation functions.

        Example aggregators:
        {
            'count': lambda events: len(events),
            'sum': lambda events: sum(e.data.get('value', 0) for e in events),
            'avg': lambda events: sum(e.data.get('value', 0) for e in events) / len(events)
        }
        """
        results = {}

        for name, func in aggregators.items():
            try:
                results[name] = func(window.events)
            except Exception as e:
                results[name] = None
                print(f"Aggregation error for {name}: {e}")

        window.aggregates = results
        return results

    def group_by(self, key_func: Callable[[StreamEvent], str],
                 max_events: int = 1000) -> Dict[str, List[StreamEvent]]:
        """Group recent events by a key function"""
        with self.lock:
            groups = defaultdict(list)

            for event in list(self.events)[-max_events:]:
                key = key_func(event)
                groups[key].append(event)

            return dict(groups)

    def count_by_key(self, key_field: str, max_events: int = 1000) -> Dict[str, int]:
        """Count events by a specific key field"""
        with self.lock:
            counts = defaultdict(int)

            for event in list(self.events)[-max_events:]:
                key = event.data.get(key_field, "unknown")
                counts[str(key)] += 1

            return dict(counts)

    def get_recent_events(self, count: int = 10) -> List[StreamEvent]:
        """Get most recent events"""
        with self.lock:
            return list(self.events)[-count:]

    def get_events_in_range(self, start_time: float, end_time: float) -> List[StreamEvent]:
        """Get events within a time range"""
        with self.lock:
            return [e for e in self.events
                   if start_time <= e.timestamp <= end_time]

    def join_streams(self, other_stream: 'StreamProcessor',
                    join_key: str, window_seconds: float = 60.0) -> List[Tuple[StreamEvent, StreamEvent]]:
        """Join events from two streams based on a key within a time window"""
        with self.lock:
            current_time = time.time()
            cutoff = current_time - window_seconds

            # Get recent events from both streams
            events1 = [e for e in self.events if e.timestamp >= cutoff]
            events2 = [e for e in other_stream.events if e.timestamp >= cutoff]

            # Join on key
            joined = []
            for e1 in events1:
                key1 = e1.data.get(join_key)
                if key1 is None:
                    continue

                for e2 in events2:
                    key2 = e2.data.get(join_key)
                    if key1 == key2:
                        joined.append((e1, e2))

            return joined

    def clear_old_windows(self, before_time: Optional[float] = None):
        """Clear windows before a specific time"""
        with self.lock:
            if before_time is None:
                before_time = time.time()

            to_remove = [
                key for key, window in self.windows.items()
                if window.end_time < before_time
            ]

            for key in to_remove:
                del self.windows[key]

            return len(to_remove)

    def get_metrics(self) -> Dict[str, Any]:
        """Get stream processing metrics"""
        with self.lock:
            return {
                **self.metrics,
                'current_events': len(self.events),
                'active_windows': len(self.windows),
                'filters': len(self.filters),
                'mappers': len(self.mappers),
                'sinks': len(self.sinks)
            }

    def reset(self):
        """Reset the stream processor"""
        with self.lock:
            self.events.clear()
            self.windows.clear()
            self.filters.clear()
            self.mappers.clear()
            self.sinks.clear()
            self.state.clear()
            self.metrics = {
                'events_received': 0,
                'events_processed': 0,
                'events_filtered': 0,
                'windows_created': 0,
                'processing_errors': 0
            }


if __name__ == "__main__":
    print("🌊 MODULE #50: STREAM PROCESSING ENGINE")
    print("=" * 60)

    # Create stream processor
    stream = StreamProcessor("ai-instance-stream")

    # Set up pipeline
    print("⚙️  Setting up processing pipeline...")

    # Filter: Only process events with value > 50
    stream.filter(lambda e: e.data.get('value', 0) > 50)

    # Map: Transform events
    def enrich_event(event):
        event.data['enriched'] = True
        event.data['double_value'] = event.data.get('value', 0) * 2
        return event

    stream.map(enrich_event)

    # Sink: Print processed events
    processed_events = []
    stream.sink(lambda e: processed_events.append(e))

    print("✅ Pipeline configured: Filter -> Map -> Sink")

    # Set up tumbling window (5 second windows)
    stream.tumbling_window(window_size=5.0)
    print("✅ Tumbling window: 5 seconds")

    # Emit events
    print("\n📤 Emitting events...")
    for i in range(20):
        stream.emit(
            event_id=f"event-{i}",
            data={
                'value': i * 10,
                'instance': f"instance-{(i % 6) + 1}",
                'timestamp': time.time()
            },
            key=f"instance-{(i % 6) + 1}"
        )
        time.sleep(0.1)

    # Check processed events
    print(f"\n✅ Processed {len(processed_events)} events (filtered: {stream.metrics['events_filtered']})")
    print(f"   Sample: value={processed_events[0].data['value']}, "
          f"double={processed_events[0].data['double_value']}")

    # Aggregate windows
    print("\n📊 Aggregating windows...")
    windows = stream.get_windows()

    aggregators = {
        'count': lambda events: len(events),
        'sum': lambda events: sum(e.data.get('value', 0) for e in events),
        'avg': lambda events: sum(e.data.get('value', 0) for e in events) / len(events) if events else 0,
        'max': lambda events: max((e.data.get('value', 0) for e in events), default=0)
    }

    for i, window in enumerate(windows[:3]):
        agg = stream.aggregate_window(window, aggregators)
        print(f"   Window {i+1}: count={agg['count']}, sum={agg['sum']}, "
              f"avg={agg['avg']:.1f}, max={agg['max']}")

    # Group by instance
    print("\n🔑 Grouping by instance...")
    groups = stream.group_by(lambda e: e.data.get('instance', 'unknown'))
    for instance_id, events in sorted(groups.items())[:3]:
        print(f"   {instance_id}: {len(events)} events")

    # Count by instance
    counts = stream.count_by_key('instance')
    print(f"\n📈 Event counts by instance:")
    for instance, count in sorted(counts.items()):
        print(f"   {instance}: {count} events")

    # Create second stream and join
    print("\n🔗 Testing stream join...")
    stream2 = StreamProcessor("second-stream")

    # Emit correlated events
    for i in range(5):
        stream2.emit(
            f"event-{i}",
            data={'value': i * 20, 'instance': f"instance-{i+1}"}
        )

    # Join on 'instance' field
    joined = stream.join_streams(stream2, join_key='instance', window_seconds=60.0)
    print(f"   Joined {len(joined)} event pairs")
    if joined:
        e1, e2 = joined[0]
        print(f"   Sample join: {e1.data['instance']} (v1={e1.data['value']}, v2={e2.data['value']})")

    # Show metrics
    metrics = stream.get_metrics()
    print(f"\n📊 Stream Metrics:")
    print(f"   Events received: {metrics['events_received']}")
    print(f"   Events processed: {metrics['events_processed']}")
    print(f"   Events filtered: {metrics['events_filtered']}")
    print(f"   Windows created: {metrics['windows_created']}")
    print(f"   Current events in buffer: {metrics['current_events']}")

    print("\n✅ Stream Processing Engine operational!")
    print("🚀 Ready to process real-time data from 6 AI instances!")
