# python
import re

# django
from urlparse import urlparse

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
import requests
from django.conf import settings

from settings import *
from l10n.models import Country
from jsonfield import JSONField
from alibrary.util.relations import get_service_by_url


# logging
import logging
log = logging.getLogger(__name__)


MUSICBRAINZ_HOST = getattr(settings, 'MUSICBRAINZ_HOST', 'musicbrainz.org')
DISCOGS_HOST = getattr(settings, 'DISCOGS_HOST', None)


################
from alibrary.models import *

USER_AGENT = 'ANORGDiscogsAPIClient/0.0.1 +http://anorg.net'


class APILookup(models.Model):
    
    PROVIDER_CHOICES = (
        (None, _('Not Set')),
        ('discogs', _('Discogs')),
        ('musicbrainz', _('Musicbrainz')),
    )
    provider = models.CharField(max_length=50, default=None, choices=PROVIDER_CHOICES)
    
    uri = models.URLField(blank=True, null=True)
    ressource_id = models.CharField(max_length=500, null=True, blank=True)
    
    api_data = JSONField(null=True, blank=True);
    

    PROCESSED_CHOICES = (
        (0, _('Waiting')),
        (1, _('Done')),
        (2, _('Error')),
    )
    processed = models.PositiveIntegerField(max_length=2, default=0, choices=PROCESSED_CHOICES)
    
    
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')


    # auto-update
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)
    
    # manager
    objects = models.Manager()

    # meta
    class Meta:
        app_label = 'alibrary'
        verbose_name = _('APILookup')
        verbose_name_plural = _('APILookups')
        ordering = ('created', )

    
    def __unicode__(self):
        return "%s - %s" % (self.provider, self.updated)


    def save(self, *args, **kwargs):

        super(APILookup, self).save(*args, **kwargs)
        
        
    """
    Generic wrapper - distributes to corresponding method
    """
    def get_from_api(self):

        log.debug('provider: %s' % self.provider)
        
        if self.provider == 'discogs':
            return self.get_from_discogs()

        if self.provider == 'musicbrainz':
            return self.get_from_musicbrainz()
        








    """
    Discogs wrapper - distribute to entities
    """
    def get_from_discogs(self):

        log.debug('content_object: %s' % self.content_object)

        self.uri = self.content_object.relations.filter(service='discogs')[0].url

        if '/release/' in self.uri:
            return self.get_release_from_discogs()

        if '/artist/' in self.uri:
            return self.get_artist_from_discogs()

        if '/label/' in self.uri:
            return self.get_label_from_discogs()




    """
    Muscicbrainz wrapper - distribute to entities
    """
    def get_from_musicbrainz(self):

        log.debug('content_object: %s' % self.content_object)

        try:
            self.uri = self.content_object.relations.filter(service='musicbrainz')[0].url
        except IndexError:
            return None

        if '/release/' in self.uri:
            return self.get_release_from_musicbrainz()

        if '/artist/' in self.uri:
            return self.get_artist_from_musicbrainz()

        if '/label/' in self.uri:
            return self.get_label_from_musicbrainz()

        if '/recording/' in self.uri:
            return self.get_media_from_musicbrainz()





    def get_artist_from_discogs(self):


        log.info('discogs artist uri: %s' % self.uri)


        # some hacks to convert site url to api id
        v1_id = self.uri.split('/')[-1]
        v1_url = 'http://%s/artist/%s?f=json' % (DISCOGS_HOST, v1_id)

        print 'mapping from v1 url:'
        print v1_url
        r = requests.get(v1_url)
        v1_data= r.json()

        d_id = v1_data['resp']['artist']['id']

        print 'extracted id: %s' % d_id


        #d_id = 8760

        # the v2 client
        from dgs2 import discogs_client
        discogs = discogs_client.Client(USER_AGENT)

        d_artist = discogs.artist(d_id)

        # strange... without print the dict is not loaded at all... so let's print!
        print d_artist




        res = {}
        d_tags = [] # needed as merged from different keys

        for k in d_artist.data:
            print k
            #print d_artist.data[k]

            # kind of ugly data mapping
            mk = k

            if k == 'profile':
                mk = 'biography'

            if k == 'realname':
                mk = 'real_name'

            if k == 'namevariations':
                res['namevariations'] = ', '.join(d_artist.data[k])


            if k == 'name':

                value = d_artist.data[k]
                # remove numbers from eg: My Artist (3)
                p = ' \([0-9]+\)'
                value = re.sub(p, '', value)

                # try to remap ", The"
                if value[-5:] == ', The':
                    value = 'The %s' % value[:-5]
                if value[-4:] == ',The':
                    value = 'The %s' % value[:-4]

                res[k] = value


            # image
            if k == 'images':
                image = None
                try:
                    d = d_artist.data[k]
                    for v in d:
                        if v['type'] == 'primary':
                            image = v['resource_url']
                        print v
                except:
                    pass

                # sorry, kind of ugly...
                if not image:
                    try:
                        d = d_artist.data[k]
                        for v in d:
                            if v['type'] == 'secondary':
                                image = v['resource_url']
                            print v
                    except:
                        pass

                try:
                    #res['remote_image'] = res['main_image'] = image.replace('api.discogs.com', 'dgs.anorg.net')
                    res['remote_image'] = res['main_image'] = image
                except:
                    res['remote_image'] = res['main_image'] = None
                #res['remote_image'] = 'http://dgs.anorg.net/image/R-5081-1147456810.jpeg'

            if not mk in res:
                res[mk] = d_artist.data[k]


        #res['d_tags'] = ', '.join(d_tags)
        self.api_data = res
        self.save()

        return res



    def get_release_from_discogs(self):

        log.info('uri: %s' % self.uri)
            
        try:
            ri = urlparse(self.uri).path
            ri = ri.split('/')
            ri = ri[-1:]
            ri = int(ri[0])
            
            self.ressource_id = ri
            log.info('ressource_id: %s' % self.ressource_id)
            
        except Exception, e:
            self.ressource_id = None
            log.warning('%s' % e)

        if not self.ressource_id:
            log.warning('no resource id for %s' % self.content_object)
        

        """
        Actual API requests
        """

        # the v1 client
        import discogs_client as discogs
        discogs.user_agent = USER_AGENT

        #d_release = discogs.Release(self.ressource_id).master
        #d_master = d_release.master
        #d_releasde = d_master.key_release
        
        # get discog's key-release from ressource id
        d_release = discogs.Release(self.ressource_id)
        
        # check if there is a master release
        """ don't do this, as makes errors in case oif wrongly assigned master release
        try:
            d_release = d_release.master.key_release
        except Exception, e:
            print e
        """
        
        """ release:
         |  artists
         |  credits
         |  labels
         |  master
         |  title
         |  tracklist
        """
        


        res = {}
        d_tags = [] # needed as merged from different keys

        for k in d_release.data:
            # print 'k: %s - v:%s' % (k, d_release.data[k])
            
            # kind of ugly data mapping
            mk = k
            if k == 'title':
                mk = 'name'

            if k == 'notes':
                mk = 'description'

            if k == 'released_formatted':
                mk = 'releasedate_approx'


            # try to extract format information
            if k == 'formats':
                try:
                    d = d_release.data[k]
                    res['releasetype'] = d[0]['descriptions'][0]
                except:
                    pass


            if k == 'country':
                mk = 'release_country'
                
            if k == 'labels':
                try:
                    d = d_release.data[k][0]
                    res['label_0'] = d['name']
                    res['catalognumber'] = d['catno']
                except:
                    pass


            # tagging
            if k == 'styles':
                try:
                    d = d_release.data[k]
                    for v in d:
                        d_tags.append(v)
                except:
                    pass

            if k == 'genres':
                try:
                    d = d_release.data[k]
                    for v in d:
                        d_tags.append(v)
                except:
                    pass

            # image
            if k == 'images':
                image = None
                try:
                    d = d_release.data[k]
                    for v in d:
                        if v['type'] == 'primary':
                            image = v['resource_url']
                        print v
                except:
                    pass

                # sorry, kind of ugly...
                if not image:
                    try:
                        d = d_release.data[k]
                        for v in d:
                            if v['type'] == 'secondary':
                                image = v['resource_url']
                            print v
                    except:
                        pass

                try:
                    if DISCOGS_HOST:
                        res['remote_image'] = res['main_image'] = image.replace('api.discogs.com', DISCOGS_HOST)
                    #res['remote_image'] = res['main_image'] = image.replace('api.discogs.com', 'dgs.anorg.net')
                    #res['remote_image'] = res['main_image'] = image
                except:
                    res['remote_image'] = res['main_image'] = None
                #res['remote_image'] = 'http://dgs.anorg.net/image/R-5081-1147456810.jpeg'




            res[mk] = d_release.data[k]

        print 'DTAGS:'
        print d_tags

        try:
            res['totaltracks'] = len(d_release.data['tracklist'])
        except:
            pass


        res['d_tags'] = ', '.join(d_tags)
        self.api_data = res
        self.save()
        
        return res





    def get_label_from_discogs(self):

        log.info('uri: %s' % self.uri)


        # some hacks to convert site url to api id
        v1_id = self.uri.split('/')[-1]
        v1_url = 'http://%s/label/%s?f=json' % (DISCOGS_HOST, v1_id)

        print "#########################################"
        print v1_url
        r = requests.get(v1_url)


        print r.status_code
        print r.text

        print
        print
        print
        print

        v1_data= r.json()

        d_id = v1_data['resp']['label']['id']


        #d_id = 8760

        # the v2 client
        from dgs2 import discogs_client
        discogs = discogs_client.Client(USER_AGENT)

        d_label = discogs.label(d_id)
        print '***********************'
        print d_label
        print '***********************'



        res = {}
        d_tags = [] # needed as merged from different keys

        for k in d_label.data:
            print k
            #print d_artist.data[k]

            # kind of ugly data mapping
            mk = k
            if k == 'title':
                mk = 'name'

            if k == 'profile':
                mk = 'description'

            if k == 'contact_info':
                mk = 'address'

            if k == 'parent_label':
                res['parent_0'] = d_label.data[k]['name']

            # image
            if k == 'images':
                image = None
                try:
                    d = d_label.data[k]
                    for v in d:
                        if v['type'] == 'primary':
                            image = v['resource_url']
                        print v
                except:
                    pass

                # sorry, kind of ugly...
                if not image:
                    try:
                        d = d_label.data[k]
                        for v in d:
                            if v['type'] == 'secondary':
                                image = v['resource_url']
                            print v
                    except:
                        pass

                try:
                    #res['remote_image'] = res['main_image'] = image.replace('api.discogs.com', 'dgs.anorg.net')
                    res['remote_image'] = res['main_image'] = image
                except:
                    res['remote_image'] = res['main_image'] = None

            res[mk] = d_label.data[k]

        self.api_data = res
        self.save()

        return res
    



        """
        Methods for Musicbrainz
        ------------------------------------------------------------
        """





    def get_release_from_musicbrainz(self):

        log.info('uri: %s' % self.uri)

        # some hacks to convert site url to api id
        id = self.uri.split('/')[-1]
        url = "http://%s/ws/2/release/%s?fmt=json&inc=aliases+url-rels+annotation+tags+artist-rels+recordings+artists+labels" % (MUSICBRAINZ_HOST, id)

        print url
        r = requests.get(url)
        data= r.json()

        res = {}
        d_tags = [] # needed as merged from different keys

        for k in data:
            print k

            # kind of ugly data mapping
            mk = k

            if k == 'annotation':
                mk = 'description'

            if k == 'title':
                mk = 'name'

            if k == 'country':
                mk = 'release_country'

            if k == 'date':
                mk = 'releasedate_approx'

            # wrong type-map
            """
            if k == 'type':
                mk = '__unused__'
            """

            if k == 'label-info':
                try:
                    print '*******************************************'
                    print data[k][0]

                    if 'label' in data[k][0] and 'name' in data[k][0]['label']:
                        res['label_0'] = data[k][0]['label']['name']

                    if 'catalog-number' in data[k][0]:
                        res['catalognumber'] = data[k][0]['catalog-number']

                except:
                    pass


            if k == 'relations':
                mapped = []
                for rel in data[k]:
                    if 'url' in rel:
                        #print rel['url']
                        #print get_service_by_url(rel['url'], None)
                        mapped.append({
                            'url': rel['url']['resource'],
                            'service': get_service_by_url(rel['url']['resource'], None),
                            })

                data[k] = mapped





            if k == 'media':
                mapped = []
                # initials
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




            # tagging
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
                #res['release_country'] = c.pk
            except:
                pass



        # try to get cover-art
        try:
            url = 'http://coverartarchive.org/release/%s' % id
            r = requests.get(url)
            if r.ok:
                res['main_image'] = r.json()['images'][0]['image']
                res['remote_image'] = r.json()['images'][0]['image']
        except:
            pass



        print 'DTAGS:'
        print d_tags

        res['d_tags'] = ', '.join(d_tags)

        self.api_data = res
        self.save()

        return res





    def get_artist_from_musicbrainz(self):

        log.info('uri: %s' % self.uri)


        # TODO: make more dynamic...
        # some hacks to convert site url to api id
        id = self.uri.split('/')[-1]
        url = "http://%s/ws/2/artist/%s?fmt=json&inc=aliases+url-rels+annotation+tags+artist-rels" % (MUSICBRAINZ_HOST, id)

        print "#########################################"
        print url
        r = requests.get(url)
        data= r.json()

        #print data

        res = {}
        d_tags = [] # needed as merged from different keys

        for k in data:
            print k

            # kind of ugly data mapping
            mk = k

            if k == 'annotation':
                mk = 'description'

            # wrong type-map
            """
            if k == 'type':
                mk = '__unused__'
            """

            if k == 'life-span':
                if 'begin' in data[k]:
                    res['date_start'] = data[k]['begin']

                if 'end' in data[k]:
                    res['date_end'] = data[k]['end']




            if k == 'relations':
                mapped = []
                for rel in data[k]:
                    if 'url' in rel:
                        #print rel['url']
                        #print get_service_by_url(rel['url'], None)
                        mapped.append({
                            'url': rel['url']['resource'],
                            'service': get_service_by_url(rel['url']['resource'], None),
                            })

                data[k] = mapped



            # tagging
            if k == 'tags':
                try:
                    d = data[k]
                    for v in d:
                        d_tags.append(v['name'])
                except:
                    pass

            res[mk] = data[k]

        # try to remap country
        if 'country' in res:

            pass
            """
            try:
                c = Country.objects.get(iso2_code=res['country'])
                res['country'] = c.pk
            except:
                pass
            """

        print 'DTAGS:'
        print d_tags

        res['d_tags'] = ', '.join(d_tags)

        self.api_data = res
        self.save()

        return res


    def get_media_from_musicbrainz(self):

        log.info('uri: %s' % self.uri)


        # TODO: make more dynamic...
        # some hacks to convert site url to api id
        id = self.uri.split('/')[-1]
        #url = "http://%s/ws/2/recording/%s?fmt=json&inc=aliases+url-rels+annotation+tags+artists+isrcs+artist-credits+work-rels+work-level-rels" % (MUSICBRAINZ_HOST, id)
        url = "http://%s/ws/2/recording/%s?fmt=json&inc=aliases+url-rels+annotation+tags+artists+isrcs+artist-credits+artist-rels+work-rels" % (MUSICBRAINZ_HOST, id)

        print "#########################################"
        print url
        r = requests.get(url)
        data= r.json()

        print data

        res = {}
        d_tags = [] # needed as merged from different keys

        for k in data:
            print k

            # kind of ugly data mapping
            mk = k

            if k == 'title':
                mk = 'name'

            if k == 'annotation':
                mk = 'description'

            # wrong type-map
            """
            if k == 'type':
                mk = '__unused__'
            """


            # we just take the first isrc code..
            if k == 'isrcs' and len(data['isrcs']) > 0:
                res['isrc'] = data['isrcs'][0]



            if k == 'relations':
                mapped = []
                for rel in data[k]:
                    if 'url' in rel:
                        #print rel['url']
                        #print get_service_by_url(rel['url'], None)
                        mapped.append({
                            'url': rel['url']['resource'],
                            'service': get_service_by_url(rel['url']['resource'], None),
                            })

                data[k] = mapped

            # tagging
            if k == 'tags':
                try:
                    d = data[k]
                    for v in d:
                        d_tags.append(v['name'])
                except:
                    pass

            res[mk] = data[k]

        # try to remap country
        if 'country' in res:
            try:
                c = Country.objects.get(iso2_code=res['country'])
                res['country'] = c.pk
            except:
                pass

        print 'DTAGS:'
        print d_tags

        res['d_tags'] = ', '.join(d_tags)

        self.api_data = res
        self.save()

        return res





    def get_label_from_musicbrainz(self):

        log.info('uri: %s' % self.uri)


        # TODO: make more dynamic...
        # some hacks to convert site url to api id
        id = self.uri.split('/')[-1]
        url = "http://%s/ws/2/label/%s?fmt=json&inc=aliases+url-rels+annotation+tags+label-rels" % (MUSICBRAINZ_HOST, id)

        print "#########################################"
        print url
        r = requests.get(url)
        data= r.json()

        print data

        res = {}
        d_tags = [] # needed as merged from different keys

        for k in data:
            print k
            #print d_artist.data[k]

            # kind of ugly data mapping
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
                            'url': rel['url']['resource'],
                            'service': get_service_by_url(rel['url']['resource'], None),
                            })

                data[k] = mapped

            # tagging
            if k == 'tags':
                try:
                    d = data[k]
                    for v in d:
                        d_tags.append(v['name'])
                except:
                    pass

            res[mk] = data[k]

        # try to remap country
        if 'country' in res:
            try:
                c = Country.objects.get(iso2_code=res['country'])
                #res['country'] = c.pk
            except:
                pass




        print 'DTAGS:'
        print d_tags

        res['d_tags'] = ', '.join(d_tags)

        self.api_data = res
        self.save()

        return res
