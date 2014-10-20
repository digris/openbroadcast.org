import json

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from dajaxice.decorators import dajaxice_register
import requests

from alibrary.models import APILookup, Release, Relation, Label, Artist, Media
from lib.util.merge import merge_model_objects

from alibrary.util.api_compare import get_from_provider


import logging
log = logging.getLogger(__name__)

MUSICBRAINZ_HOST = getattr(settings, 'MUSICBRAINZ_HOST', None)
DISCOGS_HOST = getattr(settings, 'DISCOGS_HOST', None)


@dajaxice_register
def api_lookup(request, *args, **kwargs):

    item_type = kwargs.get('item_type', None)
    item_id = kwargs.get('item_id', None)
    provider = kwargs.get('provider', None)

    log.debug('api_lookup: %s - id: %s - provider: %s' % (item_type, item_id, provider))

    try:
        data = get_from_provider(item_type, item_id, provider)
        return json.dumps(data, encoding="utf-8")
    except Exception, e:
        log.warning('api_lookup error: %s', e)
        return json.dumps({'error': e}, encoding="utf-8")



@dajaxice_register
def provider_search_query(request, *args, **kwargs):

    item_type = kwargs.get('item_type', None)
    item_id = kwargs.get('item_id', None)
    provider = kwargs.get('provider', None)

    log.debug('type: %s - id: %s - provider: %s' % (item_type, item_id, provider))

    data = {}
    try:
        if item_type == 'release' and provider == 'discogs':
            item = Release.objects.get(pk=item_id)
            ctype = ContentType.objects.get_for_model(item)
            data = {'query': '%s %s' % (item.name, item.get_artist_display())}

        if item_type == 'release' and provider == 'musicbrainz':
            item = Release.objects.get(pk=item_id)
            ctype = ContentType.objects.get_for_model(item)
            data = {'query': '%s' % (item.name)}

        if item_type == 'artist':
            item = Artist.objects.get(pk=item_id)
            ctype = ContentType.objects.get_for_model(item)
            data = {'query': '%s' % (item.name)}

        if item_type == 'media' and provider == 'discogs':
            item = Media.objects.get(pk=item_id)
            ctype = ContentType.objects.get_for_model(item)
            data = {'query': '%s' % (item.name)}

        if item_type == 'media' and provider == 'musicbrainz':
            item = Media.objects.get(pk=item_id)
            ctype = ContentType.objects.get_for_model(item)
            data = {'query': "%s AND artist:%s" % (item.name, item.artist.name)}

        if item_type == 'label':
            item = Label.objects.get(pk=item_id)
            ctype = ContentType.objects.get_for_model(item)
            data = {'query': '%s' % (item.name)}


        return json.dumps(data)

    except Exception, e:
        log.warning('%s' % e)
        return None



@dajaxice_register
def provider_search(request, *args, **kwargs):

    item_type = kwargs.get('item_type', None)
    item_id = kwargs.get('item_id', None)
    provider = kwargs.get('provider', None)
    query = kwargs.get('query', None)

    log.debug('query: %s' % (query))

    if provider == 'discogs':
        url = 'http://%s/database/search?q=%s&type=%s&per_page=%s' % (DISCOGS_HOST, query, item_type, 15)
        log.debug('query url: %s' % (url))
        r = requests.get(url)
        text = r.text
        if DISCOGS_HOST:
            text = text.replace('api.discogs.com', DISCOGS_HOST)
        results = json.loads(text)['results']
        for result in results:
            result['uri'] = 'http://www.discogs.com%s' % result['uri']

    if provider == 'musicbrainz':

        _type = item_type
        if item_type == 'media':
            _type = 'recording'

        import re
        query = re.sub('[^A-Za-z0-9 ]+', '', query)

        url = 'http://%s/ws/2/%s?query=%s&fmt=json' % (MUSICBRAINZ_HOST, _type, query)
        log.debug('query url: %s' % (url))
        r = requests.get(url)


        if item_type == 'release':
            results = json.loads(r.text)['releases']
            for result in results:
                result['uri'] = 'http://musicbrainz.org/release/%s' % result['id']
                result['thumb'] = 'http://coverartarchive.org/%s/%s' % (item_type, result['id'])

        if item_type == 'artist':
            results = json.loads(r.text)['artist']
            for result in results:
                result['uri'] = 'http://musicbrainz.org/artist/%s' % result['id']
                result['thumb'] = 'http://coverartarchive.org/%s/%s' % (item_type, result['id'])

        if item_type == 'label':
            results = json.loads(r.text)['labels']
            for result in results:
                result['uri'] = 'http://musicbrainz.org/label/%s' % result['id']
                result['thumb'] = 'http://coverartarchive.org/%s/%s' % (item_type, result['id'])

        if item_type == 'media':
            results = json.loads(r.text)['recording']
            for result in results:
                result['uri'] = 'http://musicbrainz.org/recording/%s' % result['id']


    data = {
        'query': query,
        'results': results,
    }



    try:
        data = json.dumps(data)
        return data

    except Exception, e:
        log.warning('%s' % e)
        return None


@dajaxice_register
def provider_update(request, *args, **kwargs):

    item_type = kwargs.get('item_type', None)
    item_id = kwargs.get('item_id', None)
    provider = kwargs.get('provider', None)
    uri = kwargs.get('uri', None)

    log.debug('uri: %s' % (uri))

    item = None
    data = {}
    try:
        if item_type == 'release':
            item = Release.objects.get(pk=item_id)

        if item_type == 'artist':
            item = Artist.objects.get(pk=item_id)

        if item_type == 'label':
            item = Label.objects.get(pk=item_id)

        if item_type == 'media':
            item = Media.objects.get(pk=item_id)


        if item and uri:
            rel = Relation(content_object=item, url=uri)
            rel.save()

        data = {
            'service': '%s' % rel.service,
            'url': '%s' % rel.url,
            }


    except Exception, e:
        log.warning('%s' % e)


    return json.dumps(data)









"""
listview functions (merge etc)
"""

@dajaxice_register
def merge_items(request, *args, **kwargs):

    item_type = kwargs.get('item_type', None)
    item_ids = kwargs.get('item_ids', None)
    master_id = kwargs.get('master_id', None)

    slave_items = []
    master_item = None
    data = {
        'status': None,
        'error': None
    }


    if item_type and item_ids and master_id:
        log.debug('type: %s - ids: %s - master: %s' % (item_type, ', '.join(item_ids), master_id))
        try:

            if item_type == 'release':
                items = Release.objects.filter(pk__in=item_ids).exclude(pk=int(master_id))
                for item in items:
                    slave_items.append(item)

                master_item = Release.objects.get(pk=int(master_id))
                if slave_items and master_item:
                    merge_model_objects(master_item, slave_items)
                    master_item.save()
                    # needed to clear cache
                    for media in master_item.media_release.all():
                        media.save()
                    data['status'] = True
                else:
                    data['status'] = False
                    data['error'] = 'No selection'


            if item_type == 'media':
                items = Media.objects.filter(pk__in=item_ids).exclude(pk=int(master_id))
                for item in items:
                    slave_items.append(item)

                master_item = Media.objects.get(pk=int(master_id))
                if slave_items and master_item:
                    merge_model_objects(master_item, slave_items)
                    master_item.save()
                    data['status'] = True
                else:
                    data['status'] = False
                    data['error'] = 'No selection'

            if item_type == 'artist':
                items = Artist.objects.filter(pk__in=item_ids).exclude(pk=int(master_id))
                for item in items:
                    slave_items.append(item)

                master_item = Artist.objects.get(pk=int(master_id))
                if slave_items and master_item:
                    merge_model_objects(master_item, slave_items)
                    master_item.save()
                    # needed to clear cache
                    """"""
                    for media in master_item.media_artist.all():
                        media.save()

                    data['status'] = True
                else:
                    data['status'] = False
                    data['error'] = 'No selection'

            if item_type == 'label':
                items = Label.objects.filter(pk__in=item_ids).exclude(pk=int(master_id))
                for item in items:
                    slave_items.append(item)

                master_item = Label.objects.get(pk=int(master_id))
                if slave_items and master_item:
                    merge_model_objects(master_item, slave_items)
                    master_item.save()
                    # needed to clear cache
                    """
                    for media in master_item.media_release.all():
                        media.save()
                    """
                    data['status'] = True
                else:
                    data['status'] = False
                    data['error'] = 'No selection'



        except Exception, e:
            log.warning('%s' % e)
            data['status'] = False
            data['error'] = '%s' % e

    return json.dumps(data)






