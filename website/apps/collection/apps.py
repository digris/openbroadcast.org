# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.apps import AppConfig


class CollectionConfig(AppConfig):
    name = "collection"
    verbose_name = "Collection App"

    def ready(self):
        import collection.signals
