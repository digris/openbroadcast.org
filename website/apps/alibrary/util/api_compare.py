import logging
import requests
import re
from django.conf import settings
from l10n.models import Country

from alibrary.models import Release, Label, Artist, Media
from alibrary.util.relations import get_service_by_url

log = logging.getLogger(__name__)

MUSICBRAINZ_HOST = getattr(settings, 'MUSICBRAINZ_HOST', None)
DISCOGS_HOST = getattr(settings, 'DISCOGS_HOST', None)

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
        inc = ('aliases', 'url-rels', 'annotation', 'tags', 'artist-rels', 'recordings', 'artists', 'labels', 'release-groups')
        api_url = 'http://%s/ws/2/release/%s/?fmt=json&inc=%s' % (MUSICBRAINZ_HOST, provider_id, "+".join(inc))

        log.info('composed api url: %s' % api_url)

        r = requests.get(api_url)
        data= r.json()

        # data mapping
        res = {}
        d_tags = []
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
                mapped = []
                pos = 1
                disc = 1
                for disc in data[k]:
                    for m in disc['tracks']:
                        mapped.append({
                            'position': '%s-%s' % (disc, pos),
                            'duration': m['length'],
                            'title': m['title'],
                            })

                #res['tracklist'] = mapped


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
            print data['media'][0]['track-count']
            for x in data['media']:
                num_tracks += int(x['track-count'])
            res['totaltracks'] = num_tracks if num_tracks > 0 else None
        except:
            pass

        res['d_tags'] = ', '.join(d_tags)

        return res


    def get_artist(self, uri):

        provider_id = uri.split('/')[-1]
        inc = ('aliases', 'url-rels', 'annotation', 'tags', 'artist-rels')
        api_url = 'http://%s/ws/2/artist/%s/?fmt=json&inc=%s' % (MUSICBRAINZ_HOST, provider_id, "+".join(inc))

        log.info('composed api url: %s' % api_url)

        r = requests.get(api_url)
        data= r.json()

        # data mapping
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

            if k == 'tags':
                try:
                    d = data[k]
                    for v in d:
                        d_tags.append(v['name'])
                except:
                    pass

            res[mk] = data[k]

        res['d_tags'] = ', '.join(d_tags)

        return res


    def get_label(self, uri):

        provider_id = uri.split('/')[-1]
        inc = ('aliases', 'url-rels', 'annotation', 'tags',)
        api_url = 'http://%s/ws/2/label/%s/?fmt=json&inc=%s' % (MUSICBRAINZ_HOST, provider_id, "+".join(inc))

        log.info('composed api url: %s' % api_url)

        r = requests.get(api_url)
        data= r.json()


        # data mapping
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

        return res


    def get_media(self, uri):

        provider_id = uri.split('/')[-1]

        inc = ('aliases', 'url-rels', 'annotation', 'tags', 'artists', 'isrcs', 'artist-credits', 'artist-rels', 'work-rels')
        api_url = 'http://%s/ws/2/recording/%s/?fmt=json&inc=%s' % (MUSICBRAINZ_HOST, provider_id, "+".join(inc))

        log.info('composed api url: %s' % api_url)

        r = requests.get(api_url)
        data= r.json()

        # data mapping
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
                print v
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
            if k == 'title':
                mk = 'name'

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
                    res['label_0'] = d['name']
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

                value = data[k]
                # remove numbers from eg: My Artist (3)
                p = ' \([0-9]+\)'
                value = re.sub(p, '', value)

                # try to remap ", The"
                if value[-5:] == ', The':
                    value = 'The %s' % value[:-5]
                if value[-4:] == ',The':
                    value = 'The %s' % value[:-4]

                res[k] = value


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
                mk = 'name'

            if k == 'profile':
                mk = 'description'

            if k == 'contact_info':
                mk = 'address'

            if k == 'parent_label':
                res['parent_0'] = data[k]['name']

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


    if api_url:
        print '//////////////////////////////////////////'
        print api_url


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