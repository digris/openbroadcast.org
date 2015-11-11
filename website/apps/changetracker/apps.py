from django.apps import AppConfig
from models import setup_registry

class ChangeTrackerConfig(AppConfig):
    name = 'changetracker'
    verbose_name = "Change Tracker"

    def ready(self):
        setup_registry()