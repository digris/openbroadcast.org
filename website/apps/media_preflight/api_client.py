# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import logging
import requests
import semver

from requests.exceptions import RequestException

from django.conf import settings
from requests.exceptions import ConnectionError

SITE_URL = getattr(settings, 'SITE_URL')
API_BASE_URL = getattr(settings, 'MEDIA_PREFLIGHT_API_BASE_URL', 'http://127.0.0.1:7779/api/v1/')
AUTH_TOKEN = getattr(settings, 'MEDIA_PREFLIGHT_API_AUTH_TOKEN', None)
REQUEST_TIMEOUT = 15.0


logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

log = logging.getLogger(__name__)

class MediaPreflightAPIClient(object):
    """
    API client for fprint service.
    Handles lookups by code or media object as well as fingerprint ingestion to the service
    """

    def __init__(self, auth_token=AUTH_TOKEN):

        self.headers = {
            'user-agent': 'openbroadcast.org - preflight client/0.0.1',
        }

        if auth_token:
            self.headers.update({
                'Authorization': 'Token {}'.format(AUTH_TOKEN)
            })


    def check(self):
        """
        checks remote api availability & version
        """

        # TODO: implement version check

        url = '{api_base_url}status/'.format(
            api_base_url=API_BASE_URL
        )

        api_version = None

        try:
            r = requests.get(url, timeout=REQUEST_TIMEOUT, headers=self.headers)

            if r.status_code == 200:
                data = r.json()
                api_version = data.get('version')

        except RequestException as e:
            log.warning('unable to call api: {}'.format(e))


        # print(api_version)
        if api_version:
            semver.parse_version_info(api_version)


    def request_check_for_media(self, obj):
        """
        sends code to preflight api
        """

        url = '{api_base_url}preflight/check/{uuid}/'.format(
            api_base_url=API_BASE_URL,
            uuid=obj.uuid,
        )

        data = {
            'uuid': '{}'.format(obj.uuid),
            # TODO: this is ugly. rework!
            'remote_uri': obj.preflight_check.get_api_url()
        }

        files = {'media_file': open(obj.master.path, 'rb')}

        log.debug('request media preflight at: {}'.format(url))
        log.debug('request media preflight payload: {}'.format(data))

        # TODO: add exception handling
        try:
            r = requests.get(url, timeout=REQUEST_TIMEOUT, headers=self.headers)
        except requests.exceptions.ConnectionError as e:
            log.warning('unable to process request: {}'.format(e))
            return

        if not r.status_code == 200:
            log.debug('entry does not exist > PUT')
            r = requests.put(url, data=data, files=files, timeout=REQUEST_TIMEOUT, headers=self.headers)

        else:
            log.debug('entry does exist > PATCH')
            r = requests.patch(url, data=data, files=files, timeout=REQUEST_TIMEOUT, headers=self.headers)

        if not r.status_code in [200, 201]:
            log.warning('{}'.format(r.text))
            return

        return r.json()

    def delete_check_for_media(self, media_uuid):
        """
        sends code to preflight api
        """

        url = '{api_base_url}preflight/check/{uuid}/'.format(
            api_base_url=API_BASE_URL,
            uuid=media_uuid,
        )

        log.debug('delete media preflight at: {}'.format(url))

        # TODO: add exception handling

        r = requests.delete(url, timeout=REQUEST_TIMEOUT, headers=self.headers)


        return r.status_code

