from confapp import conf
from django.contrib.auth import get_user_model
from pyforms_web.organizers import segment
from pyforms_web.widgets.django import ModelAdminWidget
from pyforms_web.widgets.django import ModelFormWidget

from .. import models


User = get_user_model()


class MembershipInlineForm(ModelFormWidget):
    FIELDSETS = ["group", "is_responsible", "is_manager"]

    LAYOUT_POSITION = conf.ORQUESTRA_NEW_WINDOW

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.is_manager.checkbox_type = ""
        self.is_responsible.checkbox_type = ""

        self.is_manager.label_visible = False
        self.is_responsible.label_visible = False


class MembershipInline(ModelAdminWidget):
    MODEL = models.Membership

    LIST_DISPLAY = ["group", "is_responsible", "is_manager"]
    LIST_HEADERS = ["Group", "Responsible", "Manager"]

    EDITFORM_CLASS = MembershipInlineForm

    USE_DETAILS_TO_ADD = False  # required to have form in NEW_TAB
    USE_DETAILS_TO_EDIT = False  # required to have form in NEW_TAB


class UserForm(ModelFormWidget):
    MODEL = User

    FIELDSETS = [
        segment(
            ("email", "date_joined", "last_login"),
            ("name", "display_name", "is_active"),
        ),
        segment("h3:Groups", "MembershipInline"),
    ]

    READ_ONLY = ["username", "email", "last_login", "date_joined"]

    INLINES = [MembershipInline]

    LAYOUT_POSITION = conf.ORQUESTRA_NEW_TAB

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.is_active.checkbox_type = ""

        # Custom labels because Django likes smallcase verbose names
        self.email.label = "Email address"
        self.date_joined.label = "Date joined"
        self.last_login.label = "Last login"
        self.is_active.label = "Active"

    @property
    def title(self):
        try:
            return self.model_object.get_display_name()
        except AttributeError:
            pass  # apparently it defaults to App TITLE


class UsersListApp(ModelAdminWidget):

    UID = "users"
    MODEL = models.User
    TITLE = "Users"

    LIST_DISPLAY = [
        "name",
        "email",
        "get_group",
        "is_active",
        "date_joined",
        "last_login",
    ]

    LIST_FILTER = [
        "memberships__group",
        "memberships__group__accesses__animaldb",
        "is_active",
    ]

    SEARCH_FIELDS = ["name__icontains", "email__icontains"]

    EDITFORM_CLASS = UserForm

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

        self._list.headers = [
            "Name",
            "Email address",
            "Group",
            "Active",
            "Date joined",
            "Last login",
        ]
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
