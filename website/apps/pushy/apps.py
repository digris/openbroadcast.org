from django.apps import AppConfig
from .models import setup_signals

class PushyConfig(AppConfig):
    name = 'pushy'
    verbose_name = "Pushy"

    def ready(self):
        setup_signals()
