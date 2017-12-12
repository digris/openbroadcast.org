# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import re
import os
import urllib
import contextlib
import hashlib
import requests
from BeautifulSoup import BeautifulSoup
from django.conf import settings
from django.db.models import Case, When

from l10n.models import Country
from alibrary.models import Relation
from alibrary.util.relations import uuid_by_url, uuid_by_object, get_service_by_url
from alibrary.util.storage import get_file_from_url, get_dir_for_object


log = logging.getLogger(__name__)

MUSICBRAINZ_HOST = getattr(settings, 'MUSICBRAINZ_HOST')
DISCOGS_HOST = getattr(settings, 'DISCOGS_HOST')
MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT')


CRAWLER_HEADERS = {
    'User-Agent': 'Open Broadcast Coverart Crawler 0.0.1',
}


#######################################################################
# image / coverart crawling
#######################################################################

class ArtworkCrawler(object):
    """
    artwork crawler
    """
    _default_services = [
        'wikidata',
        'discogs',
    ]

    def __init__(self, obj, services=None):
        self.obj = obj
        self._changes = {}

        if not services:
            self.services = self._default_services
        else:
            self.services = services

        # force order of services to crawl
        preserved = Case(*[When(service=service, then=pos) for pos, service in enumerate(self.services)])
        self.relations = obj.relations.filter(service__in=self.services).order_by(preserved)

        log.debug('crawling artwork: {} - id:{}'.format(obj, obj.pk))



    ###################################################################
    # direct field mappings
    # to be defined in type specific crawler
    ###################################################################
    def crawl_for_image_url(self):

        image_url = None

        for relation in self.relations:

            log.debug('crawling artwork on {} - {}'.format(relation.service, relation.url))

            _crawl_func = getattr(self, 'crawl_for_{service}_image'.format(service=relation.service))

            image_url = _crawl_func(relation.url)
            if image_url:
                log.info('found image on {}: {}'.format(relation.service, image_url))
                break


        return image_url




    def crawl_for_wikidata_image(slf, url):
        """
        parses wikidata url for id & tries to find valid image url
        """

        id = url.split('/')[-1].strip()
        #id = 'Q35694'

        api_url = 'https://www.wikidata.org/w/api.php?action=wbgetclaims&entity={id}&property=P18&format=json'.format(id=id)
        r = requests.get(api_url)

        if not r.status_code == 200:
            return

        data = r.json()

        # https://stackoverflow.com/a/34402875/469111
        try:
            image_name = data['claims']['P18'][0]['mainsnak']['datavalue']['value']
            image_name = image_name.replace(' ', '_')
        except KeyError as e:
            log.debug('no image data found: {}'.format(e))
            return

        # https://stackoverflow.com/a/34402875/469111
        md5 = hashlib.md5(image_name.encode('ascii', 'ignore')).hexdigest()
        image_url = 'https://upload.wikimedia.org/wikipedia/commons/{}/{}/{}'.format(
            md5[0:1],
            md5[0:2],
            urllib.quote_plus(image_name.encode('utf-8'))
        )

        # check if url returns 200
        r = requests.head(image_url)
        if r.status_code == 200:
            return image_url




    def crawl_for_discogs_image(slf, url):
        """
        parses wikidata url for id & tries to find valid image url
        """
        _bits = url.split('/')
        id = _bits[-1].strip()
        ctype = _bits[-2].strip()

        api_url = 'http://{host}/{ctype}s/{id}'.format(id=id, ctype=ctype, host=DISCOGS_HOST)
        r = requests.get(api_url)

        print(api_url)

        if not r.status_code == 200:
            return

        data = r.json()


        try:
            image_url = [i for i in data['images'] if i['type'] == 'primary'][0]['uri']
        except (KeyError, IndexError):
            image_url = None

        # try secondary image in case no primary
        if not image_url:
            try:
                image_url = [i for i in data['images'] if i['type'] == 'secondary'][0]['uri']
            except (KeyError, IndexError):
                return

        # check if url returns 200
        r = requests.head(image_url)
        if r.status_code == 200:
            return image_url


    def crawl_for_musicbrainz_image(slf, url):
        """
        parses id url for id & tries to find valid image on coverartarchive
        """
        _bits = url.split('/')
        id = _bits[-1].strip()
        ctype = _bits[-2].strip()

        image_url = 'http://coverartarchive.org/{ctype}/{id}/front'.format(id=id, ctype=ctype, host=DISCOGS_HOST)

        r = requests.get(image_url, allow_redirects=False)

        # 307: if front image available
        # header contains location/redirect
        # https://musicbrainz.org/doc/Cover_Art_Archive/API
        if r.status_code == 307 and 'Location' in r.headers:
            r2 = requests.head(r.headers['Location'], allow_redirects=True)
            return r2.url


    def crawl_for_wikipedia_image(slf, url):
        """
        parses id url for id & tries to find valid image on coverartarchive
        """
        page_url = url
        print(url)

        # image_url = 'http://coverartarchive.org/{ctype}/{id}/front'.format(id=id, ctype=ctype, host=DISCOGS_HOST)
        #
        r = requests.get(page_url, headers=CRAWLER_HEADERS)

        if not r.status_code == 200:
            return

        soup = BeautifulSoup(r.text)
        try:
            image_url = [t.find('img') for t in soup.findAll("table", {"class": "infobox vevent haudio"})][0]['src']
            if not image_url.startswith('http'):
                image_url = 'https:' + image_url
            return image_url
        except (KeyError, IndexError, TypeError) as e:
            log.debug('no image data found: {}'.format(e))
            return

    def download_and_save_image(self, image_url):
        """
        we cannot `use obj.image.save()` here - because this update the db timestamps
        and also trigger the `post_save` signal.
        so adding the file to the instance has to be done 'manually'
        """

        # 1. define files / directories
        _filename = 'logo.jpg'
        _dir = get_dir_for_object(self.obj)
        _path = os.path.join(_dir, _filename)

        _dir_abs = os.path.join(MEDIA_ROOT, _dir)
        _path_abs = os.path.join(MEDIA_ROOT, _path)


        # 2. create directory if absent
        if not os.path.isdir(_dir_abs):
            log.debug('create directory: {}'.format(_dir_abs))
            os.makedirs(_dir_abs)


        # 3. download image
        log.debug('save {} to {}'.format(image_url, _path_abs))
        _f = urllib.URLopener()
        _f.retrieve(image_url, _path_abs)
        _f.close()



        # 4. update item
        if os.path.isfile(_path_abs):
            type(self.obj).objects.filter(pk=self.obj.pk).update(
                main_image=_path
            )

        # 5. return reloaded object
        return type(self.obj).objects.get(pk=self.obj.pk)





    def run(self, save=False):
        """
        execute default sequence
        """

        image_url = self.crawl_for_image_url()
        if image_url and save:
            log.info('saving image to object')
            self.download_and_save_image(image_url)

        return image_url



#######################################################################
# 'shortcuts' for outside use
#######################################################################
def obj_crawl_artwork(obj, services=None, save=False):
    c = ArtworkCrawler(obj, services)
    return c.run(save=save)
