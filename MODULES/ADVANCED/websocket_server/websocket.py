"""MODULE #38: WEBSOCKET SERVER - Real-time bidirectional communication"""
import asyncio
import json
from typing import Set, Dict, Callable

class WebSocketServer:
    def __init__(self):
        self.clients: Set = set()
        self.handlers: Dict[str, Callable] = {}
        self.rooms: Dict[str, Set] = {}

    def on(self, event_type: str, handler: Callable):
        """Register message handler"""
        self.handlers[event_type] = handler

    async def handle_client(self, websocket):
        """Handle client connection"""
        self.clients.add(websocket)
        try:
            async for message in websocket:
                data = json.loads(message)
                event_type = data.get('type')

                if event_type in self.handlers:
                    response = self.handlers[event_type](data.get('payload'))
                    await websocket.send(json.dumps(response))
        finally:
            self.clients.remove(websocket)

    async def broadcast(self, message: dict):
        """Broadcast to all clients"""
        if self.clients:
            await asyncio.gather(
                *[client.send(json.dumps(message)) for client in self.clients]
            )

    def join_room(self, websocket, room: str):
        """Join client to room"""
        if room not in self.rooms:
            self.rooms[room] = set()
        self.rooms[room].add(websocket)

    async def broadcast_room(self, room: str, message: dict):
        """Broadcast to room"""
        if room in self.rooms:
            await asyncio.gather(
                *[client.send(json.dumps(message)) for client in self.rooms[room]]
            )

# Demo usage (requires websockets library)
if __name__ == "__main__":
    print("WebSocket Server - requires 'websockets' library")
    print("Install: pip install websockets")
    print("Usage: ws_server = WebSocketServer()")
