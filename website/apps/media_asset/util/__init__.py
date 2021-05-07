# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging

from media_asset.models import Format

log = logging.getLogger(__name__)


def get_format(media, quality=Format.DEFAULT, encoding=Format.MP3, wait=False):

    if isinstance(media, str):
        log.debug("not a media instance - try to get by uuid: %s" % media.uuid)
        from alibrary.models import Media

        media = Media.objects.get(uuid=media)

    log.debug(
        "getting format: %s - quality: %s - encoding: %s"
        % (media.uuid, quality, encoding)
    )

    format = Format.objects.get_or_create_for_media(
        media=media, quality=quality, encoding=encoding, wait=wait
    )

    return format
