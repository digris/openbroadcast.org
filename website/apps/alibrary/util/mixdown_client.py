import requests
import logging

#API_BASE_URL = 'http://localhost:8080/api/v1/'
API_BASE_URL = 'http://mixdown.apps.pbi.io/api/v1/'

log = logging.getLogger(__name__)

class MixdownAPIClient(object):

    def __init__(self):
        pass

    def get_for_playlist(self, obj):

        url = '{api_base_url}mixdown/playlist/{id}/'.format(
            api_base_url=API_BASE_URL,
            id=obj.pk
        )

        log.debug('loading mixdown from: {}'.format(url))

        r = requests.get(url, timeout=2.0)

        if not r.status_code == 200:
            return

        return r.json()

    def request_for_playlist(self, obj):

        url = '{api_base_url}mixdown/playlist/'.format(
            api_base_url=API_BASE_URL,
        )

        log.debug('requesting mixdown from: {}'.format(url))

        data = {
            'remote_uri': '{}{}'.format('https://www.openbroadcast.org', obj.get_api_url())
        }

        r = requests.post(url, json=data, timeout=2.0)

        print '-' * 72
        print r.text
        print '-' * 72

        if not r.status_code == 200:
            return

        return r.json()
