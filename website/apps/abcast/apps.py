from django.apps import AppConfig

class AbcastConfig(AppConfig):
    name = 'abcast'
    verbose_name = "Broadcast App"

    def ready(self):
        import abcast.signals  # noqa
