from confapp import conf
from pyforms_web.organizers import segment
from pyforms_web.widgets.django import ModelAdminWidget
from pyforms_web.widgets.django import ModelFormWidget

from .. import models


class DatabaseAccessInlineForm(ModelFormWidget):
    FIELDSETS = [("animaldb", "level")]

    LAYOUT_POSITION = conf.ORQUESTRA_NEW_WINDOW


class DatabaseAccessInline(ModelAdminWidget):
    MODEL = models.DatabaseAccess

    LIST_DISPLAY = ["animaldb", "level"]
    LIST_HEADERS = ["Database", "Access level"]

    EDITFORM_CLASS = DatabaseAccessInlineForm

    USE_DETAILS_TO_ADD = False  # required to have form in NEW_TAB
    USE_DETAILS_TO_EDIT = False  # required to have form in NEW_TAB


class MembershipInlineForm(ModelFormWidget):
    FIELDSETS = ["user", "is_responsible", "is_manager"]

    LAYOUT_POSITION = conf.ORQUESTRA_NEW_WINDOW

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.is_manager.checkbox_type = ""
        self.is_responsible.checkbox_type = ""

        self.is_manager.label_visible = False
        self.is_responsible.label_visible = False


class MembershipInline(ModelAdminWidget):
    MODEL = models.Membership

    LIST_DISPLAY = ["user", "is_responsible", "is_manager"]
    LIST_HEADERS = ["User", "Responsible", "Manager"]

    EDITFORM_CLASS = MembershipInlineForm

    USE_DETAILS_TO_ADD = False  # required to have form in NEW_TAB
    USE_DETAILS_TO_EDIT = False  # required to have form in NEW_TAB


class GroupForm(ModelFormWidget):
    FIELDSETS = [
        ("name", "institution"),
        segment("h3:Group Permissions", "DatabaseAccessInline"),
        segment("h3:Group Members", "MembershipInline"),
    ]

    INLINES = [DatabaseAccessInline, MembershipInline]

    LAYOUT_POSITION = conf.ORQUESTRA_NEW_TAB

    @property
    def title(self):
        try:
            return self.model_object.name
        except AttributeError:
            pass  # apparently it defaults to App TITLE


class GroupsListApp(ModelAdminWidget):
    UID = "groups"
    MODEL = models.Group
    TITLE = "Groups"

    LIST_DISPLAY = ["name", "databases", "users_count"]
    LIST_FILTER = ["accesses__animaldb"]
    SEARCH_FIELDS = ["name__icontains"]

    EDITFORM_CLASS = GroupForm

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

    def has_update_permissions(self, obj):
        # TODO allow update only their (admin) groups
        return False
