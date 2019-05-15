from django.apps import AppConfig


class CongentoDBConfig(AppConfig):
    name = "congentodb_client"
    verbose_name = "Congento DB Client"

    def ready(self):
        from .. import signals  # noqa

        from .links import CongentoDbLink
        from .sync_app import SyncApp

        global CongentoDbLink
        global SyncApp
