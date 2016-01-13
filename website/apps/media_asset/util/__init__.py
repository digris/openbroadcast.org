# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
import time

from media_asset.models import Format

log = logging.getLogger(__name__)

# shortcuts
def get_format(media, quality=Format.DEFAULT, encoding=Format.MP3, wait=False):


    if isinstance(media, str):
        log.debug('not a media instance - try to get by uuid: %s' % media)
        from alibrary.models import Media
        media = Media.objects.get(uuid=media)


    log.debug('getting format: %s - quality: %s - encoding: %s' % (media.uuid, quality, encoding))

    format, format_created = Format.objects.get_or_create(media=media, quality=quality, encoding=encoding)

    if wait:
        # hack to wait until file is ready
        counter = 0
        while format.status in [Format.INIT, Format.PROCESSING]:
            log.debug('format not ready yet. sleep for a while. %s' % counter)
            time.sleep(1)
            format.refresh_from_db()
            counter += 1
            if counter > 360:
                raise IOError('unable to process format')


    return format