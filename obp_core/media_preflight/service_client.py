import logging
import requests
from django.conf import settings

from requests.exceptions import RequestException

SERVICE_ENDPOINT = settings.MEDIA_PREFLIGHT_SERVICE_ENDPOINT

SERVICE_TOKEN = settings.MEDIA_PREFLIGHT_SERVICE_TOKEN

TIMEOUT = (10, 600)


logger = logging.getLogger(__name__)


class PreflightServiceException(Exception):
    pass


def run_check(media):

    url = SERVICE_ENDPOINT + "preflight/"
    headers = {
        "user-agent": "openbroadcast.org - preflight client/0.0.1",
        "Authentication": f"Bearer {SERVICE_TOKEN}",
    }
    try:
        with open(media.master.path, "rb") as media_file:
            r = requests.post(
                url,
                files={"data": media_file},
                timeout=TIMEOUT,
                headers=headers,
            )
    except RequestException as e:
        logger.warning("error: %s", e)
        raise PreflightServiceException(f"request error: {e}")

    if not r.status_code == 200:
        raise PreflightServiceException(f"invalid status code: {r.status_code}")

    try:
        result = r.json()
    except Exception as e:
        raise PreflightServiceException(f"unable to decode response: {e}")

    return result
