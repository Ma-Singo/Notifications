from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from allauth.account.signals import (
    user_signed_up as allauth_user_signed_up,
    password_reset as allauth_password_reset,
    password_changed as allauth_password_changed,
    email_changed as allauth_email_changed,
    email_confirmed as allauth_email_confirmed,
    email_removed as allauth_email_removed,
    
)

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