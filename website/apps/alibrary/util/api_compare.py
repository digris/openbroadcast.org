# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import re
import types

import requests

from alibrary.models import Release, Label, Artist, Media
from alibrary.util.relations import get_service_by_url
from django.conf import settings
from l10n.models import Country

log = logging.getLogger(__name__)

MUSICBRAINZ_HOST = getattr(settings, 'MUSICBRAINZ_HOST', None)
DISCOGS_HOST = getattr(settings, 'DISCOGS_HOST', None)

MUSICBRAINZ_404_MESSAGE = '''
We could not find the requested data on our Musicbrainz mirror server.<br>
This is a known issue and we're working on improving synchronisation of external data sources.
'''

class APILookup(object):

    def __init__(self, obj):
        self.obj = obj
        self.type = obj.__class__.__name__.lower()


class MusicbrainzAPILookup(APILookup):
    """
    Musicbrainz API implementation
    """

    def get_data(self, uri=None):
        log.debug('run musicbrainz lookup for %s - %s' % (self.obj, self.type))

        if not uri:
            uri = self.obj.relations.filter(service='musicbrainz')[0].url
        log.debug('musicbrainz uri: %s' % uri)

        # for consistency uri is handled in resp. method
        return getattr(self, 'get_%s' % self.type)(uri)


    def get_release(self, uri):

        provider_id = uri.split('/')[-1]
        inc = ('aliases', 'url-rels', 'annotation', 'tags', 'artist-rels', 'recordings', 'artists', 'labels', 'release-groups', 'artist-credits', 'isrcs')
        api_url = 'http://%s/ws/2/release/%s/?fmt=json&inc=%s' % (MUSICBRAINZ_HOST, provider_id, "+".join(inc))

        log.info('composed api url: %s' % api_url)

        r = requests.get(api_url)

        if r.status_code == 404:
            return {'error': MUSICBRAINZ_404_MESSAGE}

        data= r.json()

        res = {}
        d_tags = []
        mapped_media = None
        for k in data:
            mk = k

            if k == 'annotation':
                mk = 'description'

            if k == 'title':
                mk = 'name'

            if k == 'country':
                mk = 'release_country'

            if k == 'date':
                mk = 'releasedate_approx'

            if k == 'label-info':
                try:
                    if 'label' in data[k][0] and 'name' in data[k][0]['label']:
                        res['label_0'] = data[k][0]['label']['name']

                    if 'catalog-number' in data[k][0]:
                        res['catalognumber'] = data[k][0]['catalog-number']

                except:
                    pass

            if k == 'release-group':
                try:
                    res['releasetype'] = data[k]['primary-type']

                except:
                    pass


            if k == 'relations':
                mapped = []
                for rel in data[k]:
                    if 'url' in rel:
                        mapped.append({
                            'uri': rel['url']['resource'],
                            'service': get_service_by_url(rel['url']['resource'], None),
                            })
                data[k] = mapped

            if k == 'media':
                mapped_media = []
                pos = 0
                disc_no = 0

                for disc in data[k]:
                    disc_no += 1
                    for m in disc['tracks']:
                        pos += 1

                        if 'artist-credit' in m:
                            track_artists = m['artist-credit']
                        else:
                            track_artists = []

                        if 'recording' in m and 'isrcs' in m['recording']:
                            isrcs = m['recording']['isrcs']
                        else:
                            isrcs = []

                        mapped_media.append({
                            'number': '%s' % (pos),
                            'position': '%s-%s' % (disc_no, pos),
                            'duration': m['length'],
                            'title': m['title'],
                            'artists': track_artists,
                            'isrcs': isrcs,
                            })



            if k == 'tags':
                try:
                    d = data[k]
                    for v in d:
                        d_tags.append(v['name'])
                except:
                    pass


            res[mk] = data[k]

        # try to remap country
        if 'release_country' in res:
            try:
                c = Country.objects.get(iso2_code=res['release_country'])
            except:
                pass

        try:
            url = 'http://coverartarchive.org/release/%s' % id
            r = requests.get(url)
            if r.ok:
                res['main_image'] = r.json()['images'][0]['image']
                res['remote_image'] = r.json()['images'][0]['image']
        except:
            pass



        try:
            num_tracks = 0
            for x in data['media']:
                num_tracks += int(x['track-count'])
            res['totaltracks'] = num_tracks if num_tracks > 0 else None
        except:
            pass

        res['d_tags'] = ', '.join(d_tags)

        # disable tags on mb
        res['d_tags'] = res['tags'] = ''


        res['tracklist'] = mapped_media

        return res


    def get_artist(self, uri):

        provider_id = uri.split('/')[-1]
        inc = ('aliases', 'url-rels', 'annotation', 'tags', 'artist-rels')
        api_url = 'http://%s/ws/2/artist/%s/?fmt=json&inc=%s' % (MUSICBRAINZ_HOST, provider_id, "+".join(inc))

        log.info('composed api url: %s' % api_url)

        r = requests.get(api_url)

        if r.status_code == 404:
            return {'error': MUSICBRAINZ_404_MESSAGE}

        data = r.json()

        res = {}
        d_tags = []
        for k in data:
            mk = k
            if k == 'annotation':
                mk = 'description'

            if k == 'life-span':
                if 'begin' in data[k]:
                    res['date_start'] = data[k]['begin']

                if 'end' in data[k]:
                    res['date_end'] = data[k]['end']

            if k == 'relations':
                mapped = []
                for rel in data[k]:
                    if 'url' in rel:
                        mapped.append({
                            'uri': rel['url']['resource'],
                            'service': get_service_by_url(rel['url']['resource'], None),
                            })
                data[k] = mapped

            if k == 'ipis':
                try:
                    d = data[k]
                    res['ipi_code'] = d[0]
                except:
                    pass

            if k == 'isni':
                try:
                    d = data[k]
                    res['isni_code'] = d
                except:
                    pass

            if k == 'tags':
                try:
                    d = data[k]
                    for v in d:
                        d_tags.append(v['name'])
                except:
                    pass

            res[mk] = data[k]

        res['d_tags'] = ', '.join(d_tags)

        # disable tags on mb
        res['d_tags'] = res['tags'] = ''


        # temporary hack to get isni
        # http://tickets.musicbrainz.org/browse/MBS-8762
        api_url = 'http://%s/ws/2/artist/%s/?fmt=xml&inc=%s' % (MUSICBRAINZ_HOST, provider_id, "+".join(inc))
        log.info('composed api url: %s' % api_url)
        r = requests.get(api_url)
        if r.status_code == 200:
            import xmltodict
            import json
            try:
                isni_code = json.loads(json.dumps(xmltodict.parse(r.text)))['metadata']['artist']['isni-list']['isni']
                if isinstance(isni_code, types.ListType):
                    res['isni_code'] = isni_code[0]
                else:
                    res['isni_code'] = isni_code
            except:
                pass


        return res


    def get_label(self, uri):

        provider_id = uri.split('/')[-1]
        inc = ('aliases', 'url-rels', 'annotation', 'tags',)
        api_url = 'http://%s/ws/2/label/%s/?fmt=json&inc=%s' % (MUSICBRAINZ_HOST, provider_id, "+".join(inc))

        log.info('composed api url: %s' % api_url)

        r = requests.get(api_url)

        if r.status_code == 404:
            return {'error': MUSICBRAINZ_404_MESSAGE}

        data= r.json()

        res = {}
        d_tags = []
        for k in data:

            mk = k
            if k == 'label-code':
                mk = 'labelcode'

            if k == 'annotation':
                mk = 'description'

            # wrong type-map
            if k == 'type':
                mk = '__unused__'

            if k == 'life-span':
                if 'begin' in data[k]:
                    res['date_start'] = data[k]['begin']

                if 'end' in data[k]:
                    res['date_end'] = data[k]['end']

            if k == 'parent_label':
                res['parent_0'] = data[k]['name']


            if k == 'relations':
                mapped = []
                for rel in data[k]:
                    if 'url' in rel:
                        mapped.append({
                            'uri': rel['url']['resource'],
                            'service': get_service_by_url(rel['url']['resource'], None),
                            })
                data[k] = mapped

            if k == 'tags':
                try:
                    d = data[k]
                    for v in d:
                        d_tags.append(v['name'])
                except:
                    pass

            res[mk] = data[k]

        if 'country' in res:
            try:
                c = Country.objects.get(iso2_code=res['country'])
            except:
                pass

        res['d_tags'] = ', '.join(d_tags)

        # disable tags on mb
        res['d_tags'] = res['tags'] = ''

        return res


    def get_media(self, uri):

        provider_id = uri.split('/')[-1]

        inc = ('aliases', 'url-rels', 'annotation', 'tags', 'artists', 'isrcs', 'artist-credits', 'artist-rels', 'work-rels')
        api_url = 'http://%s/ws/2/recording/%s/?fmt=json&inc=%s' % (MUSICBRAINZ_HOST, provider_id, "+".join(inc))

        log.info('composed api url: %s' % api_url)

        r = requests.get(api_url)

        if r.status_code == 404:
            return {'error': MUSICBRAINZ_404_MESSAGE}

        data= r.json()

        res = {}
        d_tags = []
        for k in data:
            mk = k
            if k == 'title':
                mk = 'name'

            if k == 'annotation':
                mk = 'description'

            # we just take the first isrc code..
            if k == 'isrcs' and len(data['isrcs']) > 0:
                res['isrc'] = data['isrcs'][0]

            if k == 'relations':
                mapped = []
                for rel in data[k]:
                    if 'url' in rel:
                        mapped.append({
                            'uri': rel['url']['resource'],
                            'service': get_service_by_url(rel['url']['resource'], None),
                            })
                data[k] = mapped

            if k == 'tags':
                try:
                    d = data[k]
                    for v in d:
                        d_tags.append(v['name'])
                except:
                    pass

            res[mk] = data[k]

        res['d_tags'] = ', '.join(d_tags)

        # TODO: implement artist mapping
        # res['artist_0'] = 'peter'

        # disable tags on mb
        res['d_tags'] = res['tags'] = ''


        return res




class DiscogsAPILookup(APILookup):
    """
    Musicbrainz API implementation
    """

    def get_data(self, uri=None):
        log.debug('run discogs lookup for %s - %s' % (self.obj, self.type))

        if not uri:
            uri = self.obj.relations.filter(service='discogs')[0].url
        log.debug('discogs uri: %s' % uri)

        # for consistency uri is handled in resp. method
        return getattr(self, 'get_%s' % self.type)(uri)


    def map_image(self, d):
        """
        hackish image mapping
        """
        image = None
        try:
            for v in d:
                if v['type'] == 'primary':
                    image = v['resource_url']
        except:
            pass

        # sorry, kind of ugly...
        if not image:
            try:
                for v in d:
                    if v['type'] == 'secondary':
                        image = v['resource_url']
            except:
                pass

        return image


    def reformat_name(self, name):
        """
        reformat discogs scheme names:
         - removes the number
         - repositions the 'The'
        e.g. "Tone Control Music, The (2)" becomes "The Tone Control Music"
        """

        p = ' \([0-9]+\)'
        name = re.sub(p, '', name)

        if name[-5:] == ', The':
            name = 'The %s' % name[:-5]
        if name[-4:] == ',The':
            name = 'The %s' % name[:-4]

        return name







    def get_release(self, uri):

        """
        discogs API releases url schema:
         - url: http://www.discogs.com/Miami-Nights-1984-Early-Summer/release/5015407
         - api: http://api.discgogs.com/releases/5015407
         for releases it is fine to just take the last bit
        """

        provider_id = uri.split('/')[-1]

        if '/release/' in uri:
            api_url = 'http://%s/releases/%s' % (DISCOGS_HOST, provider_id)

        if '/master/' in uri:
            api_url = 'http://%s/masters/%s' % (DISCOGS_HOST, provider_id)


        log.info('composed api url: %s' % api_url)

        r = requests.get(api_url)
        data= r.json()

        res = {}
        d_tags = []
        relations = []

        for k in data:

            mk = k

            #if k == 'title':
            #    mk = 'name'

            if k == 'title':
                # reformat numbering & 'The'
                res['name'] = self.reformat_name(data[k])

            if k == 'artists':
                reformated_artists = []
                for item in data['artists']:
                    if 'name' in item:
                        item['name'] = self.reformat_name(item['name'])
                        reformated_artists.append(item)
                res['artists'] = reformated_artists


            if k == 'notes':
                mk = 'description'

            if k == 'released_formatted':
                mk = 'releasedate_approx'

            if k == 'formats':
                try:
                    d = data[k]
                    if len(d[0]['descriptions']) > 1:
                        res['releasetype'] = d[0]['descriptions'][1]
                    else:
                        res['releasetype'] = d[0]['descriptions'][0]

                except:
                    pass


            if k == 'country':
                mk = 'release_country'

            if k == 'labels':
                try:
                    d = data[k][0]
                    res['label_0'] = self.reformat_name(d['name'])
                    res['catalognumber'] = d['catno']
                except:
                    pass


            # tagging
            if k == 'styles':
                try:
                    d = data[k]
                    for v in d:
                        d_tags.append(v)
                except:
                    pass

            if k == 'genres':
                try:
                    d = data[k]
                    for v in d:
                        d_tags.append(v)
                except:
                    pass


            if k == 'urls':
                mapped = []
                for rel in data[k]:
                    relations.append({
                        'uri': rel,
                        'service': get_service_by_url(rel, None),
                        })

            # image
            if k == 'images':
                res['remote_image'] = res['main_image'] = self.map_image(data[k])

            res[mk] = data[k]

        try:
            res['totaltracks'] = len(data['tracklist'])
        except:
            pass

        res['d_tags'] = ', '.join(d_tags)
        res['relations'] = relations

        # remap borgious countries
        try:
            if res['release_country'].upper() == 'UK':
                res['release_country'] = 'GB'
        except:
            pass


        # reformat tracklist
        res['tracklist'] = []
        for track in data['tracklist']:
            if 'artists' in track:
                try:
                    track['artists'][0]['name'] = self.reformat_name(track['artists'][0]['name'])
                except:
                    pass
            res['tracklist'].append(track)



        return res


    def get_artist(self, uri):

        """
        discogs API artists url schema:
         - url: http://www.discogs.com/artist/2693332-Miami-Nights-1984
         - api: http://api.discgogs.com/artists/2693332
         for artists, we neet to take the last bit, split it by '-' and use the first element
        """

        provider_id = uri.split('/')[-1].split('-')[0]
        api_url = 'http://%s/artists/%s' % (DISCOGS_HOST, provider_id)

        log.info('composed api url: %s' % api_url)

        r = requests.get(api_url)
        data= r.json()

        res = {}
        d_tags = [] # needed as merged from different keys
        relations = []

        for k in data:

            if k == 'profile':
                mk = 'biography'

            if k == 'realname':
                mk = 'real_name'

            if k == 'namevariations':
                res['namevariations'] = ', '.join(data[k])

            if k == 'name':
                # reformat numbering & 'The'
                res[k] = self.reformat_name(data[k])

            if k == 'urls':
                mapped = []
                for rel in data[k]:
                    relations.append({
                        'uri': rel,
                        'service': get_service_by_url(rel, None),
                        })

            if k == 'images':
                res['remote_image'] = res['main_image'] = self.map_image(data[k])

            try:
                if not mk in res:
                    res[mk] = data[k]
            except:
                pass


        res['d_tags'] = ', '.join(d_tags)
        res['relations'] = relations


        return res


    def get_label(self, uri):

        """
        discogs API labels url schema:
         - url: http://www.discogs.com/label/234260-Rosso-Corsa-Records
         - api: http://api.discgogs.com/labels/234260
         for labels, we neet to take the last bit, split it by '-' and use the first element
        """

        provider_id = uri.split('/')[-1].split('-')[0]
        api_url = 'http://%s/labels/%s' % (DISCOGS_HOST, provider_id)

        log.info('composed api url: %s' % api_url)

        r = requests.get(api_url)
        data= r.json()

        res = {}
        d_tags = [] # needed as merged from different keys
        relations = []


        for k in data:

            if k == 'name':
                res[k] = self.reformat_name(data[k])

            if k == 'profile':
                mk = 'description'

            if k == 'contact_info':
                mk = 'address'

            if k == 'parent_label':
                res['parent_0'] = self.reformat_name(data[k]['name'])

            if k == 'urls':
                mapped = []
                for rel in data[k]:
                    relations.append({
                        'uri': rel,
                        'service': get_service_by_url(rel, None),
                        })

            if k == 'images':
                res['remote_image'] = res['main_image'] = self.map_image(data[k])



            try:
                if not mk in res:
                    res[mk] = data[k]
            except:
                pass


        res['d_tags'] = ', '.join(d_tags)
        res['relations'] = relations

        return res



"""
function to call from 'outside'
"""
def get_from_provider(item_type, item_id, provider, api_url=None):

    log.debug('get_from_provider: %s - id: %s - provider: %s' % (item_type, item_id, provider))


    # get source object
    obj = None
    if item_type == 'release':
        obj = Release.objects.get(pk=item_id)

    if item_type == 'artist':
        obj = Artist.objects.get(pk=item_id)

    if item_type == 'media':
        obj = Media.objects.get(pk=item_id)

    if item_type == 'label':
        obj = Label.objects.get(pk=item_id)


    if obj and provider == 'musicbrainz':
        lookup = MusicbrainzAPILookup(obj=obj)
        return lookup.get_data(uri=api_url)

    if obj and provider == 'discogs':
        lookup = DiscogsAPILookup(obj=obj)
        return lookup.get_data(uri=api_url)



    log.debug('item to process: %s - %s' % (obj.pk, obj))

    return {}