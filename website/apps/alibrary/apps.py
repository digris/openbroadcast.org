from django.apps import AppConfig


class AlibraryConfig(AppConfig):
    name = "alibrary"
    verbose_name = "Library App"

    def ready(self):
        import alibrary.signals  # noqa
