# encoding: utf-8
"""
A convenient way to attach django-elasticsearch-dsl to Django's signals and
cause things to index.
"""

from __future__ import absolute_import

from django.db import models
from django.apps import apps

from celery import shared_task

from django_elasticsearch_dsl.signals import BaseSignalProcessor
from django_elasticsearch_dsl.registries import registry


class CelerySignalProcessor(BaseSignalProcessor):

    def setup(self):
        # Listen to all model saves.
        models.signals.post_save.connect(self.handle_save)
        models.signals.post_delete.connect(self.handle_delete)

        # Use to manage related objects update
        models.signals.m2m_changed.connect(self.handle_m2m_changed)
        models.signals.pre_delete.connect(self.handle_pre_delete)

    def teardown(self):
        # Disconnect signals.
        models.signals.post_save.disconnect(self.handle_save)
        models.signals.post_delete.disconnect(self.handle_delete)
        models.signals.m2m_changed.disconnect(self.handle_m2m_changed)
        models.signals.pre_delete.disconnect(self.handle_pre_delete)


    def handle_save(self, sender, instance, **kwargs):
        pk = instance.pk
        app_label = instance._meta.app_label
        model_name = instance._meta.concrete_model.__name__
        self.handle_save_task.delay(pk, app_label, model_name)


    @shared_task()
    def handle_save_task(pk, app_label, model_name):
        instance = apps.get_model(app_label, model_name).objects.get(pk=pk)
        registry.update(instance)
        registry.update_related(instance)
