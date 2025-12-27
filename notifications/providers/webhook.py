import requests, hmac, hashlib
from .base import NotificationProvider


class WebhookProvider(NotificationProvider):
    def send(self, payload):
        secret = payload.metadata["secret"]
        signature = hmac.new(
            secret.encode(),
            payload.body.encode(),
            hashlib.sha256
        ).hexdigest()

        requests.post(
            payload.metadata["url"],
            json=payload.metadata,
            headers={"X-Signature": signature},
            timeout=5
        )