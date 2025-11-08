# MODULE #38: WEBSOCKET SERVER
Real-time bidirectional communication with rooms and broadcasting.
```python
from websocket import WebSocketServer
ws = WebSocketServer()
ws.on("message", lambda data: {"status": "ok"})
await ws.broadcast({"event": "update"})
```
**#38 COMPLETE** ✅
