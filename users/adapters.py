import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Q
from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.models import EmailAddress
from allauth.account.utils import send_email_confirmation
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


logger = logging.getLogger(__name__)


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

    def pre_social_login(self, request, sociallogin):
        """
        Invoked just after a user successfully authenticates via a
        social provider, but before the login is actually processed
        (and before the pre_social_login signal is emitted).

        We're trying to solve different use cases:
        - social account already exists, just go on
        - social account's email exists, link social account to existing user
        """

        # social account already exists, so this is just a login
        if sociallogin.is_existing:
            logger.info(
                "SocialAccount for User %s exists. Logging in.", sociallogin.user
            )
            return

        # extract username and domain
        email = sociallogin.account.extra_data["email"]
        username, domain = email.split("@")

        # TODO validate valid email domains
        # create table instead of local variable VALID_DOMAINS
        # It is possible to lock to internal users only at SocialApp level

        # if domain not in VALID_DOMAINS:
        #     message = "Invalid account: %s" % sociallogin.user.email
        #     messages.error(request, message)
        #     raise ImmediateHttpResponse(HttpResponseRedirect(reverse("account_login")))

        # check if given username already exists
        User = get_user_model()
        try:
            user = User.objects.get(
                Q(username__iexact=username) | Q(email__iexact=email)
            )
        except User.DoesNotExist:
            # proceed with sign up as usual
            logger.info("User %s <%s> not found. Signing up.", username, email)
            return
        else:
            logger.info("Associating User %s to EmailAddress %s", user, email)

            EmailAddress.objects.get_or_create(
                user=user,
                email=email,
                verified=sociallogin.account.extra_data["verified_email"],
                primary=True,
            )

            # connect this new social login to the existing user
            sociallogin.connect(request, user)
