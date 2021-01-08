# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

logger = logging.getLogger(__name__)


def reassign_media(release, media_qs):
    logger.debug('re-assign media {} to {}'.format(media_qs, release))

    for media in media_qs:
        media.release = release
        media.save()

    release.refresh_from_db()

    return release
