# MODULE #51: MESSAGE BROKER

High-performance pub/sub message broker for distributed communication between 6 AI instances.

## Features
- Topic-based publish/subscribe
- Priority messaging (LOW, NORMAL, HIGH, CRITICAL)
- Message TTL (time-to-live)
- Multi-subscriber support
- Message history
- Thread-safe operations

## Usage

```python
from message_broker import MessageBroker, MessagePriority

broker = MessageBroker("broker-1")
broker.start()

# Subscribe
def on_message(msg):
    print(f"Received: {msg.payload}")

broker.subscribe("ai.coordination", on_message)

# Publish
broker.publish("ai.coordination", {"action": "sync"},
               priority=MessagePriority.HIGH)
```

**#51 COMPLETE** ✅
