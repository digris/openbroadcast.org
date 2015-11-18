# -*- coding: utf-8 -*-
import os
from datetime import timedelta
from django.conf import settings
BASE_DIR = getattr(settings, 'BASE_DIR')
DEBUG = getattr(settings, 'DEBUG')


################################################################################
# messaging
################################################################################

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_CONFIRMATION_DAYS = 5
EMAIL_DEBUG = DEBUG
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'


################################################################################
# celery / rabbitmq
################################################################################

CELERYD_MAX_TASKS_PER_CHILD = 1
CELERY_ACCEPT_CONTENT = ['pickle', 'json',]
CELERY_RESULT_BACKEND = 'djcelery.backends.cache:CacheBackend'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

# broker settings, used to compose connection for playout messaging
BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_USER = "obp"
BROKER_PASSWORD = "obp"
BROKER_VHOST_PYPO = "playout"

# base broker url - used for task servers
BROKER_URL = 'amqp://obp:obp@127.0.0.1:5672/openbroadcast.org'
PLAYOUT_BROKER_URL = 'amqp://obp:obp@127.0.0.1:5672/openbroadcast.org/playout'

CELERY_IMPORTS = (
    'importer.util.importer', # ?
    'lib.pypo_gateway.gateway',
)

CELERY_ROUTES = {
    #'importer.models.process_task': {'queue': 'import'},
    # assign import task to single-instance worker
    'importer.models.import_task': {'queue': 'import'},
    'importer.models.process_task': {'queue': 'process'},
    'importer.util.importer.mb_complete_media_task': {'queue': 'complete'},
    #
    'alibrary.models.generate_media_versions_task': {'queue': 'convert'},
    'alibrary.models.create_waveform_image': {'queue': 'convert'},
}


CELERYBEAT_SCHEDULE = {
    'exporter-cleanup': {
        'task': 'exporter.models.cleanup_exports',
        'schedule': timedelta(seconds=600),
    },
    'importer-cleanup': {
        'task': 'importer.models.reset_hangin_files',
        'schedule': timedelta(seconds=600),
    },
}


"""
using django pushy
"""
# TODO: refactor settings in a way of:
# PUSHY_REGISTER_MODELS =
# PUSHY_REDIS_HOST =
# etc.
PUSHY_SETTINGS = {
    'MODELS': (
        'alibrary.playlist',
        'alibrary.media',
        'importer.import',
        'importer.importfile',
        'abcast.emission',
        'exporter.export',
        'abcast.channel',
    ),
    'SOCKET_SERVER': 'http://localhost:8888/',
    'CHANNEL_PREFIX': 'pushy_',
    'DEBUG': DEBUG
}
