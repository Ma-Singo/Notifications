from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_login_failed
from django.contrib.auth import get_user_model

from notifications.tasks import send_welcome_email, send_notification_task
from notifications.services.payload import NotificationPayload
from notifications.services.notification_service import NotificationService

from allauth.account.signals import (
    user_signed_up as allauth_user_signed_up,
    password_reset as allauth_password_reset,
    password_changed as allauth_password_changed,
    email_changed as allauth_email_changed,
    email_confirmed as allauth_email_confirmed,
    email_removed as allauth_email_removed,
    
)

User = get_user_model()

from allauth.socialaccount.signals import (
    pre_social_login,
    social_account_added,
    social_account_removed,
    social_account_updated
)

@receiver(allauth_user_signed_up)
def user_signed_up_handler(request, user, *args, **kwargs):
    """
    Triggered when a user successfully signs up
    
    :param request: django request
    :param user: Description
    :param args: Description
    :param kwargs: Description
    """
    
    send_mail(
        subject="Welcome to Notif",
        message=f"Hi {user.email}, your account was successfully created.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email], 
        fail_silently=False
    )

@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    if created:
        key = f"user-created:{instance.id}"
        send_welcome_email(instance.id, key)

@receiver(user_login_failed)
def failed_login(sender, credentials, **kwargs):
    payload = NotificationPayload(
        user_id=None,
        channel="email",
        subject="Failed login attempt",
        body="Someone tried to log into your account.",
        metadata={"email": credentials.get("username")}
    )

    NotificationService.send(None, payload, "failed-login")