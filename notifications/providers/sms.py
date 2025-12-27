from .base import NotificationProvider


class SMSProvider(NotificationProvider):
    def send(self, payload):
        print('Sending SMS:', payload.body)