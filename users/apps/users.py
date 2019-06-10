from confapp import conf
from django.contrib.auth import get_user_model
from pyforms_web.widgets.django import ModelAdminWidget

User = get_user_model()


class UsersListApp(ModelAdminWidget):

    UID = "users"
    MODEL = User
    TITLE = "Users"

    AUTHORIZED_GROUPS = ['superuser']

    LIST_DISPLAY = ['email', 'is_active', 'is_staff', 'is_superuser']

    LAYOUT_POSITION = conf.ORQUESTRA_HOME
    ORQUESTRA_MENU = "middle-left"
    ORQUESTRA_MENU_ORDER = 10
    ORQUESTRA_MENU_ICON = "users"
