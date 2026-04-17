from django.apps import AppConfig


class BaseConfig(AppConfig):
    name = "base"
    verbose_name = "Base"

    def ready(self):
        import base.checks
