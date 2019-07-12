from confapp import conf
from pyforms_web.organizers import no_columns, segment
from pyforms_web.widgets.django import ModelAdminWidget
from pyforms_web.widgets.django import ModelFormWidget

from users import models


class DatabaseAccessInline(ModelAdminWidget):
    MODEL = models.DatabaseAccess

    LIST_DISPLAY = ["animaldb", "level"]


class MembershipInlineForm(ModelFormWidget):
    FIELDSETS = [no_columns("user", "is_responsible", "is_manager")]


class MembershipInline(ModelAdminWidget):
    MODEL = models.Membership

    EDITFORM_CLASS = MembershipInlineForm

    LIST_DISPLAY = ["user", "is_responsible", "is_manager"]


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

    LIST_DISPLAY = ["id", "name", "databases", "users_count"]

    AUTHORIZED_GROUPS = ["superuser"]

    EDITFORM_CLASS = GroupForm

    USE_DETAILS_TO_EDIT = False  # required to have form in NEW_TAB

    LAYOUT_POSITION = conf.ORQUESTRA_HOME
    ORQUESTRA_MENU = "middle-left"
    ORQUESTRA_MENU_ORDER = 10
    ORQUESTRA_MENU_ICON = "users"
