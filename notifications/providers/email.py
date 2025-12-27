from django.core.mail import send_mail
from .base import NotificationProvider


class EmailProvider(NotificationProvider):
    def send(self, payload):
        send_mail(
            payload.subject,
            payload.body,
            None,
            [payload.metadata["email"]],
        )