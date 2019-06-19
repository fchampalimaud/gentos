from confapp import conf
from pyforms_web.widgets.django import ModelAdminWidget
from pyforms_web.widgets.django import ModelFormWidget

from users.models import Group
from users.models import Membership


class MembershipInline(ModelAdminWidget):
    MODEL = Membership

    LIST_DISPLAY = ["user", "is_responsible", "is_manager"]


class GroupForm(ModelFormWidget):
    FIELDSETS = [
        ("name", "institution"),
        " ",
        "MembershipInline",
    ]

    INLINES = [MembershipInline]

    LAYOUT_POSITION = conf.ORQUESTRA_NEW_TAB

    @property
    def title(self):
        try:
            return self.model_object.name
        except AttributeError:
            pass  # apparently it defaults to App TITLE


class GroupsListApp(ModelAdminWidget):

    UID = "groups"
    MODEL = Group
    TITLE = "Groups"

    AUTHORIZED_GROUPS = ['superuser']

    EDITFORM_CLASS = GroupForm

    USE_DETAILS_TO_EDIT = False  # required to have form in NEW_TAB

    LAYOUT_POSITION = conf.ORQUESTRA_HOME
    ORQUESTRA_MENU = "middle-left"
    ORQUESTRA_MENU_ORDER = 10
    ORQUESTRA_MENU_ICON = "users"
