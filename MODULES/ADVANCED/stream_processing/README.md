# MODULE #50: STREAM PROCESSING ENGINE

Real-time stream processing with windowing, filtering, transformations, and aggregations. Process continuous data streams from 6 AI instances.

## Features

- **Event Streams**: Process continuous data in real-time
- **Windowing**: Tumbling, Sliding, and Session windows
- **Filtering**: Filter events based on predicates
- **Mapping**: Transform events through pipeline
- **Aggregations**: Count, sum, avg, max, min, custom
- **Grouping**: Group events by keys
- **Stream Joins**: Join events from multiple streams
- **Sinks**: Output to multiple destinations

## Usage

```python
from stream_processing import StreamProcessor

# Create stream processor
stream = StreamProcessor("my-stream")

# Set up processing pipeline
stream.filter(lambda e: e.data.get('value', 0) > 100)  # Only high values
stream.map(lambda e: enrich_event(e))                  # Transform
stream.sink(lambda e: print(e.data))                   # Output

# Emit events
stream.emit("event-1", {"value": 150, "user": "alice"})
stream.emit("event-2", {"value": 200, "user": "bob"})

# Events automatically flow through pipeline
```

## Windowing

### Tumbling Windows (Non-overlapping)

```python
# 10-second tumbling windows
stream.tumbling_window(window_size=10.0)

# Emit events
for i in range(100):
    stream.emit(f"event-{i}", {"value": i})
    time.sleep(0.1)

# Get windows
windows = stream.get_windows()

# Aggregate each window
for window in windows:
    agg = stream.aggregate_window(window, {
        'count': lambda events: len(events),
        'sum': lambda events: sum(e.data['value'] for e in events)
    })
    print(f"Window: count={agg['count']}, sum={agg['sum']}")
```

### Sliding Windows (Overlapping)

```python
# 30-second windows, sliding every 10 seconds
stream.sliding_window(window_size=30.0, slide_interval=10.0)
```

### Session Windows (Activity-based)

```python
# Session window with 5-minute timeout
stream.session_window(timeout=300.0)

# Events with same key are grouped into sessions
stream.emit("e1", {"value": 1}, key="user-123")
stream.emit("e2", {"value": 2}, key="user-123")  # Same session
# ... 6 minutes later ...
stream.emit("e3", {"value": 3}, key="user-123")  # New session
```

## Filtering & Mapping

```python
# Filter events
stream.filter(lambda e: e.data.get('type') == 'important')
stream.filter(lambda e: e.data.get('value', 0) > 50)

# Transform events
def enrich(event):
    event.data['processed_at'] = time.time()
    event.data['double'] = event.data.get('value', 0) * 2
    return event

stream.map(enrich)

# Multiple transformations are chained
stream.map(transform1).map(transform2).map(transform3)
```

## Aggregations

```python
# Define aggregation functions
aggregators = {
    'count': lambda events: len(events),
    'sum': lambda events: sum(e.data.get('value', 0) for e in events),
    'avg': lambda events: sum(e.data.get('value', 0) for e in events) / len(events),
    'max': lambda events: max((e.data.get('value', 0) for e in events), default=0),
    'min': lambda events: min((e.data.get('value', 0) for e in events), default=0)
}

# Apply to window
window = stream.get_windows()[0]
results = stream.aggregate_window(window, aggregators)

print(results['count'])  # 100
print(results['avg'])    # 50.5
```

## Grouping

```python
# Group by key function
groups = stream.group_by(lambda e: e.data.get('user'))

for user, events in groups.items():
    print(f"{user}: {len(events)} events")

# Count by field
counts = stream.count_by_key('instance_id')
print(counts)  # {'instance-1': 10, 'instance-2': 15, ...}
```

## Stream Joins

```python
# Create two streams
stream1 = StreamProcessor("stream-1")
stream2 = StreamProcessor("stream-2")

# Emit correlated events
stream1.emit("e1", {"user_id": "alice", "action": "login"})
stream2.emit("e2", {"user_id": "alice", "location": "NYC"})

# Join on 'user_id' within 60 second window
joined = stream1.join_streams(stream2, join_key='user_id', window_seconds=60.0)

for event1, event2 in joined:
    print(f"User {event1.data['user_id']}: {event1.data['action']} from {event2.data['location']}")
```

## Sinks (Output)

```python
# Add multiple output sinks
stream.sink(lambda e: print(e.data))                    # Console
stream.sink(lambda e: save_to_db(e))                    # Database
stream.sink(lambda e: send_to_kafka(e))                 # Message queue
stream.sink(lambda e: update_dashboard(e))              # Dashboard
```

## Time-based Queries

```python
# Get recent events
recent = stream.get_recent_events(count=10)

# Get events in time range
import time
start = time.time() - 3600  # Last hour
end = time.time()
events = stream.get_events_in_range(start, end)
```

## Monitoring

```python
# Get metrics
metrics = stream.get_metrics()
print(metrics['events_received'])
print(metrics['events_processed'])
print(metrics['events_filtered'])
print(metrics['windows_created'])

# Clean up old windows
removed = stream.clear_old_windows()
print(f"Removed {removed} old windows")

# Reset stream
stream.reset()
```

**#50 COMPLETE** ✅
