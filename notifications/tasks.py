from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from core.models import IdempotencyKey
from core.idempotency import IdempotencyLock
from notifications.services.dispatcher import ProviderFactory


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={'max_retries': 5}
)
def send_welcome_email(self, user_id, idempotency_key):
    lock = IdempotencyLock(idempotency_key)

    # Acquire Redis lock
    if not lock.acquire():
        return "Duplicate task ignored (lock)"
    
    try:
        obj, created = IdempotencyKey.objects.get_or_create(
            key=idempotency_key,
            defaults={"task_name": self.name}
        )

        if not created and obj.status == "SUCCESS":
            return "Already processed"
        

        send_mail(
            subject="Welcome to Notif!",
            message="Thanking you for joining Notif",
            from_email=None,
            recipient_list=['singoekwe@gmail.com']
        )

        obj.status = "SUCCESS"
        obj.completed_at = timezone.now()
        obj.save()

        return "Email sent"

    except Exception as e:
        obj.status = "FAILED"
        obj.save()
        raise e
    finally:
        lock.release()


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={'max_retries': 5}
)
def send_notification_task(payload):
    provider = ProviderFactory.get(payload["channel"])
    provider.send(payload)