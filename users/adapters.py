from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)


class SocialAccountAdapter(DefaultSocialAccountAdapter):

    def is_open_for_signup(self, request, sociallogin):
            return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        user.name = " ".join((user.first_name, user.last_name))
        return user
