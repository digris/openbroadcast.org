import logging
import hashlib
import os

log = logging.getLogger(__name__)

def sha1_by_file(file):

    try:
        sha = hashlib.sha1()
        file.seek(0)
        sha.update(file.read())
        sha1 = sha.hexdigest()
        file.seek(0)

        return sha1

    except Exception as e:
        log.warning('unable to create sha1 hash: {}'.format(e))
