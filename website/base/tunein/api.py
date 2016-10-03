# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests
import logging
log = logging.getLogger(__name__)

class TuneinAPIClient:

    def __init__(self, station_id, partner_id, partner_key):

        self.station_id = station_id
        self.partner_id = partner_id
        self.partner_key = partner_key


    def set_metadata(self, content_object):

        """
        http://air.radiotime.com/Playing.ashx?partnerId=<id>&partnerKey=<key>&id=<stationid>&title=Bad+Romance&artist=Lady+Gaga
        """

        url = 'http://air.radiotime.com/Playing.ashx'
        params = {
            'partnerId': self.partner_id,
            'partnerKey': self.partner_key,
            'id': self.station_id,
            'title': content_object.name,
            'artist': content_object.get_artist_display(),
            'album': content_object.release.name if content_object.release else '',
        }

        r = requests.get(url, params=params, timeout=2.0)

        if r.status_code == 200:
            log.info('successfully updated tunein metadata')
        else:
            log.warning('unable to set tunein metadata')



def set_tunein_metadata(channel, content_object):
    try:
        api = TuneinAPIClient(
            station_id=channel.tunein_station_id,
            partner_id=channel.tunein_partner_id,
            partner_key=channel.tunein_partner_key
        )
        api.set_metadata(content_object)
    except Exception as e:
        log.warning(u'unable to set tunein metadata text: %s' % e)
