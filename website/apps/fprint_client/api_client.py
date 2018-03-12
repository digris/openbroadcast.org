# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import requests
import logging
from django.conf import settings

from .utils import fprint_from_path, code_from_path

API_BASE_URL = getattr(settings, 'FPRINT_API_BASE_URL', 'http://127.0.0.1:7777/api/v1/')


logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

log = logging.getLogger(__name__)

class FprintAPIClient(object):
    """
    API client for fprint service.
    Handles lookups by code or media object as well as fingerprint ingestion to the service
    """

    def __init__(self):
        pass


    @staticmethod
    def identify(fprint, min_score=0.2, duration_tolerance=5.0):

        url = '{api_base_url}fprint/identify/'.format(
            api_base_url=API_BASE_URL,
        )

        log.debug('loading fprint entry from: {}'.format(url))

        fprint.update({
            'min_score': min_score,
            'duration_tolerance': duration_tolerance,
        })

        try:
            r = requests.post(url, json=fprint)
            data = r.json()
        except:
            data = []

        return data


    def ingest_for_media(self, obj):
        """
        sends code to fprint api
        """

        url = '{api_base_url}fprint/entry/{uuid}/'.format(
            api_base_url=API_BASE_URL,
            uuid=obj.uuid,
        )

        log.debug('ingest fprint entry to: {}'.format(url))


        code = code_from_path(obj.master.path)

        if not code:
            log.warning('unable to generate echoprint code: {}'.format(obj.master.path))
            return

        data = {
            #'uuid': str(obj.uuid), # uuid in uri
            'code': code,
            'duration': obj.master_duration,
            'name': obj.name,
            'artist_name': obj.artist.name if obj.artist else None
        }

        r = requests.put(url, json=data, timeout=2.0)

        if not r.status_code in [200, 201]:
            log.warning('unable to ingest code for {} - status: {} - response: {}'.format(
                obj.master.path,
                r.status_code,
                r.text
            ))
            return

        return r.json()


    def delete_for_media(self, obj):
        """
        sends code to fprint api
        """

        url = '{api_base_url}fprint/entry/{uuid}/'.format(
            api_base_url=API_BASE_URL,
            uuid=obj.uuid,
        )

        log.debug('delete fprint entry: {}'.format(url))

        r = requests.delete(url, timeout=2.0)

        if not r.status_code in [200, 202, 204]:
            log.warning('unable to delete code - status: {} - response: {}'.format(
                r.status_code,
                r.text
            ))

        return r.status_code
