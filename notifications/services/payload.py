from dataclasses import dataclass

@dataclass
class NotificationPayload:
    user_id: int
    channel: str
    subject: str
    body: str
    metadata: dict

    