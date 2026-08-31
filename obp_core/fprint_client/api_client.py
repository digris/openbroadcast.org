import requests
import logging
from django.conf import settings

from .utils import code_from_path

API_BASE_URL = getattr(settings, "FPRINT_API_BASE_URL", "http://127.0.0.1:7777/api/v1/")


logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

log = logging.getLogger(__name__)


class FprintAPIClient:
    """
    API client for fprint service.
    Handles lookups by code or media object as well as fingerprint ingestion to the service
    """

    def __init__(self):
        pass

    @staticmethod
    def identify(fprint, min_score=0.2, duration_tolerance=5.0):

        url = f"{API_BASE_URL}fprint/identify/"

        log.debug("loading fprint entry from: %s", url)

        fprint.update(
            {"min_score": min_score, "duration_tolerance": duration_tolerance}
        )

        try:
            r = requests.post(url, json=fprint)
            data = r.json()
        except BaseException:
            data = []

        return data

    def ingest_for_media(self, obj):
        """
        sends code to fprint api
        """

        url = f"{API_BASE_URL}fprint/entry/{obj.uuid}/"

        log.debug("ingest fprint entry to: %s", url)

        # TODO: implement exception handling
        try:
            code = code_from_path(obj.master.path)
        except BaseException:
            return

        if not code:
            log.warning("unable to generate echoprint code: %s", obj.master.path)
            return

        data = {
            #'uuid': str(obj.uuid), # uuid in uri
            "code": code,
            "duration": obj.master_duration,
            "name": obj.name,
            "artist_name": obj.artist.name if obj.artist else None,
        }

        # TODO: add exception handling
        try:
            r = requests.put(url, json=data, timeout=2.0)
        except requests.exceptions.ConnectionError as e:
            log.warning("unable to process request: %s", e)
            return

        if r.status_code not in [200, 201]:
            log.warning(
                "unable to ingest code for %s - status: %s - response: %s",
                obj.master.path,
                r.status_code,
                r.text,
            )
            return

        return r.json()

    def delete_for_media(self, media_uuid):
        """
        sends code to fprint api
        """

        url = f"{API_BASE_URL}fprint/entry/{media_uuid}/"

        log.debug("delete fprint entry: %s", url)

        r = requests.delete(url, timeout=2.0)

        if r.status_code not in [200, 202, 204]:
            log.warning(
                "unable to delete code - status: %s - response: %s",
                r.status_code,
                r.text,
            )

        return r.status_code
