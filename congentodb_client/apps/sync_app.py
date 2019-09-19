from confapp import conf
from pyforms_web.widgets.django import ModelAdminWidget
from ..models import MissedSync
from pyforms_web.allcontrols import ControlButton


class SyncApp(ModelAdminWidget):

    UID = "sync-with-congentodb"
    MODEL = MissedSync
    TITLE = "Sync with Congento DB"

    LIST_DISPLAY = ["contenttype", "object_id", "operation", "created"]

    LIST_HEADERS = ["Table", "Object ID", "Operation", "Created on"]

    LAYOUT_POSITION = conf.ORQUESTRA_HOME
    ORQUESTRA_MENU = "middle-left"
    ORQUESTRA_MENU_ORDER = 10
    ORQUESTRA_MENU_ICON = "database"

    def __init__(self, *args, **kwargs):

        self._sync_btn = ControlButton(
            "Syncronize data with the remote Congento DB",
            default=self.__sync_evt,
            css="red",
        )

        super().__init__(*args, **kwargs)

        self._list.item_selection_changed_event = lambda: None

        self.formset = ["_sync_btn", "_list"]

    @classmethod
    def has_permissions(cls, user):
        if user.is_superuser or user.is_admin(cls.MODEL._meta.app_label):
            return True
        return False

    def get_queryset(self, request, queryset):
        return queryset.filter(committed=None)

    def __sync_evt(self):

        for o in MissedSync.objects.filter(committed=None).order_by("created"):
            o.sync()
            print(o)

        self.populate_list()

    def has_add_permissions(self):
        return False

    def has_view_permissions(self, obj):
        return False

    def has_update_permissions(self, obj):
        return False
