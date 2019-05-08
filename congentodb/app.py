from django.apps import AppConfig

class CongentoDbConfig(AppConfig):
    name = 'congentodb'
    verbose_name = 'CongentoDb'

    def ready(self):
        import congentodb.signals