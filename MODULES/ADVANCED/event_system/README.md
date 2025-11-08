# MODULE #36: EVENT SYSTEM
Pub/Sub event handling. Subscribe to events, emit events, track history.
```python
from events import EventSystem
events = EventSystem()
events.on("user_action", lambda e: print(e.data))
events.emit("user_action", {"action": "click"})
```
**#36 COMPLETE** ✅
