# -*- coding: utf-8 -*-
import logging
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch.dispatcher import receiver
from django.apps import apps
from changetracker import receivers
from changetracker.registry import tracker

TRACKED_MODELS = getattr(settings, 'CHANGETRACKER_TRACKED_MODELS', {})

print TRACKED_MODELS

log = logging.getLogger(__name__)

def setup_registry():


    for item in TRACKED_MODELS:

        model = apps.get_model(*item['model'].lower().split('.'))
        diff_function = item.get('diff_function', None)

        print 'model:         %s' % model
        print 'diff_function: %s' % diff_function

        kwargs = {'diff_function': diff_function}

        tracker.register(model, diff_function=diff_function)

        #pre_save.connect(receivers.tracker_update)


