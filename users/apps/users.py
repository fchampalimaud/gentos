from confapp import conf
from django.contrib.auth import get_user_model
from pyforms_web.organizers import no_columns
from pyforms_web.widgets.django import ModelAdminWidget
from pyforms_web.widgets.django import ModelFormWidget

from users.models import Membership

User = get_user_model()


class MembershipInlineForm(ModelFormWidget):
    FIELDSETS = [no_columns("group", "is_responsible", "is_manager")]


class MembershipInline(ModelAdminWidget):
    MODEL = Membership

    EDITFORM_CLASS = MembershipInlineForm

    LIST_DISPLAY = ["group", "is_responsible", "is_manager"]


class UserForm(ModelFormWidget):
    FIELDSETS = [
        ("name", "email", "display_name"),
        " ",
        "is_active",
        "is_staff",
        "is_superuser",
        " ",
        "MembershipInline",
        ("last_login", "date_joined"),
    ]

    READ_ONLY = ["username", "email"]

    INLINES = [MembershipInline]

    LAYOUT_POSITION = conf.ORQUESTRA_NEW_TAB

    @property
    def title(self):
        try:
            return self.model_object.get_display_name()
        except AttributeError:
            pass  # apparently it defaults to App TITLE


class UsersListApp(ModelAdminWidget):

    UID = "users"
    MODEL = User
    TITLE = "Users"

    EDITFORM_CLASS = UserForm

    LIST_DISPLAY = ["name", "email", "get_group", "is_active"]

    LIST_FILTER = [
        "memberships__group",
        "memberships__group__accesses__animaldb",
        "is_active",
    ]

    SEARCH_FIELDS = ["name__icontains", "email__icontains"]

    USE_DETAILS_TO_EDIT = False  # required to have form in NEW_TAB

    LAYOUT_POSITION = conf.ORQUESTRA_HOME
    ORQUESTRA_MENU = "middle-left"
    ORQUESTRA_MENU_ORDER = 10
    ORQUESTRA_MENU_ICON = "users"

    @classmethod
    def has_permissions(cls, user):
        if user.is_superuser or user.is_facility_staff():
            return True
        return False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._list.headers = ["Name", "Email Address", "Group", "Active"]
        self._list.custom_filter_labels = {"is_active": "Active"}

    def get_queryset(self, request, queryset):
        user = request.user

        if user.is_superuser:
            return queryset
        else:
            queryset = self.model.db_users.all()

            facility_users = queryset.none()

            if user.is_admin("fishdb"):
                facility_users |= queryset.fishdb_users()

            if user.is_admin("flydb"):
                facility_users |= queryset.flydb_users()

            if user.is_admin("rodentdb"):
                facility_users |= queryset.rodentdb_users()

            return facility_users.distinct()

    def has_add_permissions(self):
        return False

    def has_remove_permissions(self, obj):
        return False
