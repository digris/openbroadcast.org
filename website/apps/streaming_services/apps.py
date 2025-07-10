from django.apps import AppConfig


class StreamingServicesConfig(AppConfig):
    name = "streaming_services"
    verbose_name = "Streaming Services Connector"

    def ready(self):
        import streaming_services.signals  # noqa
