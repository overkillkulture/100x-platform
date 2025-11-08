"""
MODULE #23: REAL-TIME COLLABORATION HUB
Instance 3: Module Developer
Built: 2025-11-08

Enable seamless real-time collaboration between humans and AI.
Perfect for the Figure 8 Infinity Loop - connecting 6 instances across 3 computers.
"""

import json
import time
import uuid
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict
import threading
from queue import Queue


class ParticipantType(Enum):
    """Types of participants"""
    HUMAN = "human"
    AI_INSTANCE = "ai_instance"
    COMPUTER = "computer"
    SERVICE = "service"


class EventType(Enum):
    """Types of collaboration events"""
    JOIN = "join"
    LEAVE = "leave"
    MESSAGE = "message"
    STATE_UPDATE = "state_update"
    EDIT = "edit"
    LOCK = "lock"
    UNLOCK = "unlock"
    SYNC = "sync"
    HEARTBEAT = "heartbeat"


class Priority(Enum):
    """Message priority levels"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


@dataclass
class Participant:
    """Represents a collaborator"""
    id: str
    name: str
    type: ParticipantType
    metadata: Dict[str, Any]
    joined_at: float
    last_seen: float
    is_active: bool = True


@dataclass
class CollaborationEvent:
    """Represents an event in the collaboration"""
    id: str
    timestamp: float
    event_type: EventType
    participant_id: str
    data: Dict[str, Any]
    priority: Priority


@dataclass
class SharedResource:
    """Resource that can be locked for editing"""
    id: str
    name: str
    owner_id: Optional[str]
    locked_by: Optional[str]
    locked_at: Optional[float]
    version: int
    data: Any


class RealtimeCollaborationHub:
    """
    Real-time collaboration system for humans and AI.

    Features:
    - Real-time messaging
    - Presence tracking (who's online)
    - Shared state management
    - Resource locking (prevent conflicts)
    - Event broadcasting
    - Conflict resolution
    - History tracking
    """

    def __init__(self, hub_id: str = None):
        self.hub_id = hub_id or str(uuid.uuid4())
        self.participants: Dict[str, Participant] = {}
        self.events: List[CollaborationEvent] = []
        self.shared_state: Dict[str, Any] = {}
        self.resources: Dict[str, SharedResource] = {}
        self.event_handlers: Dict[EventType, List[Callable]] = defaultdict(list)
        self.message_queue: Queue = Queue()
        self.is_running = False
        self._lock = threading.Lock()

    def add_participant(
        self,
        name: str,
        participant_type: ParticipantType,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Participant:
        """
        Add a new participant to the collaboration

        Args:
            name: Participant name
            participant_type: Type of participant
            metadata: Additional information

        Returns:
            Participant object
        """
        participant_id = str(uuid.uuid4())

        participant = Participant(
            id=participant_id,
            name=name,
            type=participant_type,
            metadata=metadata or {},
            joined_at=time.time(),
            last_seen=time.time(),
            is_active=True
        )

        with self._lock:
            self.participants[participant_id] = participant

        # Broadcast join event
        self._emit_event(
            event_type=EventType.JOIN,
            participant_id=participant_id,
            data={"name": name, "type": participant_type.value},
            priority=Priority.NORMAL
        )

        return participant

    def remove_participant(self, participant_id: str):
        """Remove a participant from the collaboration"""

        with self._lock:
            if participant_id in self.participants:
                self.participants[participant_id].is_active = False

        # Release any locked resources
        self._release_all_locks(participant_id)

        # Broadcast leave event
        self._emit_event(
            event_type=EventType.LEAVE,
            participant_id=participant_id,
            data={},
            priority=Priority.NORMAL
        )

    def send_message(
        self,
        sender_id: str,
        content: str,
        recipient_id: Optional[str] = None,
        priority: Priority = Priority.NORMAL,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Send a message in the collaboration

        Args:
            sender_id: Who is sending
            content: Message content
            recipient_id: Specific recipient (None = broadcast)
            priority: Message priority
            metadata: Additional data
        """

        # Update last seen
        self._update_heartbeat(sender_id)

        # Create message event
        self._emit_event(
            event_type=EventType.MESSAGE,
            participant_id=sender_id,
            data={
                "content": content,
                "recipient_id": recipient_id,
                "metadata": metadata or {}
            },
            priority=priority
        )

    def update_shared_state(
        self,
        participant_id: str,
        key: str,
        value: Any,
        merge: bool = False
    ):
        """
        Update the shared state

        Args:
            participant_id: Who is updating
            key: State key
            value: New value
            merge: If True and value is dict, merge with existing
        """

        self._update_heartbeat(participant_id)

        with self._lock:
            if merge and isinstance(value, dict) and isinstance(self.shared_state.get(key), dict):
                self.shared_state[key].update(value)
            else:
                self.shared_state[key] = value

        # Broadcast state update
        self._emit_event(
            event_type=EventType.STATE_UPDATE,
            participant_id=participant_id,
            data={"key": key, "value": value, "merge": merge},
            priority=Priority.NORMAL
        )

    def get_shared_state(self, key: Optional[str] = None) -> Any:
        """Get shared state (specific key or all)"""

        with self._lock:
            if key:
                return self.shared_state.get(key)
            return self.shared_state.copy()

    def create_resource(
        self,
        name: str,
        owner_id: str,
        initial_data: Any = None
    ) -> SharedResource:
        """
        Create a shared resource that can be locked

        Args:
            name: Resource name
            owner_id: Creator
            initial_data: Initial data

        Returns:
            SharedResource
        """

        resource_id = str(uuid.uuid4())

        resource = SharedResource(
            id=resource_id,
            name=name,
            owner_id=owner_id,
            locked_by=None,
            locked_at=None,
            version=1,
            data=initial_data
        )

        with self._lock:
            self.resources[resource_id] = resource

        return resource

    def lock_resource(
        self,
        resource_id: str,
        participant_id: str,
        timeout: float = 300.0
    ) -> bool:
        """
        Lock a resource for editing

        Args:
            resource_id: Resource to lock
            participant_id: Who wants to lock it
            timeout: Auto-unlock after this many seconds

        Returns:
            True if locked successfully, False if already locked
        """

        with self._lock:
            resource = self.resources.get(resource_id)

            if not resource:
                return False

            # Check if already locked
            if resource.locked_by:
                # Check if lock expired
                if time.time() - resource.locked_at > timeout:
                    # Lock expired, release it
                    resource.locked_by = None
                else:
                    # Still locked by someone else
                    return False

            # Lock it
            resource.locked_by = participant_id
            resource.locked_at = time.time()

        # Broadcast lock event
        self._emit_event(
            event_type=EventType.LOCK,
            participant_id=participant_id,
            data={"resource_id": resource_id},
            priority=Priority.HIGH
        )

        return True

    def unlock_resource(self, resource_id: str, participant_id: str) -> bool:
        """
        Unlock a resource

        Args:
            resource_id: Resource to unlock
            participant_id: Who is unlocking (must be lock holder)

        Returns:
            True if unlocked, False if not locked by this participant
        """

        with self._lock:
            resource = self.resources.get(resource_id)

            if not resource:
                return False

            if resource.locked_by != participant_id:
                return False

            resource.locked_by = None
            resource.locked_at = None

        # Broadcast unlock event
        self._emit_event(
            event_type=EventType.UNLOCK,
            participant_id=participant_id,
            data={"resource_id": resource_id},
            priority=Priority.NORMAL
        )

        return True

    def edit_resource(
        self,
        resource_id: str,
        participant_id: str,
        new_data: Any,
        version: Optional[int] = None
    ) -> bool:
        """
        Edit a resource (must be locked first)

        Args:
            resource_id: Resource to edit
            participant_id: Who is editing
            new_data: New data
            version: Expected version (for optimistic locking)

        Returns:
            True if edit succeeded, False if not locked or version mismatch
        """

        with self._lock:
            resource = self.resources.get(resource_id)

            if not resource:
                return False

            # Check lock
            if resource.locked_by != participant_id:
                return False

            # Check version if specified
            if version is not None and resource.version != version:
                return False

            # Update resource
            resource.data = new_data
            resource.version += 1

        # Broadcast edit event
        self._emit_event(
            event_type=EventType.EDIT,
            participant_id=participant_id,
            data={
                "resource_id": resource_id,
                "version": resource.version,
                "data": new_data
            },
            priority=Priority.HIGH
        )

        return True

    def get_active_participants(self) -> List[Participant]:
        """Get all active participants"""

        with self._lock:
            return [p for p in self.participants.values() if p.is_active]

    def get_participant_status(self, participant_id: str) -> Dict[str, Any]:
        """Get detailed status of a participant"""

        with self._lock:
            participant = self.participants.get(participant_id)

            if not participant:
                return {"status": "not_found"}

            # Check if participant is still active (heartbeat within last 60 seconds)
            time_since_seen = time.time() - participant.last_seen
            is_online = time_since_seen < 60

            # Count locked resources
            locked_resources = [
                r for r in self.resources.values()
                if r.locked_by == participant_id
            ]

            return {
                "status": "online" if is_online else "offline",
                "name": participant.name,
                "type": participant.type.value,
                "joined_at": participant.joined_at,
                "last_seen": participant.last_seen,
                "time_since_seen": time_since_seen,
                "locked_resources": len(locked_resources),
                "metadata": participant.metadata
            }

    def on_event(self, event_type: EventType, handler: Callable):
        """
        Register an event handler

        Args:
            event_type: Type of event to listen for
            handler: Function to call when event occurs
        """

        self.event_handlers[event_type].append(handler)

    def get_recent_events(
        self,
        limit: int = 50,
        event_type: Optional[EventType] = None,
        participant_id: Optional[str] = None
    ) -> List[CollaborationEvent]:
        """
        Get recent events with optional filtering

        Args:
            limit: Maximum number of events
            event_type: Filter by event type
            participant_id: Filter by participant

        Returns:
            List of events
        """

        with self._lock:
            events = self.events.copy()

        # Filter
        if event_type:
            events = [e for e in events if e.event_type == event_type]

        if participant_id:
            events = [e for e in events if e.participant_id == participant_id]

        # Sort by timestamp (newest first)
        events.sort(key=lambda e: e.timestamp, reverse=True)

        return events[:limit]

    def generate_activity_report(self) -> str:
        """Generate human-readable activity report"""

        report = "=" * 60 + "\n"
        report += "REAL-TIME COLLABORATION HUB - ACTIVITY REPORT\n"
        report += "=" * 60 + "\n\n"

        report += f"Hub ID: {self.hub_id}\n"
        report += f"Total Events: {len(self.events)}\n\n"

        # Participants
        active = self.get_active_participants()
        report += f"ACTIVE PARTICIPANTS: {len(active)}\n"
        for p in active:
            status = self.get_participant_status(p.id)
            report += f"  - {p.name} ({p.type.value}): {status['status']}\n"
        report += "\n"

        # Shared state
        report += "SHARED STATE:\n"
        if self.shared_state:
            for key, value in self.shared_state.items():
                value_str = str(value)[:50]
                report += f"  - {key}: {value_str}\n"
        else:
            report += "  (empty)\n"
        report += "\n"

        # Resources
        report += f"SHARED RESOURCES: {len(self.resources)}\n"
        for resource in self.resources.values():
            lock_status = f"locked by {resource.locked_by}" if resource.locked_by else "unlocked"
            report += f"  - {resource.name} (v{resource.version}): {lock_status}\n"
        report += "\n"

        # Recent activity
        report += "RECENT EVENTS (last 10):\n"
        recent = self.get_recent_events(limit=10)
        for event in recent:
            participant = self.participants.get(event.participant_id)
            name = participant.name if participant else "unknown"
            report += f"  - [{event.event_type.value}] {name}: "

            if event.event_type == EventType.MESSAGE:
                report += event.data.get('content', '')[:40]
            elif event.event_type == EventType.STATE_UPDATE:
                report += f"updated {event.data.get('key')}"
            elif event.event_type == EventType.EDIT:
                report += f"edited resource {event.data.get('resource_id')[:8]}"
            else:
                report += str(event.data)[:40]

            report += "\n"

        report += "\n" + "=" * 60 + "\n"

        return report

    def _emit_event(
        self,
        event_type: EventType,
        participant_id: str,
        data: Dict[str, Any],
        priority: Priority
    ):
        """Internal: Emit an event"""

        event = CollaborationEvent(
            id=str(uuid.uuid4()),
            timestamp=time.time(),
            event_type=event_type,
            participant_id=participant_id,
            data=data,
            priority=priority
        )

        with self._lock:
            self.events.append(event)

        # Call handlers
        for handler in self.event_handlers.get(event_type, []):
            try:
                handler(event)
            except Exception as e:
                print(f"Error in event handler: {e}")

    def _update_heartbeat(self, participant_id: str):
        """Update participant's last seen time"""

        with self._lock:
            if participant_id in self.participants:
                self.participants[participant_id].last_seen = time.time()

    def _release_all_locks(self, participant_id: str):
        """Release all locks held by a participant"""

        with self._lock:
            for resource in self.resources.values():
                if resource.locked_by == participant_id:
                    resource.locked_by = None
                    resource.locked_at = None


def demo():
    """Demonstrate the real-time collaboration hub"""

    print("=" * 60)
    print("REAL-TIME COLLABORATION HUB - DEMO")
    print("=" * 60)
    print()

    # Create hub
    hub = RealtimeCollaborationHub(hub_id="demo_hub")

    # Add participants
    print("Adding participants...")
    alice = hub.add_participant("Alice (Human)", ParticipantType.HUMAN, {"role": "developer"})
    instance_1 = hub.add_participant("Instance 1", ParticipantType.AI_INSTANCE, {"computer": "C1"})
    instance_2 = hub.add_participant("Instance 2", ParticipantType.AI_INSTANCE, {"computer": "C1"})
    print(f"  - {alice.name}")
    print(f"  - {instance_1.name}")
    print(f"  - {instance_2.name}")
    print()

    # Send messages
    print("Exchanging messages...")
    hub.send_message(alice.id, "Hello team! Let's build something great.", priority=Priority.NORMAL)
    hub.send_message(instance_1.id, "Ready to collaborate!", priority=Priority.NORMAL)
    hub.send_message(instance_2.id, "Let's sync our work.", priority=Priority.NORMAL)
    print()

    # Update shared state
    print("Updating shared state...")
    hub.update_shared_state(alice.id, "project_status", "in_progress")
    hub.update_shared_state(instance_1.id, "tasks_completed", 5)
    hub.update_shared_state(instance_2.id, "tasks_completed", 3, merge=False)
    print()

    # Create and lock resource
    print("Creating shared resource...")
    code_file = hub.create_resource("main.py", alice.id, "# Initial code")
    print(f"  Created: {code_file.name}")
    print()

    print("Alice locks the resource for editing...")
    locked = hub.lock_resource(code_file.id, alice.id)
    print(f"  Lock successful: {locked}")
    print()

    print("Instance 1 tries to lock (should fail)...")
    locked2 = hub.lock_resource(code_file.id, instance_1.id)
    print(f"  Lock successful: {locked2}")
    print()

    print("Alice edits the resource...")
    hub.edit_resource(code_file.id, alice.id, "# Updated code\nprint('Hello')")
    print()

    print("Alice unlocks the resource...")
    hub.unlock_resource(code_file.id, alice.id)
    print()

    # Generate report
    print(hub.generate_activity_report())

    # Show participant statuses
    print("PARTICIPANT STATUSES:")
    for participant_id in [alice.id, instance_1.id, instance_2.id]:
        status = hub.get_participant_status(participant_id)
        print(f"{status['name']}: {status['status']} (last seen {status['time_since_seen']:.1f}s ago)")
    print()

    print("=" * 60)
    print("Demo complete. Collaboration hub operational!")
    print("=" * 60)


if __name__ == "__main__":
    demo()
