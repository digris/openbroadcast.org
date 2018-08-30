from __future__ import absolute_import, unicode_literals

import logging
import requests

from django.utils import timezone
from django.conf import settings
from easy_thumbnails.files import get_thumbnailer

from .api_client import IngestAPIClient

SITE_URL = getattr(settings, 'SITE_URL')

log = logging.getLogger(__name__)


class RadioplayerMetadataGenerator(object):
    """
    generates metadata for swissradioplayer
    """
    def __init__(self):
        self.client = IngestAPIClient()


    def ingest_now_playing(self, media):
        """
        http://support.radioplayer.co.uk/customer/en/portal/articles/1127184-how-to-submit-metadata-to-radioplayer
        http://dev.radioplayer.at/support/informationen-fuer-ihre-hoerer-verfuegbar-machen/metadaten-an-den-radioplayer-uebermitteln/

        curl -u ***:*** -v \
            --data "rpId=***&startTime=2018-08-29T13:55:00&duration=3600&title=Love Power&artist=Nicola Conte" \
            -X POST "https://ingest.swissradioplayer.ch/ingestor/metadata/v1/np/"
        """

        log.info('set now playing: {}'.format(media))

        start = (timezone.now() - timezone.timedelta(hours=2)).replace(microsecond=0).isoformat()

        payload = {
            'startTime': start,
            'duration': int(media.master_duration),
            'title': media.name,
            'artist': media.get_artist_display()
        }

        try:
            # generate thumbnail image
            opts = {
                'crop': True,
                'quality': 80,
                'size': (86, 48)
            }
            thumbnailer = get_thumbnailer(media.release.main_image).get_thumbnail(opts)
            thumbnail_url = '{}{}'.format(SITE_URL, thumbnailer.url)

            payload.update({
                'imageUrl': thumbnail_url
            })

        except Exception as e:
            log.warning('unable to generate thumbnail image: {}'.format(e))


        r = self.client.post('/ingestor/metadata/v1/np/', payload=payload)
        log.info('returned status code: {}'.format(r.status_code))


    def __set_now_playing(self, media, start, duration):
        """
        curl -u ing_ob:Swissradio1 -v --data "rpId=155&startTime=2018-08-29T13:55:00&duration=3600&title=Love Power&artist=Nicola Conte" -X POST "https://ingest.swissradioplayer.ch/ingestor/metadata/v1/np/"
        """

        log.info('set now playing: {} {} {}'.format(media, start, duration))

        # r = self.client.get('/ingestor/metadata/v1/18884470')

        _start = (start - timezone.timedelta(hours=2)).replace(microsecond=0).isoformat()

        _start = (timezone.now() - timezone.timedelta(hours=2)).replace(microsecond=0).isoformat()
        #
        # print(_start)

        payload = {
            'startTime': _start,
            'duration': int(duration / 1000),
            'title': media.name,
            'artist': media.get_artist_display()
        }

        r = self.client.post('/ingestor/metadata/v1/np/', payload=payload)

        # print(r)
        # print(r.__dict__)
        # print(r.headers['Location'])
        # print(r.text)

        pass




def get_item_timing(emission, content_object):

    for item in emission.get_timestamped_media():
        if item.content_object == content_object:
            return {
                'start': item.timestamp,
                'duration': item.playout_duration,
            }


# def set_radioplayer_metadata(emission, content_object):
#
#     log.info('set now playing: {} {}'.format(
#         emission, content_object
#     ))
#
#     timing = get_item_timing(emission, content_object)
#
#     rpc = RadioplayerMetadataGenerator()
#
#
#     rpc.set_now_playing(
#         media=content_object,
#         start=timing['start'],
#         duration=timing['duration'],
#     )
#
#     pass


def set_radioplayer_metadata(content_object):
    """
    TODO: this is a temporary way that just allows to ingest 'title' & 'artist'
    `set_radioplayer_metadata` is called as soon as a new item starts playing, and
    so can be used in the same way as updates to icecast / tunein.
    """

    log.info('set now playing: {}'.format(
        content_object
    ))

    rpc = RadioplayerMetadataGenerator()
    rpc.ingest_now_playing(media=content_object)


