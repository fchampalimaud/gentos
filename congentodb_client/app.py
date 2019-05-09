from django.apps import AppConfig

class CongentoDbConfig(AppConfig):
    name = 'congentodb_client'
    verbose_name = 'CongentoDb'

    def ready(self):
        import congentodb_client.signals