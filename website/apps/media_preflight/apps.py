from django.apps import AppConfig


class MediaPreflightConfig(AppConfig):
    name = "media_preflight"
    verbose_name = "Media Preflight App"

    def ready(self):
        import media_preflight.signals  # noqa
