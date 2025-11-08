"""MODULE #51: MESSAGE BROKER - Pub/Sub messaging for 6 AI instances"""
import time
import threading
import json
from typing import Dict, List, Callable, Any, Optional
from dataclasses import dataclass, field
from collections import defaultdict
from enum import Enum
import queue

class MessagePriority(Enum):
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class Message:
    id: str
    topic: str
    payload: Any
    priority: MessagePriority
    timestamp: float = field(default_factory=time.time)
    sender_id: Optional[str] = None
    ttl: Optional[float] = None  # Time to live in seconds
    headers: Dict[str, Any] = field(default_factory=dict)

    def is_expired(self) -> bool:
        if self.ttl is None:
            return False
        return (time.time() - self.timestamp) > self.ttl

class MessageBroker:
    """High-performance pub/sub message broker for distributed AI instances"""

    def __init__(self, broker_id: str):
        self.broker_id = broker_id

        # Subscriptions: topic -> list of callback functions
        self.subscriptions: Dict[str, List[Callable]] = defaultdict(list)

        # Message queues per topic
        self.queues: Dict[str, queue.PriorityQueue] = defaultdict(queue.PriorityQueue)

        # Message history
        self.message_history: List[Message] = []
        self.max_history = 1000

        # Thread safety
        self.lock = threading.RLock()

        # Worker threads
        self.workers: Dict[str, threading.Thread] = {}
        self.running = False

        # Metrics
        self.metrics = {
            'messages_published': 0,
            'messages_delivered': 0,
            'messages_dropped': 0,
            'active_topics': 0,
            'total_subscribers': 0
        }

    def publish(self, topic: str, payload: Any, priority: MessagePriority = MessagePriority.NORMAL,
               sender_id: Optional[str] = None, ttl: Optional[float] = None,
               headers: Dict[str, Any] = None) -> str:
        """Publish message to topic"""
        msg_id = f"{self.broker_id}-{self.metrics['messages_published']}-{time.time()}"

        msg = Message(
            id=msg_id,
            topic=topic,
            payload=payload,
            priority=priority,
            sender_id=sender_id,
            ttl=ttl,
            headers=headers or {}
        )

        with self.lock:
            # Add to queue (lower number = higher priority)
            priority_value = 5 - priority.value
            self.queues[topic].put((priority_value, msg))

            # Add to history
            self.message_history.append(msg)
            if len(self.message_history) > self.max_history:
                self.message_history.pop(0)

            self.metrics['messages_published'] += 1
            self.metrics['active_topics'] = len(self.queues)

            # Start worker for topic if not running
            if topic not in self.workers and self.running:
                self._start_worker(topic)

        return msg_id

    def subscribe(self, topic: str, callback: Callable[[Message], None]):
        """Subscribe to topic with callback"""
        with self.lock:
            self.subscriptions[topic].append(callback)
            self.metrics['total_subscribers'] = sum(len(subs) for subs in self.subscriptions.values())

            # Start worker if not exists
            if self.running and topic not in self.workers:
                self._start_worker(topic)

    def unsubscribe(self, topic: str, callback: Callable):
        """Unsubscribe callback from topic"""
        with self.lock:
            if topic in self.subscriptions and callback in self.subscriptions[topic]:
                self.subscriptions[topic].remove(callback)
                self.metrics['total_subscribers'] = sum(len(subs) for subs in self.subscriptions.values())

    def _start_worker(self, topic: str):
        """Start worker thread for topic"""
        if topic in self.workers:
            return

        worker = threading.Thread(target=self._process_topic, args=(topic,), daemon=True)
        self.workers[topic] = worker
        worker.start()

    def _process_topic(self, topic: str):
        """Process messages for a topic"""
        while self.running:
            try:
                # Get message with timeout
                priority, msg = self.queues[topic].get(timeout=0.1)

                # Check if expired
                if msg.is_expired():
                    self.metrics['messages_dropped'] += 1
                    continue

                # Deliver to all subscribers
                with self.lock:
                    subscribers = self.subscriptions.get(topic, [])

                for callback in subscribers:
                    try:
                        callback(msg)
                        self.metrics['messages_delivered'] += 1
                    except Exception as e:
                        print(f"Error in subscriber callback: {e}")

            except queue.Empty:
                continue
            except Exception as e:
                print(f"Worker error for topic {topic}: {e}")

    def start(self):
        """Start broker workers"""
        self.running = True

        # Start workers for existing topics
        with self.lock:
            for topic in self.queues.keys():
                self._start_worker(topic)

    def stop(self):
        """Stop broker workers"""
        self.running = False

        # Wait for workers to finish
        for worker in self.workers.values():
            worker.join(timeout=1.0)

    def get_topics(self) -> List[str]:
        """Get all active topics"""
        return list(self.queues.keys())

    def get_message_history(self, topic: Optional[str] = None, limit: int = 100) -> List[Message]:
        """Get message history, optionally filtered by topic"""
        with self.lock:
            if topic:
                messages = [msg for msg in self.message_history if msg.topic == topic]
            else:
                messages = self.message_history

            return messages[-limit:]

    def get_metrics(self) -> Dict[str, Any]:
        """Get broker metrics"""
        with self.lock:
            return {
                **self.metrics,
                'queue_depths': {topic: q.qsize() for topic, q in self.queues.items()}
            }


if __name__ == "__main__":
    print("📨 MODULE #51: MESSAGE BROKER")
    print("=" * 60)

    # Create broker
    broker = MessageBroker("broker-1")
    broker.start()

    print("✅ Message broker started")

    # Create subscribers for different instances
    received_messages = defaultdict(list)

    def instance_handler(instance_id: int):
        def handler(msg: Message):
            received_messages[instance_id].append(msg)
            print(f"   Instance {instance_id} received: {msg.payload}")
        return handler

    # Subscribe instances to topics
    broker.subscribe("ai.coordination", instance_handler(1))
    broker.subscribe("ai.coordination", instance_handler(2))
    broker.subscribe("ai.status", instance_handler(3))
    broker.subscribe("ai.alerts", instance_handler(4))

    print(f"✅ Subscribed 4 instances to topics")

    # Publish messages
    print("\n📤 Publishing messages...")

    broker.publish("ai.coordination", {"action": "sync", "data": [1,2,3]},
                  priority=MessagePriority.HIGH, sender_id="instance-1")

    broker.publish("ai.status", {"status": "healthy", "cpu": 45},
                  priority=MessagePriority.NORMAL, sender_id="instance-3")

    broker.publish("ai.alerts", {"level": "warning", "msg": "High memory usage"},
                  priority=MessagePriority.CRITICAL, sender_id="instance-5")

    broker.publish("ai.coordination", {"action": "update", "version": 2},
                  priority=MessagePriority.LOW, sender_id="instance-2")

    # Wait for processing
    time.sleep(0.5)

    # Show results
    print(f"\n📊 Messages Received:")
    for inst_id, messages in received_messages.items():
        print(f"   Instance {inst_id}: {len(messages)} messages")

    # Show metrics
    metrics = broker.get_metrics()
    print(f"\n📈 Broker Metrics:")
    print(f"   Published: {metrics['messages_published']}")
    print(f"   Delivered: {metrics['messages_delivered']}")
    print(f"   Active topics: {metrics['active_topics']}")
    print(f"   Subscribers: {metrics['total_subscribers']}")

    # Stop broker
    broker.stop()

    print("\n✅ Message Broker operational!")
    print("🚀 Ready for distributed messaging across 6 instances!")
