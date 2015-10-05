import pprint
import logging

import musicbrainzngs
from obp_legacy.models import *
from spf.models import Match
log = logging.getLogger(__name__)


class MediaMatch(object):

    def __init__(self):
        log = logging.getLogger('util.migrator.__init__')
        musicbrainzngs.set_useragent("Example music app", "0.1", "http://example.com/music")
        #musicbrainzngs.set_hostname("mb.anorg.net")
        #musicbrainzngs.set_rate_limit(limit_or_interval=False)
        self.pp = pprint.PrettyPrinter(indent=4)
        #self.pp.pprint = lambda d: None


    def match(self, obj):

        log = logging.getLogger('util.match.match')
        log.info('matching: %s' % obj.title)

        for r in obj.results_mb:
            print '--'
            #print r

            mb_id = r['id']
            print mb_id

            match, created = Match.objects.get_or_create(request=obj, mb_id=mb_id)

            includes = [
                'artists',
                'releases',
                'artist-credits',
                'release-rels',
                'release-group-rels',
                'artist-rels',
                'annotation',
                'discids',
                'label-rels',
                'work-rels',
                'recording-rels',
                'media',
                'isrcs',
                ]


            try:

                mr = musicbrainzngs.get_recording_by_id(id=mb_id, includes=includes)
                mr = mr['recording']

                # self.pp.pprint(mr)

                match.title = mr['title']

                # match data as json
                match.results_mb = mr

                match.artist = mr['artist-credit-phrase']


                if 'length' in mr:
                    match.duration = mr['length']


                # compose cretits string
                if 'artist-credit' in mr:
                    credits = ''
                    for c in mr['artist-credit']:

                        try:
                            astr = c['artist']['name']
                            credits += astr + "\n"
                        except:
                            pass
                    match.artist_credits = credits

                # compose secondary cretits string
                if 'artist-relation-list' in mr:
                    credits = ''
                    for c in mr['artist-relation-list']:

                        try:
                            astr = c['artist']['name']

                            astr = '%s - [%s: %s]' % (astr, c['type'], ', '.join(c['attribute-list']))

                            credits += astr + "\n"
                        except Exception, e:
                            print e
                            pass

                    match.artist_credits_secondary = credits

                if 'isrc-list' in mr:
                    self.pp.pprint(mr['isrc-list'])

                    try:
                        isrcs = "\n".join(mr['isrc-list'])
                        match.isrc_list = isrcs
                    except Exception, e:
                        print e
                        pass


                # compose release string
                if 'release-list' in mr:
                    releases = ''
                    for r in mr['release-list']:

                        """
                        print '*******************************'
                        self.pp.pprint(r)
                        print '*******************************'
                        """

                        includes = ['labels','release-rels', 'work-rels']




                        #mr = mr['recording']

                        try:
                            pass
                        except:
                            pass

                        try:
                            rstr = r['title']

                            rstr = '%s - [%s | %s]' % (rstr, r['country'], r['date'])



                            if 'medium-list' in r:
                                try:
                                    rstr += ' - %s - Track# %s' % (r['medium-list'][0]['format'], r['medium-list'][0]['track-list'][0]['number'])
                                except:
                                    pass


                            try:

                                tstr = ''

                                if 'label-info-list' in mrel:
                                    lil = mrel['label-info-list'][0]
                                    self.pp.pprint(lil)


                                    if 'label' in lil:
                                        tstr += ' %s ' % lil['label']['name']

                                        if 'label-code' in lil['label']:
                                            tstr += '(%s) ' % lil['label']['label-code']


                                    if 'catalog-number' in lil:
                                        tstr += 'catno: %s' % lil['catalog-number']



                                print '****'
                                print tstr

                                rstr += ' [ ' + tstr + ' ] '

                            except Exception, e:
                                print e
                                pass



                            try:
                                mrel = musicbrainzngs.get_release_by_id(id=r['id'], includes=includes)
                                mrel = mrel['release']
                                # self.pp.pprint(mrel)

                                rstr += ' [barcode: %s]' % (mrel['barcode'])


                            except:
                                pass




                            releases += rstr + "\n"
                        except Exception, e:
                            print e
                            pass

                    match.release_list = releases

                # compose release string
                if 'work-relation-list' in mr:
                    try:
                        iswcs = "\n".join(mr['work-relation-list'][0]['work']['iswc-list'])
                        match.iswc_list = iswcs
                    except:
                        pass

                match.status = 1

            except Exception, e:
                print 'GOT ERROR!!!: '
                print e
                print

                match.status = 99


            match.save()










