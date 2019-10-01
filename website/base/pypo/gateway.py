# -*- coding: utf-8 -*-
import json
import logging
from kombu import Connection
from celery.task import task
from django.conf import settings

log = logging.getLogger(__name__)

USE_CELERYD = getattr(settings, "PYPO_USE_CELERYD", False)
PLAYOUT_BROKER_URL = getattr(settings, "PLAYOUT_BROKER_URL", False)

BROKER_QUEUE = "pypo-fetch"


class PypoGateway(object):
    def __init__(self):
        pass

    def send(self, message):
        if USE_CELERYD:
            self.send_task.delay(self, message)
        else:
            self.send_task(self, message)

    @task
    def send_task(obj, message):
        log.info("send message: %s" % message["event_type"])
        try:

            connection = Connection(PLAYOUT_BROKER_URL)

            simple_queue = connection.SimpleQueue(BROKER_QUEUE)
            simple_queue.put(json.dumps(message))
            simple_queue.close()
            connection.close()

        except Exception as e:
            log.error("error sending message: %s" % e)


def send(message):
    pg = PypoGateway()
    pg.send(message)
