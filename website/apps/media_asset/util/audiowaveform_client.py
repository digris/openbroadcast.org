# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import requests
import logging
import tempfile

log = logging.getLogger(__name__)


API_URL = "http://10.10.8.202:2001/png/1800/301"


class AudioWaveformException(Exception):
    pass


def waveform_as_png(path):

    log.debug("generate waveform (as PNG) for: {}".format(path))

    url = API_URL
    files = {"file": open(path, "rb")}
    r = requests.post(url, files=files)

    if not r.status_code == 200:
        raise AudioWaveformException(
            "Unable to process file: {} - {}".format(r.status_code, r.text)
        )

    png_path = tempfile.mkstemp(suffix=".png")[1]
    with open(png_path, "wb") as f:
        f.write(r.content)

    return png_path
