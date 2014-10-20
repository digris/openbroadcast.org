# -*- coding: utf-8 -*-
"""
    PypoGateway
    ~~~~~~~~~

    :author: (c) 2013 by Jonas Ohrstrom.
    :license: GPLv3, see LICENSE for more details.
"""
import json
import logging

from kombu import Connection
from celery.task import task

log = logging.getLogger(__name__)

from django.conf import settings

USE_CELERYD = False

"""
Same config as used for celery setup
"""
BROKER_HOST = getattr(settings, 'BROKER_HOST', 'localhost')
BROKER_PORT = getattr(settings, 'BROKER_PORT', 5672)
BROKER_USER = getattr(settings, 'BROKER_USER', 'guest')
BROKER_PASSWORD = getattr(settings, 'BROKER_PASSWORD', 'guest')
BROKER_VHOST_PYPO = getattr(settings, 'BROKER_VHOST_PYPO', '/pypo')
BROKER_QUEUE = 'pypo-fetch'


# BROKER_HOST = 'node05.daj.anorg.net'

log = logging.getLogger(__name__)

class PypoGateway:

    def __init__(self):
        log.info('gateway init')

    def send(self, message):
        if USE_CELERYD:
            self.send_task.delay(self, message)
        else:
            self.send_task(self, message)

    @task
    def send_task(obj, message):
        log.info('send message: %s' % message['event_type'])
        try:
            connection = Connection('amqp://%s:%s@%s:%s/%s' % (BROKER_USER, BROKER_PASSWORD, BROKER_HOST, BROKER_PORT, BROKER_VHOST_PYPO))
            simple_queue = connection.SimpleQueue(BROKER_QUEUE)
            simple_queue.put(json.dumps(message))
            simple_queue.close()
            connection.close()
        except Exception, e:
            log.error('error sending message: %s' % e)


def send(message):
    pg = PypoGateway()
    pg.send(message)
