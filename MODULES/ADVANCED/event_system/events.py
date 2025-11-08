"""MODULE #36: EVENT SYSTEM - Pub/Sub event handling"""
from typing import Callable, Dict, List
from dataclasses import dataclass
import time

@dataclass
class Event:
    name: str
    data: dict
    timestamp: float

class EventSystem:
    def __init__(self):
        self.handlers: Dict[str, List[Callable]] = {}
        self.history: List[Event] = []

    def on(self, event_name: str, handler: Callable):
        """Subscribe to event"""
        if event_name not in self.handlers:
            self.handlers[event_name] = []
        self.handlers[event_name].append(handler)

    def emit(self, event_name: str, data: dict = None):
        """Emit event"""
        event = Event(event_name, data or {}, time.time())
        self.history.append(event)

        if event_name in self.handlers:
            for handler in self.handlers[event_name]:
                handler(event)

    def off(self, event_name: str, handler: Callable = None):
        """Unsubscribe"""
        if event_name in self.handlers:
            if handler:
                self.handlers[event_name].remove(handler)
            else:
                del self.handlers[event_name]

if __name__ == "__main__":
    events = EventSystem()
    events.on("user_login", lambda e: print(f"User logged in: {e.data}"))
    events.emit("user_login", {"user": "alice"})
    print(f"Events: {len(events.history)}")
