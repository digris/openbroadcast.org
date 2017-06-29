import requests
import logging

from .utils import code_for_path

API_BASE_URL = 'http://localhost:7777/api/v1/'
#API_BASE_URL = 'http://mixdown.apps.pbi.io/api/v1/'


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
    def get_for_code(obj):

        url = '{api_base_url}fprint/search/'.format(
            api_base_url=API_BASE_URL,
        )

        log.debug('loading mixdown from: {}'.format(url))

        r = requests.get(url, timeout=2.0)

        if not r.status_code == 200:
            return

        return r.json()


    @staticmethod
    def get_for_media(obj):

        url = '{api_base_url}fprint/entry/{uuid}/'.format(
            api_base_url=API_BASE_URL,
            uuid=obj.uuid
        )

        log.debug('loading fprint entry from: {}'.format(url))

        r = requests.get(url, timeout=2.0)

        if not r.status_code == 200:
            return

        return r.json()


    def ingest_for_media(self, obj, update=False):

        if not update:
            existing_entry = self.get_for_media(obj)
            if existing_entry:
                return existing_entry


        url = '{api_base_url}fprint/entry/{uuid}/'.format(
            api_base_url=API_BASE_URL,
            uuid=obj.uuid,
        )

        log.debug('ingest fprint entry to: {}'.format(url))


        code = code_for_path(obj.master.path)

        data = {
            #'uuid': str(obj.uuid),
            'code': code
        }

        r = requests.put(url, json=data, timeout=2.0)

        if not r.status_code in [200, 201]:
            log.warning('{}'.format(r.text))
            return

        return r.json()
