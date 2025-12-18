from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.shortcuts import redirect
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Handles pre-signup logic for social logins
    """

    def pre_social_login(self, request, sociallogin):
        email = sociallogin.user.email

        if not email:
            return
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return
        
        if not sociallogin.is_existing:
            sociallogin.connect(request, user)
            raise ImmediateHttpResponse(redirect("/"))