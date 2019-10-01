# -*- coding: utf-8 -*-
import logging

from django.conf import settings

DEVSERVER_HEADER = "HTTP_" + getattr(
    settings, "WEBPACK_DEVSERVER_HEADER", "X-WEBPACK-DEVSERVER"
).replace("-", "_")

log = logging.getLogger(__name__)


class WebpackDevserverMiddleware(object):
    def process_request(self, request):

        if request.META.get(DEVSERVER_HEADER, False):
            request.webpack_devserver = True

        return None
