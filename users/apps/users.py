from confapp import conf
from django.contrib.auth import get_user_model
from pyforms_web.widgets.django import ModelAdminWidget
from pyforms_web.widgets.django import ModelFormWidget

from users.models import Membership

User = get_user_model()


class MembershipInline(ModelAdminWidget):
    MODEL = Membership

    LIST_DISPLAY = ["group", "is_manager"]


class UserForm(ModelFormWidget):
    FIELDSETS = [
        ("username", "email"),
        ("first_name", "last_name"),
        " ",
        "is_active",
        " ",
        "MembershipInline",
    ]

    READ_ONLY = ["username", "email"]

    INLINES = [MembershipInline]

    LAYOUT_POSITION = conf.ORQUESTRA_NEW_TAB

    @property
    def title(self):
        try:
            return self.model_object.get_full_name()
        except AttributeError:
            pass  # apparently it defaults to App TITLE


class UsersListApp(ModelAdminWidget):

    UID = "users"
    MODEL = User
    TITLE = "Users"

    AUTHORIZED_GROUPS = ['superuser']

    EDITFORM_CLASS = UserForm

    LIST_DISPLAY = ['get_full_name', 'email', 'is_active', 'is_staff', 'is_superuser']

    USE_DETAILS_TO_EDIT = False  # required to have form in NEW_TAB

    LAYOUT_POSITION = conf.ORQUESTRA_HOME
    ORQUESTRA_MENU = "middle-left"
    ORQUESTRA_MENU_ORDER = 10
    ORQUESTRA_MENU_ICON = "users"

    def get_queryset(self, request, queryset):
        print(queryset)

        user = request.user

        if user.is_superuser:
            pass

        for user in queryset:
            print(user)
            print(user.__dict__)
            print(user.groups.all())
            print(user.memberships.all())

        return queryset
