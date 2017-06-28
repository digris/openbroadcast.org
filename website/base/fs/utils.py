# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import os

log = logging.getLogger(__name__)



def clean_directory_tree_reverse(path):
    """
    Cleans directory tree if empty
    """

    if not os.path.isdir(path):
        path = os.path.dirname(path)

    if not os.path.isdir(path):
        raise IOError('Path does not seem to be a directory: {0}'.format(path))

    if path.endswith('/'):
        path = path[:-1]

    # log.debug('clean tree: {0}'.format(path))

    empty = True
    while empty:
        for dirpath, dirs, files in os.walk(path):

            if files or dirs:
                empty = False
                #log.debug('breaking at non-empty directory: {0}'.format(path))
                break

            else:
                os.rmdir(path)
                path = os.path.dirname(path)
