from __future__ import unicode_literals
from django.apps import AppConfig

class PlatformBaseConfig(AppConfig):
    name = 'platform_base'
    verbose_name = 'Platform'

    def ready(self):
        import platform_base.checks
