# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
app = Celery('project')

app.config_from_object('django.conf:settings')


# app.conf.update(
#     #CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
#     CELERY_RESULT_BACKEND='djcelery.backends.cache:CacheBackend',
#     CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler",
# )