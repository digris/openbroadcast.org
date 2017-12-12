# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import re
import requests
import time
from django.conf import settings

from l10n.models import Country
from alibrary.models import Relation
from alibrary.util.relations import uuid_by_url, uuid_by_object, get_service_by_url

log = logging.getLogger(__name__)

DISCOGS_HOST = getattr(settings, 'DISCOGS_HOST')
DISCOGS_HOST = 'api.discogs.com'

SLEEP_ON_429 = 30



DISCOGS_RELATION_USE_SERVICES = [
    'imdb',
    'twitter',
    'bandcamp',
    'instagram',
    'facebook',
    'wikipedia',
    'youtube',
    'vimeo',
    'wikidata',
    'viaf',
]


def unify_name(text):
    """
    unify strings for matching - as different conventions/styles exist
    """
    _map = (
        ('’', '\''),
    )

    for c in _map:
        text = text.replace(c[0], c[1])

    return text


def strip_http(url):

    _map = (
        ('https://', ''),
        ('http://', ''),
        ('//', ''),
    )

    for c in _map:
        url = url.replace(c[0], c[1])

    return url


def strip_query_params(url):

    url = url.split('?')[0]

    return url


def format_approx_date(approx_date):

    if len(approx_date) == 4:
        approx_date = '{}-00-00'.format(approx_date)
    elif len(approx_date) == 7:
        approx_date = '{}-00'.format(approx_date)
    elif len(approx_date) == 10:
        approx_date = '{}'.format(approx_date)

    re_date_start = re.compile('^\d{4}-\d{2}-\d{2}$')

    if re_date_start.match(approx_date) and approx_date != '0000-00-00':
        return '{}'.format(approx_date)



#######################################################################
# discogs crawling
#######################################################################
class DiscogsCrawler(object):
    """
    generic musicbrainz crawler
     - implements loading data from api
     - implements crawling of relations a.k.a. urls
     - implements flow
    """

    def __init__(self, obj):
        self.obj = obj

        """
        url format: 
        https://www.discogs.com/label/401445-Zzyzx-Music or 
        https://www.discogs.com/label/401445
        """
        _url = obj.relations.filter(service='discogs').first().url
        _bits = _url.split('/')
        self.discogs_id = _bits[-1].strip().split('-')[0]
        self.discogs_ctype = _bits[-2].strip()

        log.debug('crawling metadata: {} - id:{} - discogs_id:{}'.format(obj, obj.pk, self.discogs_id))

        self._data = None
        self._changes = {}
        self._data = self.load_data_from_api()


    def load_data_from_api(self):


        url = 'http://{host}/{discogs_ctype}s/{discogs_id}'.format(
            host=DISCOGS_HOST,
            discogs_id=self.discogs_id,
            discogs_ctype=self.discogs_ctype
        )

        log.debug('load data from: {}'.format(url))

        try:
            r = requests.get(url)
        except Exception as e:
            log.warning('unable to load data - {}'.format(url))
            return

        if r.status_code == 429:
            log.warning('too many requests - 429')
            time.sleep(SLEEP_ON_429)
            self.load_data_from_api()

        if not r.status_code == 200:
            log.warning('unable to load data: {} - {}'.format(r.status_code, url))
            return

        return r.json()




    ###################################################################
    # direct field mappings
    # to be defined in type specific crawler
    ###################################################################
    def update_fields(self):
        raise NotImplementedError('implement on derived class')




    def update_relations(self):
        """
        relation mappings (urls)
        """

        if not self._data:
            return

        relations = self._data.get('urls')
        if relations:

            _relation_qs = self.obj.relations.all()
            _relation_urls = [strip_http(strip_query_params(r.url)) for r in _relation_qs]

            for url in relations:

                _service = get_service_by_url(url)
                log.debug('{}: {}'.format(_service, url))

                if _service in DISCOGS_RELATION_USE_SERVICES and not strip_http(strip_query_params(url))in _relation_urls:
                    rel = Relation(
                        content_object=self.obj,
                        url=strip_query_params(url),
                        service=_service
                    )
                    rel.save()

                    if not 'relations' in self._changes:
                        self._changes['relations'] = []

                    self._changes['relations'].append(url)


    def run(self):
        """
        execute default sequence
        """
        #self.update_fields()
        self.update_relations()

        if self._changes:
            log.info('apply changes on {}: {}'.format(self.obj, self._changes))
            return self._changes
        else:
            log.debug('no changes for {}'.format(self.obj))




class DiscogsLabelCrawler(DiscogsCrawler):
    """
    crawl label metadata
     - description
    """

    ###################################################################
    # direct field mappings
    ###################################################################
    def update_fields(self):

        if not self.obj.description:
            try:
                self._changes['description'] = self._data['profile']
            except (IndexError, KeyError, AttributeError):
                pass

        # update instance fields
        if self._changes:
            type(self.obj).objects.filter(pk=self.obj.pk).update(**self._changes)






#######################################################################
# 'shortcuts' for outside use
#######################################################################
def label_crawl_discogs(obj):
    c = DiscogsLabelCrawler(obj)
    return c.run()


