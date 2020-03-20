# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.apps import AppConfig


class StreamingServicesConfig(AppConfig):
    name = "streaming_services"
    verbose_name = "Streaming Services Connector"

    def ready(self):
        import streaming_services.signals  # noqa
