# -*- coding: utf-8 -*-
import logging
import json
import time
from pushy import settings as pushy_settings
from multiprocessing import Pool

from django.db.models.signals import post_save, post_delete
import redis


log = logging.getLogger(__name__)

pool = Pool(processes=10)


def pushy_publish(channel, key, message):
    rs = redis.StrictRedis(host=pushy_settings.get_redis_host())
    time.sleep(0.005)
    return rs.publish("%s%s" % (channel, key), json.dumps(message))


def pushy_post_save(sender, **kwargs):

    if kwargs.get("raw"):
        return

    rs = redis.StrictRedis(host=pushy_settings.get_redis_host())
    obj = kwargs["instance"]
    created = kwargs["created"]

    try:
        pushy_ignore = obj._pushy_ignore
    except:
        pushy_ignore = False

    if pushy_ignore:
        return

    if created:
        action = "create"
        try:
            route = obj.get_api_list_url()
        except:
            route = obj.get_api_url()
    else:
        action = "update"
        route = obj.get_api_url()

    message = {"route": route, "type": action}
    log.debug("Routing message to: %s" % pushy_settings.get_channel())
    log.debug("route: %s" % route)

    # pushy_publish(pushy_settings.get_channel(), 'update', message)
    pool.apply_async(pushy_publish(pushy_settings.get_channel(), action, message))


def pushy_post_delete(sender, **kwargs):
    rs = redis.StrictRedis(host=pushy_settings.get_redis_host())
    obj = kwargs["instance"]

    message = {"route": obj.get_api_url(), "type": "delete"}
    log.debug("Routing message to: %s" % pushy_settings.get_channel())
    log.debug("route: %s" % obj.get_api_url())

    pool.apply_async(pushy_publish(pushy_settings.get_channel(), "delete", message))


def setup_signals():

    for model in pushy_settings.get_models().values():
        if not model:
            log.error("Unable to register model %s" % model)
            continue
        else:
            post_save.connect(pushy_post_save, sender=model)
            post_delete.connect(pushy_post_delete, sender=model)
            # log.debug('registered pushy signals for %s' % model)


# setup_signals()
