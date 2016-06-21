# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.apps import AppConfig


class AlibraryConfig(AppConfig):
    name = 'alibrary'
    verbose_name = "Library App"

    def ready(self):
        import alibrary.signals
