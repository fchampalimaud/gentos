from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.models import EmailAddress
from allauth.account.utils import send_email_confirmation
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def new_user(self, request):
        """All accounts but superusers are inactivated upon creation."""
        user = super().new_user(request)
        user.is_active = False
        return user

    def respond_user_inactive(self, request, user):
        """Method overridden to resend email confirmation if needed."""
        response = super().respond_user_inactive(request, user)
        primary_email = EmailAddress.objects.get_primary(user=user)
        if not primary_email.verified:
            send_email_confirmation(request, user)
        return response


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        user.name = " ".join((user.first_name, user.last_name))
        return user
