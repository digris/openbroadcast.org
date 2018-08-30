# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging

from django.core.cache import cache
from pushy.util import pushy_custom
from base.icecast.api import set_stream_metadata
from base.tunein.api import set_tunein_metadata
from metadata_generator.radioplayer.generator import set_radioplayer_metadata


log = logging.getLogger(__name__)


def start_play(item, channel=None, user=None):
    log.debug('item: %s - channel: %s - user: %s' % (item, channel, user))

    # Set current values to cache
    cache.set('abcast_on_air_%s' % channel.pk, item, 30)

    # Broadcast to pushy clients
    pushy_custom('%son-air/' % channel.get_api_url())


    if item.release and not 'jingle' in item.release.name.lower():

        try:
            text = '%s by %s - %s' % (item.name, item.artist.name, item.release.name)
            set_stream_metadata(channel, text)
        except Exception as e:
            log.warning('unable to set stream metadata: {}'.format(e))

        try:
            set_tunein_metadata(channel, item)
        except Exception as e:
            log.warning('unable to set tunein metadata: {}'.format(e))

        try:
            set_radioplayer_metadata(item)
        except Exception as e:
            log.warning('unable to set radioplayer metadata: {}'.format(e))


    try:
        from atracker.util import create_event
        create_event(user, item, channel, 'playout')
    except Exception as e:
        log.warning('exception: %s' % e)
