import requests
import logging
import dateutil.parser

from requests.exceptions import ConnectionError
from django.conf import settings

SITE_URL = settings.SITE_URL
API_BASE_URL = getattr(
    settings, "MIXDOWN_API_BASE_URL", "http://127.0.0.1:7778/api/v1/"
)
AUTH_TOKEN = getattr(settings, "MIXDOWN_API_AUTH_TOKEN", None)
REQUEST_TIMEOUT = (3.02, 10)


logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

log = logging.getLogger(__name__)


class MixdownAPIClient:
    """
    API client for mixdown service.
    """

    def __init__(self, auth_token=AUTH_TOKEN):

        self.headers = {
            "user-agent": "openbroadcast.org - mixdown client/0.0.1",
            "Authorization": f"Token {AUTH_TOKEN}",
        }

    def get_for_playlist(self, obj):

        url = f"{API_BASE_URL}mixdown/playlist/{obj.uuid}/"

        log.debug(f"loading mixdown from: {url}")

        try:
            r = requests.get(url, timeout=REQUEST_TIMEOUT, headers=self.headers)
        except ConnectionError as e:
            log.warning(f"unable to get data from mixdown api: {e}")
            return

        if r.status_code != 200:
            return

        return self.parse_mixdown_data(r.json())

    def request_for_playlist(self, obj):
        """
        request mixdown-rendering for a playlist
        """

        url = f"{API_BASE_URL}mixdown/playlist/{obj.uuid}/"

        log.debug(f"requesting mixdown: {url}")

        data = {"remote_uri": f"{SITE_URL}{obj.get_api_url()}"}

        try:
            r = requests.put(
                url, json=data, timeout=REQUEST_TIMEOUT, headers=self.headers
            )

            if r.status_code == 200:
                r = requests.patch(
                    url, json=data, timeout=REQUEST_TIMEOUT, headers=self.headers
                )

        except ConnectionError as e:
            log.warning(f"unable to post data to mixdown api: {e}")
            return

        if r.status_code not in [200, 201]:
            log.warning(f"{r.text}")
            return

        return self.parse_mixdown_data(r.json())

    @staticmethod
    def parse_mixdown_data(mixdown_data):
        """
        prepare data fields / parse values
        """
        mixdown_data["eta"] = dateutil.parser.parse(mixdown_data["eta"])

        return mixdown_data
