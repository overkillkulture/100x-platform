"""
MODULE #34: MESSAGE QUEUE
Built: 2025-11-08
Async message queue for decoupled systems.
"""

import time
from typing import Any, Optional, List, Callable
from collections import deque
from dataclasses import dataclass


@dataclass
class Message:
    """Queue message"""
    id: str
    data: Any
    priority: int
    timestamp: float
    attempts: int = 0


class MessageQueue:
    """Priority message queue with retry"""

    def __init__(self, name: str):
        self.name = name
        self.queue = deque()
        self.processing = {}
        self.handlers: List[Callable] = []
        self.stats = {'sent': 0, 'processed': 0, 'failed': 0}

    def send(self, data: Any, priority: int = 5):
        """Send message to queue"""
        msg = Message(
            id=f"{self.name}_{self.stats['sent']}",
            data=data,
            priority=priority,
            timestamp=time.time()
        )
        self.queue.append(msg)
        self.stats['sent'] += 1

    def receive(self, timeout: float = 1.0) -> Optional[Message]:
        """Receive message from queue"""
        if not self.queue:
            return None

        # Sort by priority
        msgs = sorted(self.queue, key=lambda m: m.priority, reverse=True)
        msg = msgs[0]
        self.queue.remove(msg)

        self.processing[msg.id] = msg
        return msg

    def ack(self, msg_id: str):
        """Acknowledge processed message"""
        if msg_id in self.processing:
            del self.processing[msg_id]
            self.stats['processed'] += 1

    def nack(self, msg_id: str, retry: bool = True):
        """Negative acknowledge (failed)"""
        if msg_id in self.processing:
            msg = self.processing[msg_id]
            del self.processing[msg_id]

            if retry and msg.attempts < 3:
                msg.attempts += 1
                self.queue.append(msg)
            else:
                self.stats['failed'] += 1

    def subscribe(self, handler: Callable):
        """Subscribe handler to queue"""
        self.handlers.append(handler)

    def process_all(self):
        """Process all messages"""
        while self.queue:
            msg = self.receive()
            if not msg:
                break

            try:
                for handler in self.handlers:
                    handler(msg.data)
                self.ack(msg.id)
            except Exception as e:
                print(f"Handler error: {e}")
                self.nack(msg.id, retry=True)


# Demo
if __name__ == "__main__":
    queue = MessageQueue("demo")

    # Send messages
    queue.send({"task": "process_data"}, priority=10)
    queue.send({"task": "send_email"}, priority=5)

    # Subscribe handler
    def handler(data):
        print(f"Processing: {data}")

    queue.subscribe(handler)

    # Process
    queue.process_all()

    print(f"Stats: {queue.stats}")
