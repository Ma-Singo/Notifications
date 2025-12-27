from notifications.providers.email import EmailProvider
from notifications.providers.sms import SMSProvider
from notifications.providers.webhook import WebhookProvider

class ProviderFactory:
    MAP = {
        'email': EmailProvider,
        'sms': SMSProvider, 
        'webhook': WebhookProvider
    }

    @classmethod
    def get(cls, channel):
        return cls.MAP[channel]()