# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import logging
import requests
import semver

from requests.exceptions import RequestException
from requests.auth import HTTPBasicAuth

from django.conf import settings
from requests.exceptions import ConnectionError

API_BASE_URL = getattr(
    settings, "RADIOPLAYER_API_BASE_URL", "https://ingest.swissradioplayer.ch"
)
API_STATION_ID = getattr(settings, "RADIOPLAYER_API_STATION_ID")
API_USER = getattr(settings, "RADIOPLAYER_API_USER")
API_PASSWORD = getattr(settings, "RADIOPLAYER_API_PASSWORD")

REQUEST_TIMEOUT = 15.0


logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

log = logging.getLogger(__name__)


class IngestAPIClient(object):
    """
    API client for fprint service.
    Handles lookups by code or media object as well as fingerprint ingestion to the service
    """

    def __init__(self):

        self.base_url = API_BASE_URL
        self.station_id = API_STATION_ID
        self.auth = HTTPBasicAuth(API_USER, API_PASSWORD)

        self.headers = {"user-agent": "openbroadcast.org - radioplayer client/0.0.1"}

    def compose_url(self, url):

        if url.startswith("http://") or url.startswith("https://"):
            return url

        return "{}{}".format(self.base_url, url)

    def get(self, url, params=None):

        _url = self.compose_url(url)

        log.info("API GET request: {} - {}".format(_url, params))

        r = requests.get(
            self.compose_url(_url), params, auth=self.auth, headers=self.headers
        )

        return r

    def post(self, url, payload={}):

        _url = self.compose_url(url)
        payload.update({"rpId": self.station_id})

        log.info("API POST request: {} - {}".format(_url, payload))

        r = requests.post(
            self.compose_url(_url), data=payload, auth=self.auth, headers=self.headers
        )

        return r
