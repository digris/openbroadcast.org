# -*- coding: utf-8 -*-
import logging
from django.core.cache import cache
from base.icecast.api import set_stream_metadata
from base.tunein.api import set_tunein_metadata
from pushy.util import pushy_custom

log = logging.getLogger(__name__)

def start_play(item, channel=None, user=None):

    log.debug(u'item: %s - channel: %s - user: %s' % (item, channel, user))

    # Set current values to cache
    cache.set('abcast_on_air_%s' % channel.pk, item, 30)

    # Broadcast to pushy clients
    pushy_custom('%son-air/' % channel.get_api_url())

    # Update stream metadata
    text = u'%s by %s - %s' % (item.name, item.artist.name, item.release.name)
    set_stream_metadata(channel, text)

    if item.release and not 'jingle' in item.release.name.lower():
        set_tunein_metadata(channel, item)

    if user:
        try:
            from atracker.util import create_event
            create_event(user, item, channel, 'playout')
        except Exception, e:
            log.warning('exception: %s' % e)

