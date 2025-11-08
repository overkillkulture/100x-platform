"""MODULE #45: NOTIFICATION SYSTEM - Multi-channel notifications"""
import time
from typing import List, Dict, Callable
from dataclasses import dataclass
from enum import Enum

class NotificationPriority(Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"

class NotificationChannel(Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    WEBHOOK = "webhook"
    IN_APP = "in_app"

@dataclass
class Notification:
    id: str
    title: str
    message: str
    priority: NotificationPriority
    channels: List[NotificationChannel]
    recipient: str
    timestamp: float
    sent: bool = False

class NotificationSystem:
    def __init__(self):
        self.notifications: List[Notification] = []
        self.handlers: Dict[NotificationChannel, Callable] = {}
        self.queue: List[Notification] = []

    def register_handler(self, channel: NotificationChannel, handler: Callable):
        """Register notification handler"""
        self.handlers[channel] = handler

    def send(self, title: str, message: str, recipient: str,
             priority: NotificationPriority = NotificationPriority.NORMAL,
             channels: List[NotificationChannel] = None):
        """Send notification"""
        if channels is None:
            channels = [NotificationChannel.IN_APP]

        notif = Notification(
            id=f"notif_{len(self.notifications)}",
            title=title,
            message=message,
            priority=priority,
            channels=channels,
            recipient=recipient,
            timestamp=time.time()
        )

        self.notifications.append(notif)
        self.queue.append(notif)

        return notif.id

    def process_queue(self):
        """Process notification queue"""
        while self.queue:
            notif = self.queue.pop(0)

            for channel in notif.channels:
                if channel in self.handlers:
                    try:
                        self.handlers[channel](notif)
                        notif.sent = True
                    except Exception as e:
                        print(f"Failed to send via {channel}: {e}")

    def get_notifications(self, recipient: str, limit: int = 10) -> List[Notification]:
        """Get notifications for recipient"""
        user_notifs = [n for n in self.notifications if n.recipient == recipient]
        user_notifs.sort(key=lambda x: x.timestamp, reverse=True)
        return user_notifs[:limit]

    def mark_read(self, notification_id: str):
        """Mark notification as read"""
        for notif in self.notifications:
            if notif.id == notification_id:
                notif.sent = True

if __name__ == "__main__":
    notif_system = NotificationSystem()

    # Register simple handler
    def email_handler(notif):
        print(f"📧 Sending email to {notif.recipient}: {notif.title}")

    notif_system.register_handler(NotificationChannel.EMAIL, email_handler)

    # Send notification
    notif_system.send(
        "Welcome!",
        "Thank you for joining the Consciousness Revolution",
        "user@example.com",
        priority=NotificationPriority.HIGH,
        channels=[NotificationChannel.EMAIL]
    )

    notif_system.process_queue()

    print("✅ Notification System working!")
