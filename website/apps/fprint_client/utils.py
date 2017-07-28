# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import os
import subprocess
import base64
import zlib
import itertools

from django.conf import settings

ECHOPRINT_CODEGEN_BINARY = getattr(settings, 'ECHOPRINT_CODEGEN_BINARY', None)

def split_seq(iterable, size):
    it = iter(iterable)
    item = list(itertools.islice(it, size))
    while item:
        yield item
        item = list(itertools.islice(it, size))


def decode_echoprint(echoprint_b64_zipped):
    """
    decode an echoprint string as output by `echoprint-codegen`.
    (https://github.com/spotify/echoprint-server/blob/master/echoprint_server/lib.py)
    """
    zipped = base64.urlsafe_b64decode(echoprint_b64_zipped)
    unzipped = zlib.decompress(zipped)
    N = len(unzipped)
    offsets = [int(''.join(o), 16) for o in split_seq(unzipped[:N/2], 5)]
    codes = [int(''.join(o), 16) for o in split_seq(unzipped[N/2:], 5)]
    return offsets, codes




def fprint_from_path(path, quiet=False):
    """
    generates echoprint data (code & metadata) for file at given path
    """

    if not os.path.isfile(path):
        if quiet:
            return
        raise IOError('file does not exist: {}'.format(path))

    command = [
        ECHOPRINT_CODEGEN_BINARY,
        path
    ]

    p = subprocess.Popen(command, stdout=subprocess.PIPE, close_fds=True)

    data = json.loads(p.stdout.read())[0]

    return data


def code_from_path(path, **kwargs):
    """
    generates echoprint code for file at given path
    """

    data = fprint_from_path(path, **kwargs)
    code = str(data['code'])

    return code
