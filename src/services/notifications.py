"""
Notification Dispatch Domain Service
Author: Saksham Singh (24BTRAO035)
Handles transactional emails, event logs, and notification delivery queues.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional
import time

from src.utils.validators import validate_email, validate_phone


@dataclass
class NotificationEvent:
    event_id: str
    recipient: str
    channel: str  # "email" or "sms"
    subject: str
    body: str
    status: str = "queued"
    timestamp: float = field(default_factory=time.time)


class NotificationService:
    """Manages transactional messaging with input guards and dispatch histories."""

    def __init__(self):
        self._events: Dict[str, NotificationEvent] = {}

    def send_email(self, recipient_email: str, subject: str, message: str) -> NotificationEvent:
        if not validate_email(recipient_email):
            raise ValueError(f"Invalid email: {recipient_email}")
        if not subject.strip():
            raise ValueError("Email subject cannot be empty")

        event_id = f"evt_mail_{len(self._events) + 1:05d}"
        event = NotificationEvent(
            event_id=event_id,
            recipient=recipient_email.strip(),
            channel="email",
            subject=subject.strip(),
            body=message.strip(),
            status="delivered",
            timestamp=time.time()
        )
        self._events[event_id] = event
        return event

    def send_sms(self, phone_number: str, message: str) -> NotificationEvent:
        if not validate_phone(phone_number):
            raise ValueError(f"Invalid phone number: {phone_number}")
        if len(message) > 160:
            raise ValueError("SMS body exceeds 160 character limit")

        event_id = f"evt_sms_{len(self._events) + 1:05d}"
        event = NotificationEvent(
            event_id=event_id,
            recipient=phone_number.strip(),
            channel="sms",
            subject="SMS_ALERT",
            body=message.strip(),
            status="delivered",
            timestamp=time.time()
        )
        self._events[event_id] = event
        return event

    def get_event(self, event_id: str) -> Optional[NotificationEvent]:
        return self._events.get(event_id)

    def get_user_events(self, recipient: str) -> List[NotificationEvent]:
        return [evt for evt in self._events.values() if evt.recipient.lower() == recipient.lower()]
