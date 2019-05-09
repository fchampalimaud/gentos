from django.contrib.auth.models import User
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlText
from pyforms.controls import ControlLabel
from pyforms.controls import ControlButton
from pyforms.controls import ControlQueryList
from confapp import conf
from pyforms_web.organizers import segment, no_columns


class Dashboard(BaseWidget):

    UID = 'dashboard-app'
    TITLE = 'Dashboard'

    ########################################################
    #### ORQUESTRA CONFIGURATION ###########################
    ########################################################
    LAYOUT_POSITION      = conf.ORQUESTRA_HOME
    ORQUESTRA_MENU       = 'left'
    ORQUESTRA_MENU_ICON  = 'clipboard outline'
    ORQUESTRA_MENU_ORDER = 0
    ########################################################


    AUTHORIZED_GROUPS = ['superuser']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._label = ControlLabel('These users are pending your authorization to access the database', css='orange')
        self._list = ControlQueryList(field_css='wide seven', list_display=['username', 'email'], headers=['Username', 'Email'])
        self._accept = ControlButton('Accept user', label_visible=False, css='green', visible=False, default=self.__accept_evt)
        self._reject = ControlButton('Reject user', label_visible=False, css='red', visible=False, default=self.__reject_evt)

        self.formset  = [
            ' ',
            '_label',
            no_columns('_list','_accept', '_reject')
        ]

        self._list.item_selection_changed_event = self.__user_selected_evt
        self.populate_users_list()


    def populate_users_list(self):
        queryset = User.objects.filter(is_active=False)
        if queryset.exists():
            self._list.value = queryset
            self._label.show()
        else:
            self._list.hide()
            self._label.hide()




    def __user_selected_evt(self):
        user_id = self._list.selected_row_id
        user = User.objects.get(pk=user_id)

        self._accept.label = f"Accept [{user.username}]"
        self._accept.show()

        self._reject.label = f"Reject [{user.username}]"
        self._reject.show()


    def __accept_evt(self):
        user_id = self._list.selected_row_id
        user = User.objects.get(pk=user_id)
        user.is_active = True
        user.save()

        self.populate_users_list()
        self._reject.hide()
        self._accept.hide()

    def __reject_evt(self):
        user_id = self._list.selected_row_id
        user = User.objects.get(pk=user_id)
        user.delete()

        self.populate_users_list()
        self._reject.hide()
        self._accept.hide()