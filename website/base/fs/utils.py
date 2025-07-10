import logging
import os
import string
import hashlib

from base.utils.AsciiDammit import asciiDammit

VALID_CHARS = "-_.()[] {}{}".format(string.ascii_letters, string.digits)
EXCLUDE_CHARS = "/\\'"

log = logging.getLogger(__name__)


def safe_filename(filename):

    return asciiDammit(filename.replace("/", " "))


def sha1_by_file(file):

    try:
        sha = hashlib.sha1()
        file.seek(0)
        sha.update(file.read())
        sha1 = sha.hexdigest()
        file.seek(0)

        return sha1

    except Exception as e:
        log.warning(f"unable to create sha1 hash: {e}")


def clean_directory_tree_reverse(path):
    """
    Cleans directory tree if empty
    """

    if not os.path.isdir(path):
        path = os.path.dirname(path)

    if not os.path.isdir(path):
        raise OSError(f"Path does not seem to be a directory: {path}")

    if path.endswith("/"):
        path = path[:-1]

    # log.debug('clean tree: {0}'.format(path))

    empty = True
    while empty:
        for dirpath, dirs, files in os.walk(path):

            if files or dirs:
                empty = False
                # log.debug('breaking at non-empty directory: {0}'.format(path))
                break

            else:
                os.rmdir(path)
                path = os.path.dirname(path)
