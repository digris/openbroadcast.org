import requests
import logging
import tempfile
from django.conf import settings

from requests.exceptions import RequestException


SERVICE_ENDPOINT = getattr(
    settings,
    "WAVEFORM_SERVICE_ENDPOINT",
    "http://10.10.8.202:2001/",
)

TIMEOUT = (10, 1200)

logger = logging.getLogger(__name__)


class AudioWaveformException(Exception):
    pass


def waveform_as_png(path):

    logger.debug(f"generate waveform (as PNG) for: {path}")

    url = SERVICE_ENDPOINT + "png/1800/301"
    headers = {
        "user-agent": "openbroadcast.org - waveform client/0.0.1",
    }

    files = {
        "file": open(path, "rb"),
    }

    try:
        r = requests.post(
            url,
            files=files,
            timeout=TIMEOUT,
            headers=headers,
        )
    except RequestException as e:
        logger.warning(f"error: {e}")
        raise AudioWaveformException(f"request error: {e}")

    if not r.status_code == 200:
        raise AudioWaveformException(
            f"Unable to process file: {r.status_code} - {r.text}"
        )

    png_path = tempfile.mkstemp(suffix=".png")[1]
    with open(png_path, "wb") as f:
        f.write(r.content)

    return png_path
