from django import forms
from django.utils.translation import ugettext_lazy as _

from allauth.account.forms import SignupForm


class SignupForm(SignupForm):
    name = forms.CharField(
        max_length=150,
        label=_("Full Name"),
        required=True,
        widget=forms.TextInput(attrs={"placeholder": _("Full Name")}),
    )

    def custom_signup(self, request, user):
        user.name = self.cleaned_data["name"]
        user.save()
        return user
