from pyforms_web.basewidget import BaseWidget


class ExternalLinkBaseWidget(BaseWidget):
    ORQUESTRA_MENU = "bottom-left"
    ORQUESTRA_MENU_ORDER = 900
    ORQUESTRA_MENU_ICON = "external alternate"


class CongentoDbLink(ExternalLinkBaseWidget):
    UID = "congentodb-link"
    TITLE = "Congento DB"

    ORQUESTRA_URL = "https://database.congento.org/"
    ORQUESTRA_TARGET = "_blank"
