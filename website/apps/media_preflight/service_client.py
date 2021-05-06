# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
import requests
from django.conf import settings

from requests.exceptions import RequestException

SERVICE_ENDPOINT = getattr(
    settings,
    "MEDIA_PREFLIGHT_SERVICE_ENDPOINT",
    "https://media-preflight-service-kcek2ea7xq-oa.a.run.app/",
)

SERVICE_TOKEN = getattr(settings, "MEDIA_PREFLIGHT_SERVICE_TOKEN", None)

TIMEOUT = (10, 600)


logger = logging.getLogger(__name__)


class PreflightServiceException(Exception):
    pass


def run_check(media):

    url = SERVICE_ENDPOINT + "preflight/"
    headers = {
        "user-agent": "openbroadcast.org - preflight client/0.0.1",
        "Authentication": "Bearer {}".format(SERVICE_TOKEN),
    }
    files = {
        "data": open(media.master.path, "rb"),
    }

    try:
        r = requests.post(
            url,
            files=files,
            timeout=TIMEOUT,
            headers=headers,
        )
    except RequestException as e:
        logger.warning("error: {}".format(e))
        raise PreflightServiceException("request error: {}".format(e))

    if not r.status_code == 200:
        raise PreflightServiceException("invalid status code: {}".format(r.status_code))

    try:
        result = r.json()
    except Exception as e:
        raise PreflightServiceException("unable to decode response: {}".format(e))

    return result
