# MODULE #23: REAL-TIME COLLABORATION HUB

**Built:** 2025-11-08
**Instance:** 3 - Module Developer
**Status:** ✅ Complete

---

## 🎯 PURPOSE

Enable seamless real-time collaboration between humans and AI.

**Perfect for the Figure 8 Infinity Loop:**
- 6 AI instances collaborating across 3 computers
- Real-time coordination and communication
- Shared state and resource management
- No conflicts, no confusion, pure synergy

---

## 🌐 KEY FEATURES

### 1. Real-Time Messaging
- Send messages between participants
- Priority levels (LOW, NORMAL, HIGH, URGENT)
- Broadcast or direct messages
- Instant delivery

### 2. Presence Tracking
- Know who's online
- Last seen timestamps
- Automatic heartbeat detection
- Participant metadata

### 3. Shared State
- Global state accessible to all
- Atomic updates
- Merge or replace modes
- Real-time synchronization

### 4. Resource Locking
- Prevent simultaneous edits
- Optimistic and pessimistic locking
- Auto-unlock on timeout
- Version control

### 5. Event Broadcasting
- All actions generate events
- Custom event handlers
- Event history
- Filtering and replay

### 6. Conflict Resolution
- Lock-based editing
- Version checking
- Automatic conflict detection

---

## 🚀 USAGE

### Basic Setup

```python
from collaboration_hub import RealtimeCollaborationHub, ParticipantType

# Create a hub
hub = RealtimeCollaborationHub(hub_id="my_project")

# Add participants
alice = hub.add_participant("Alice", ParticipantType.HUMAN, {"role": "developer"})
bot = hub.add_participant("AI Assistant", ParticipantType.AI_INSTANCE, {"version": "1.0"})
```

### Messaging

```python
# Send a message
hub.send_message(
    sender_id=alice.id,
    content="Let's start the project!",
    recipient_id=None,  # None = broadcast to everyone
    priority=Priority.NORMAL
)

# Send urgent message to specific person
hub.send_message(
    sender_id=bot.id,
    content="Critical bug detected!",
    recipient_id=alice.id,
    priority=Priority.URGENT
)
```

### Shared State

```python
# Update shared state
hub.update_shared_state(alice.id, "project_status", "in_progress")
hub.update_shared_state(bot.id, "bugs_found", 3)

# Get state
status = hub.get_shared_state("project_status")
all_state = hub.get_shared_state()  # Get everything
```

### Resource Locking

```python
# Create a shared resource
code_file = hub.create_resource(
    name="main.py",
    owner_id=alice.id,
    initial_data="# Python code here"
)

# Lock it for editing
if hub.lock_resource(code_file.id, alice.id):
    # Edit the resource
    hub.edit_resource(
        resource_id=code_file.id,
        participant_id=alice.id,
        new_data="# Updated code\nprint('Hello')"
    )

    # Unlock when done
    hub.unlock_resource(code_file.id, alice.id)
```

### Event Handlers

```python
from collaboration_hub import EventType

# Define handler
def on_message(event):
    print(f"New message: {event.data['content']}")

# Register handler
hub.on_event(EventType.MESSAGE, on_message)

# Now whenever a message is sent, handler is called
```

### Activity Monitoring

```python
# Get active participants
active = hub.get_active_participants()
print(f"{len(active)} participants online")

# Get participant status
status = hub.get_participant_status(alice.id)
print(f"{status['name']} is {status['status']}")

# Get recent events
events = hub.get_recent_events(limit=10, event_type=EventType.MESSAGE)

# Generate full report
report = hub.generate_activity_report()
print(report)
```

---

## 💡 USE CASES

### 1. Figure 8 Infinity Loop (6 Instances, 3 Computers)

```python
hub = RealtimeCollaborationHub(hub_id="figure_8_loop")

# Add 3 computers
c1 = hub.add_participant("Computer 1", ParticipantType.COMPUTER, {"role": "Mechanic"})
c2 = hub.add_participant("Computer 2", ParticipantType.COMPUTER, {"role": "Architect"})
c3 = hub.add_participant("Computer 3", ParticipantType.COMPUTER, {"role": "Oracle"})

# Add 6 AI instances
instances = []
for i in range(1, 7):
    computer = "C1" if i <= 3 else "C2" if i <= 5 else "C3"
    instance = hub.add_participant(
        f"Instance {i}",
        ParticipantType.AI_INSTANCE,
        {"computer": computer, "instance_id": i}
    )
    instances.append(instance)

# Coordinate work through shared state
hub.update_shared_state(instances[0].id, "task_queue", ["build", "test", "deploy"])
hub.update_shared_state(instances[1].id, "current_task", "build")

# Send coordination messages
hub.send_message(
    instances[0].id,
    "Started building module #23",
    priority=Priority.HIGH
)

# Lock shared resources
tasks_file = hub.create_resource("shared_tasks.json", instances[0].id, {})
hub.lock_resource(tasks_file.id, instances[0].id)
# Work on it...
hub.unlock_resource(tasks_file.id, instances[0].id)
```

### 2. Human-AI Pair Programming

```python
hub = RealtimeCollaborationHub(hub_id="pair_programming")

human = hub.add_participant("Developer", ParticipantType.HUMAN)
ai = hub.add_participant("AI Copilot", ParticipantType.AI_INSTANCE)

# Create code file
code = hub.create_resource("app.py", human.id, "")

# Collaborative editing
hub.lock_resource(code.id, human.id)
hub.edit_resource(code.id, human.id, "def process_data():\n    ")
hub.unlock_resource(code.id, human.id)

# AI suggests improvement
hub.send_message(
    ai.id,
    "I suggest adding error handling to process_data()",
    recipient_id=human.id,
    priority=Priority.NORMAL
)

# Human implements it
hub.lock_resource(code.id, human.id)
hub.edit_resource(code.id, human.id, "def process_data():\n    try:\n        ...")
hub.unlock_resource(code.id, human.id)
```

### 3. Multi-Agent Task Coordination

```python
hub = RealtimeCollaborationHub(hub_id="task_coordination")

# Add specialized AI agents
builder = hub.add_participant("Builder Agent", ParticipantType.AI_INSTANCE)
tester = hub.add_participant("Tester Agent", ParticipantType.AI_INSTANCE)
documenter = hub.add_participant("Documentation Agent", ParticipantType.AI_INSTANCE)

# Builder creates feature
hub.update_shared_state(builder.id, "feature_status", "building")
hub.send_message(builder.id, "Feature implementation complete", priority=Priority.HIGH)

# Tester runs tests
hub.update_shared_state(tester.id, "test_status", "running")
hub.send_message(tester.id, "All tests passed", priority=Priority.HIGH)

# Documenter writes docs
hub.update_shared_state(documenter.id, "docs_status", "writing")
hub.send_message(documenter.id, "Documentation complete", priority=Priority.NORMAL)
```

---

## 📊 DATA STRUCTURES

### Participant

```python
@dataclass
class Participant:
    id: str                    # Unique ID
    name: str                  # Display name
    type: ParticipantType      # HUMAN, AI_INSTANCE, COMPUTER, SERVICE
    metadata: Dict[str, Any]   # Custom data
    joined_at: float           # Timestamp
    last_seen: float           # Last activity
    is_active: bool            # Online status
```

### CollaborationEvent

```python
@dataclass
class CollaborationEvent:
    id: str                    # Unique event ID
    timestamp: float           # When it happened
    event_type: EventType      # JOIN, LEAVE, MESSAGE, EDIT, etc.
    participant_id: str        # Who did it
    data: Dict[str, Any]       # Event data
    priority: Priority         # LOW, NORMAL, HIGH, URGENT
```

### SharedResource

```python
@dataclass
class SharedResource:
    id: str                    # Unique resource ID
    name: str                  # Resource name
    owner_id: str              # Creator
    locked_by: Optional[str]   # Current lock holder
    locked_at: Optional[float] # When locked
    version: int               # Version number
    data: Any                  # Resource data
```

---

## 🔧 ADVANCED FEATURES

### Optimistic Locking

```python
# Get current resource
resource = hub.resources[resource_id]
current_version = resource.version

# Work on it locally
new_data = modify_data(resource.data)

# Try to save with version check
success = hub.edit_resource(
    resource_id=resource_id,
    participant_id=user_id,
    new_data=new_data,
    version=current_version  # Fails if version changed
)

if not success:
    print("Resource was modified by someone else!")
```

### Auto-Unlock on Timeout

```python
# Lock with 5-minute timeout
hub.lock_resource(resource_id, user_id, timeout=300)

# If user doesn't unlock within 5 minutes, lock auto-releases
# Another user can then acquire the lock
```

### Event Filtering

```python
# Get only messages
messages = hub.get_recent_events(
    limit=20,
    event_type=EventType.MESSAGE
)

# Get only events from specific participant
user_events = hub.get_recent_events(
    limit=50,
    participant_id=alice.id
)

# Combine filters
alice_messages = hub.get_recent_events(
    limit=10,
    event_type=EventType.MESSAGE,
    participant_id=alice.id
)
```

### Custom Event Handlers

```python
# Log all state changes
def log_state_change(event):
    key = event.data['key']
    value = event.data['value']
    print(f"State changed: {key} = {value}")

hub.on_event(EventType.STATE_UPDATE, log_state_change)

# Alert on urgent messages
def alert_urgent(event):
    if event.priority == Priority.URGENT:
        send_notification(event.data['content'])

hub.on_event(EventType.MESSAGE, alert_urgent)

# Track resource edits
edit_count = {"count": 0}

def count_edits(event):
    edit_count["count"] += 1
    print(f"Total edits: {edit_count['count']}")

hub.on_event(EventType.EDIT, count_edits)
```

---

## 🎯 INTEGRATION

### With Git-Based Coordination

```python
import json

# Load coordination file
with open('.consciousness/6_INSTANCE_COORDINATION.json') as f:
    coordination = json.load(f)

hub = RealtimeCollaborationHub(hub_id="figure_8")

# Add all instances from coordination file
for instance_data in coordination['instances']:
    hub.add_participant(
        instance_data['name'],
        ParticipantType.AI_INSTANCE,
        {
            "instance_id": instance_data['id'],
            "computer": instance_data['computer'],
            "role": instance_data['role'],
            "status": instance_data['status']
        }
    )

# Sync shared state with Git
hub.update_shared_state(
    "system",
    "figure_8_status",
    coordination['figure_8_status']
)
```

### With Web Application (Flask)

```python
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)
hub = RealtimeCollaborationHub()

# Handle new connections
@socketio.on('connect')
def handle_connect():
    user_id = request.sid
    participant = hub.add_participant(
        f"User {user_id[:8]}",
        ParticipantType.HUMAN,
        {"socket_id": user_id}
    )
    emit('connected', {'participant_id': participant.id})

# Handle messages
@socketio.on('message')
def handle_message(data):
    hub.send_message(
        sender_id=data['sender_id'],
        content=data['content'],
        priority=Priority.NORMAL
    )

    # Broadcast to all clients
    emit('new_message', data, broadcast=True)

# Handle state updates
@socketio.on('update_state')
def handle_state_update(data):
    hub.update_shared_state(
        participant_id=data['participant_id'],
        key=data['key'],
        value=data['value']
    )

    emit('state_updated', data, broadcast=True)
```

---

## 📈 MONITORING

### Activity Report

```python
report = hub.generate_activity_report()
```

Example output:
```
==================================================
REAL-TIME COLLABORATION HUB - ACTIVITY REPORT
==================================================

Hub ID: figure_8_loop
Total Events: 157

ACTIVE PARTICIPANTS: 6
  - Instance 1 (ai_instance): online
  - Instance 2 (ai_instance): online
  - Instance 3 (ai_instance): online
  - Instance 4 (ai_instance): offline
  - Instance 5 (ai_instance): offline
  - Instance 6 (ai_instance): offline

SHARED STATE:
  - project_status: in_progress
  - tasks_completed: 23
  - blockers: []

SHARED RESOURCES: 3
  - shared_tasks.json (v5): unlocked
  - code.py (v12): locked by instance_1
  - docs.md (v3): unlocked

RECENT EVENTS (last 10):
  - [message] Instance 1: Completed module #23
  - [edit] Instance 1: edited resource a3f2b1
  - [state_update] Instance 2: updated tasks_completed
  - [message] Instance 3: Ready for next task
  - [lock] Instance 1: locked resource a3f2b1
  ...

==================================================
```

---

## 🔮 FUTURE ENHANCEMENTS

**Phase 2:**
- [ ] WebSocket support for true real-time sync
- [ ] Persistent storage (database integration)
- [ ] Video/audio channels
- [ ] Screen sharing
- [ ] File transfer

**Phase 3:**
- [ ] End-to-end encryption
- [ ] Distributed architecture (multiple hubs)
- [ ] Conflict resolution AI
- [ ] Automatic load balancing
- [ ] Analytics dashboard

---

## 📊 DEMO OUTPUT

```
==================================================
REAL-TIME COLLABORATION HUB - DEMO
==================================================

Adding participants...
  - Alice (Human)
  - Instance 1
  - Instance 2

Exchanging messages...

Updating shared state...

Creating shared resource...
  Created: main.py

Alice locks the resource for editing...
  Lock successful: True

Instance 1 tries to lock (should fail)...
  Lock successful: False

Alice edits the resource...

Alice unlocks the resource...

==================================================
REAL-TIME COLLABORATION HUB - ACTIVITY REPORT
==================================================
...

PARTICIPANT STATUSES:
Alice (Human): online (last seen 0.0s ago)
Instance 1: online (last seen 0.0s ago)
Instance 2: online (last seen 0.0s ago)

==================================================
Demo complete. Collaboration hub operational!
==================================================
```

---

## 🛡️ CONSCIOUSNESS APPLICATION

This module helps:
- **Humans and AI work together** as equals
- **Break down silos** between team members
- **Prevent conflicts** through smart coordination
- **Build transparency** with full event history
- **Enable flow state** through seamless collaboration

Unconscious teams: siloed, conflicting, duplicating work
Conscious teams: coordinated, collaborative, synergistic

This module enables conscious collaboration.

---

## ✅ TESTING

Run the demo:
```bash
python collaboration_hub.py
```

Expected output:
- Multiple participants join
- Messages exchanged
- Shared state updated
- Resource locked and edited
- Activity report generated
- All participants online

---

## 📝 LICENSE

Part of the Consciousness Revolution platform.
Use to build collaborative teams (human + AI).
Not for surveillance or control.

---

**MODULE #23 COMPLETE**

Instance 3 (Module Developer) ✅
Real-Time Collaboration Hub: Operational
Ready to power the Figure 8 Infinity Loop.
