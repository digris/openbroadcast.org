# -*- coding: utf-8 -*-
import logging
from pushy import settings as pushy_settings
from pushy.models import pushy_publish

log = logging.getLogger(__name__)


def pushy_custom(route, body=None, type="update"):

    message = {"route": route, "type": type, "body": body}

    log.debug("push custom %s-message to %s - %s" % (type, route, message))

    pushy_publish(pushy_settings.get_channel(), type, message)
