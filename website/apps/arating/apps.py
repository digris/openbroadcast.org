from django.apps import AppConfig


class AratingConfig(AppConfig):
    name = "arating"
    verbose_name = "Rating"

    def ready(self):
        prepare_enabled_models()


def prepare_enabled_models():
    pass
