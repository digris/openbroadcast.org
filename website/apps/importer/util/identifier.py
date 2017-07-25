# -*- coding: utf-8 -*-
import os
import re
import locale
import pprint
import logging
from mutagen import File as MutagenFile
from mutagen.easyid3 import EasyID3
from mutagen.easymp4 import EasyMP4
from django.conf import settings
import acoustid
import requests
import musicbrainzngs
from lib.util.sha1 import sha1_by_file
from importer.util.tools import discogs_image_by_url
from base.audio.echoprint import echoprint_from_path

log = logging.getLogger(__name__)

AC_API_KEY = getattr(settings, 'AC_API_KEY', 'ZHKcJyyV')
MUSICBRAINZ_HOST = getattr(settings, 'MUSICBRAINZ_HOST', None)
MUSICBRAINZ_RATE_LIMIT = getattr(settings, 'MUSICBRAINZ_RATE_LIMIT', True)

LIMIT_AID_RESULTS = 6
AID_MIN_SCORE = 0.9
LIMIT_MB_RELEASES = 12
LIMIT_EQUAL_NAMES = 7

METADATA_SET = {
                # media
                'obp_media_uuid': None,
                'media_name': None,
                'media_mb_id': None,
                'media_tracknumber': None,
                'media_totaltracks': None,
                # artist
                'artist_name': None,
                'artist_mb_id': None,
                'performer_name': None,
                # release
                'release_name': None,
                'release_mb_id': None,
                'release_date': None,
                'release_releasecountry': None,
                'release_catalognumber': None,
                'release_type': None,
                'release_status': None,
                # label
                'label_name': None,
                'label_mb_id': None,
                'label_code': None,
                # disc
                'disc_number': None,
                # media mixed
                'media_genres' : [],
                'media_tags' : [],
                'media_copyright': None,
                'media_comment': None,
                'media_bpm': None,
                }

class Identifier(object):


    def __init__(self):

        musicbrainzngs.set_useragent("NRG Processor", "0.01", "http://anorg.net/")
        musicbrainzngs.set_rate_limit(MUSICBRAINZ_RATE_LIMIT)

        self.pp = pprint.PrettyPrinter(indent=4)
        self.pp.pprint = lambda d: None

        self.file_metadata = None

        if MUSICBRAINZ_HOST:
            musicbrainzngs.set_hostname(MUSICBRAINZ_HOST)

    """
    look for a duplicate by sha1
    """
    def id_by_sha1(self, file):

        sha1 = sha1_by_file(file)
        log.debug(u'generated SHA1 %s for %s' % (sha1, file))

        from alibrary.models import Media
        duplicates = Media.objects.filter(master_sha1=sha1)
        if duplicates.exists():
            log.info(u'detected duplicate by SHA1 hash. pk is: %s' % duplicates[0].pk)
            return duplicates[0].pk
        else:
            log.debug(u'no duplicate by SHA1 hash.')
            return None


    """
    look for a duplicate by metadata
    """
    def id_by_metadata(self, file):

        from alibrary.models.mediamodels import Media

        try:
            metadata = self.extract_metadata(file)
        except:
            metadata = None


        if not metadata:
            return

        try:

            if 'media_mb_id' in metadata and metadata['media_mb_id']:
                # don't check for duplicates by name if musicbrainz id available
                return


            if 'performer_name' in metadata and 'media_name' in metadata and 'release_name' in metadata:

                # TODO: make this matching more inteligent!

                qs = Media.objects.filter(
                    name__istartswith=metadata['media_name'][0:8],
                    artist__name__istartswith=metadata['performer_name'][0:8]
                )

                if not qs.exists():
                    qs = Media.objects.filter(
                        name__istartswith=metadata['media_name'][0:8],
                        release__name__istartswith=metadata['release_name'][0:8]
                    )

                if qs.exists():
                    return qs[0].pk

        except:
            pass



    """
    look for a duplicate by fingerprint
    """
    def id_by_echoprint(self, file):


        from ep.API import fp

        code, version, duration, echoprint = echoprint_from_path(file.path, offset=10, duration=100)

        try:
            res = fp.best_match_for_query(code_string=code)

            if res.match():
                log.info('echoprint match - score: %s trid: %s' % (res.score, res.TRID))
                return int(res.TRID)

        except Exception as e:
            log.warning('echoprint error: %s' % (e))


        return None


    def extract_metadata(self, file):


        if self.file_metadata:
            return self.file_metadata

        log.info('Extracting metadata for: %s' % (file.path))

        enc = locale.getpreferredencoding()


        meta = None
        ext = os.path.splitext(file.path)[1]
        log.debug('detected %s as extension' % ext)

        if ext:
            ext = ext.lower()

        if ext == '.mp3':
            try:
                meta = EasyID3(file.path)
            except Exception as e:
                log.debug('unable to process MP3')

        if ext in ['.mp4', '.m4a']:
            try:
                meta = EasyMP4(file.path)
            except Exception as e:
                log.debug('unable to process M4A')


        if not meta:
            try:
                meta = MutagenFile(file.path)
                log.debug('using MutagenFile')
            except Exception as e:
                log.warning('even unable to open file with straight mutagen: %s' % e)




        dataset = dict(METADATA_SET)

        # try to get obp identifyer
        try:
            from mutagen.id3 import ID3
            id3 = ID3(file.path)
            obp_media_uuid = id3["UFID:http://openbroadcast.org"].data.decode('ascii')
            if obp_media_uuid:
                dataset['obp_media_uuid'] = obp_media_uuid
        except:
            pass




        # Media
        try:
            dataset['media_name'] = meta['title'][0]
        except Exception as e:
            log.info('metadata missing "media_name": %s' % (e))

        try:
            dataset['media_mb_id'] = meta['musicbrainz_trackid'][0]
        except Exception as e:
            log.debug('metadata missing "media_mb_id": %s' % (e))

        try:

            try:
                dataset['media_tracknumber'] = int(meta['tracknumber'][0])
            except Exception as e:
                try:
                    dataset['media_tracknumber'] = int(meta['tracknumber'][0].split('/')[0])
                except Exception as e:
                    pass
                log.debug('metadata missing "media_tracknumber": %s' % (e))

            try:
                tn = meta['tracknumber'][0].split('/')
                dataset['media_tracknumber'] = int(tn[0])
                dataset['media_totaltracks'] = int(tn[1])

            except Exception as e:
                pass

        except Exception as e:
            log.debug('unable to extract tracknumber from metadata')


        # try to extract tracknumber from filename
        if 'media_tracknumber' in dataset and not dataset['media_tracknumber']:

            t_num = None

            path, filename = os.path.split(file.path)
            log.info('Looking for number in filename: %s' % filename)


            match = re.search("\A\d+", filename)

            try:
                if match:
                    t_num = int(match.group(0))
            except:
                pass

            dataset['media_tracknumber'] = t_num


        # Artist
        try:
            dataset['artist_name'] = meta['artist'][0]
        except Exception as e:
            pass


        try:
            # mutagen metadata contains '/' separated ids for mp3, while a list for flac
            # so we join by '/' to get an unified way.
            # the opposite would actually be better, but also would require a lot of refactoring...
            # so a TODO: fix this at some point of time...
            dataset['artist_mb_id'] = '/'.join(meta['musicbrainz_artistid'])

        except Exception as e:
            pass

        try:
            dataset['performer_name'] = meta['performer'][0]
        except Exception as e:
            pass



        # Release
        try:
            dataset['release_name'] = meta['album'][0]
        except Exception as e:
            #print e
            pass

        try:
            dataset['release_mb_id'] = meta['musicbrainz_albumid'][0]
        except Exception as e:
            #print e
            pass

        try:
            dataset['release_date'] = meta['date'][0]
        except Exception as e:
            #print e
            pass

        try:
            dataset['release_releasecountry'] = meta['releasecountry'][0]
        except Exception as e:
            #print e
            pass

        try:
            dataset['release_status'] = meta['musicbrainz_albumstatus'][0]
        except Exception as e:
            #print e
            pass



         # Label
        try:
            try:
                dataset['label_name'] = meta['organization'][0]
            except Exception as e:
                #print e
                pass

            try:
                dataset['label_name'] = meta['label'][0]
            except Exception as e:
                #print e
                pass

        except Exception as e:
            #print e
            pass


        try:
            dataset['label_code'] = meta['labelno'][0]
        except Exception as e:
            #print e
            pass



        # Misc
        try:
            dataset['media_copyright'] = meta['copyright'][0]
        except Exception as e:
            #print e
            pass

        try:
            dataset['media_comment'] = meta['comment'][0]
        except Exception as e:
            #print e
            pass

        try:
            dataset['media_bpm'] = meta['bpm'][0]
        except Exception as e:
            #print e
            pass


        """
        hacks to prevent some mutagen bugs:
         - https://bitbucket.org/lazka/mutagen/issues/215/mutageneasyid3easyid3keyerror
         - https://dev.sourcefabric.org/browse/CC-6035
        """
        if meta:

            for k in meta:

                if k == 'replaygain_SeratoGain_gain':
                    del(meta[k])

                if k == 'replaygain_SeratoGain_peak':
                    del(meta[k])

                if k[0:13] == 'PRIV:TRAKTOR4':
                    del(meta[k])


        self.file_metadata = dataset

        return dataset

    """
    acoustid lookup
    returns musicbrainz "recording" ids
    """
    def get_aid(self, file):

        log.info('lookup acoustid for: %s' % (file.path))

        try:

            data = acoustid.match(AC_API_KEY, file.path)

            res = []
            i = 0
            for d in data:
                selected = False
                if i == 0:
                    selected = True
                t = {
                     'score': d[0],
                     'id': d[1],
                     'selected': selected,
                     }


                if i < LIMIT_AID_RESULTS:
                    log.debug('acoustid: got result (loop: %s) - score: %s | mb id: %s' % (i, d[0], d[1]))
                    if i < 1:
                        res.append(t)
                    else:
                        # only append further releases if score is high enough
                        if float(d[0]) > AID_MIN_SCORE:
                            res.append(t)
                        else:
                            log.debug('skipping acoustid, score %s < %s (AID_MIN_SCORE)' % (float(d[0]), AID_MIN_SCORE))

                else:
                    pass
                    #log.debug('skipping acoustid, we have %s of them' % i)
                i += 1

            log.info('got %s possible matches via acoustid' % len(res))


            return res

        except:
            return None


    def get_musicbrainz(self, obj):

        log.info('Lookup musicbrainz for importfile id: %s' % obj.pk)

        """
        trying to get the tracknumber
        """
        tracknumber = None
        releasedate = None

        """
        try loading settings
        """
        skip_tracknumber = obj.settings.get('skip_tracknumber', False)

        try:
            tracknumber = obj.results_tag['media_tracknumber']
            log.debug('tracknumber from metadata: %s' % tracknumber)
        except Exception as e:
            log.debug('no tracknumber in metadata')

        try:
            releasedate = obj.results_tag['release_date']
            log.debug('releasedate from metadata: %s' % releasedate)
        except Exception as e:
            log.debug('no releasedate in metadata')


        """
         - loop recording ids
         - query by it and tracknumber (if available)
         - sort releases by date
         
        release entry looks as following:
         
        {
            id: "12a0eabc-28ee-3ac6-834d-390861f0f20c",
            title: "Live!",
            status: "Official",
            release-group: {
                id: "90eb5951-1225-35bc-9ef0-0845ac3c81aa",
                primary-type: "Album",
                secondary-types: [
                    "Live"
                ]
            },
            date: "1995",
            country: "GB",
            track-count: 30,
            media: [
                {
                    position: 2,
                    format: "CD",
                    track: [
                        {
                            number: "3",
                            title: "Walking in Your Footsteps",
                            length: 295000
                        }
                    ],
                    track-count: 15,
                    track-offset: 2
                }
            ]
        }
        
        """
        releases = []
        for e in obj.results_acoustid:
            recording_id = e['id']
            log.info('recording mb_id: %s' % recording_id)

            """
            search query e.g.:
            http://www.musicbrainz.org/ws/2/recording/?query=rid:1e701b4e-2b6e-4509-af29-b8df2cdc8225%20AND%20number:3&fmt=json
            """

            url = 'http://%s/ws/2/recording/?fmt=json&query=rid:%s' % (MUSICBRAINZ_HOST, recording_id)

            if tracknumber and not skip_tracknumber:
                url = '%s%s%s' % (url, '%20AND%20number:', tracknumber)


            #mdata = MutagenFile(obj.file.path)
            #qdur = (float(mdata.info.length * 1000) / 2000.0)
            #print 'QDUR: %s' % qdur
            #url = '%s%s%s' % (url, '%20AND%20qdur:', qdur)



            """    
            if releasedate:
                url = '%s%s%s' % (url, '%20AND%20date:', releasedate)
            """

            log.debug('API url for request: %s' % url)
            r = requests.get(url, timeout=5)
            result = r.json()

            if 'recordings' in result:

                log.info('recording on API mb_id: %s' % recording_id)
                if len(result['recordings']) > 0:

                    if 'releases' in result['recordings'][0]:

                        log.info('got releases on api: %s' % len(result['recordings'][0]['releases']))

                        """
                        fix missing dates
                        """
                        for r in result['recordings'][0]['releases']:
                            # dummy-date - sorry, none comes first else.
                            if 'date' not in r:
                                r['date'] = '9999'


                        """
                        try to get the first one, by date
                        """
                        try:
                            sorted_releases = sorted(result['recordings'][0]['releases'], key=lambda k: k['date'])
                            release = sorted_releases[0]
                            log.debug('Sorting OK!')
                            # reset dummy-date
                            if release['date'] == '9999':
                                release['date'] = None
                            log.info('First Date: %s' % release['date'])

                        except Exception as e:
                            log.warning('Unable to sort by date: %s' % e)
                            sorted_releases = result['recordings'][0]['releases']

                        #sorted_releases = result['recording'][0]['releases']




                        """
                        1. implementation
                        pull out a selection of gathered releases.
                        basically we limit releases with equal names
                        """

                        """
                        selected_releases = []
                        if len(sorted_releases) > 1:
                            # get releases with unique name
                            count = 0
                            current_names = []
                            for t_rel in sorted_releases:
                                if (not t_rel['title'] in current_names and count < LIMIT_MB_RELEASES):
                                    log.debug('adding new release name to results: %s' % t_rel['title'])
                                    current_names.append(t_rel['title'])
                                    selected_releases.append(t_rel)
                                    count += 1
                                else:
                                    pass
                                    #log.debug('release name already in results: %s' % t_rel['title'])

                        else:
                            selected_releases.append(sorted_releases[0])
                        """


                        """
                        2. implementation
                        pull out a selection of gathered releases.
                        basically we limit releases with equal names
                        """
                        selected_releases = []

                        if len(sorted_releases) > 1:
                            named_releases = {}
                            for t_rel in sorted_releases:
                                if (not t_rel['title'] in named_releases):
                                    named_releases[t_rel['title']] = []
                                    named_releases[t_rel['title']].append(t_rel)
                                    #log.debug('adding new release name: "%s"' % t_rel['title'])
                                else:
                                    named_releases[t_rel['title']].append(t_rel)
                                    #log.debug('appending to existing: "%s"' % t_rel['title'])

                            for k, v in named_releases.iteritems():
                                #log.debug('got %s releases for "%s"' % (len(v), k))
                                selected_releases += v[0:LIMIT_EQUAL_NAMES]

                            #selected_releases.append(sorted_releases[0])

                        else:
                            selected_releases.append(sorted_releases[0])






                        for selected_release in selected_releases:

                            selected_release['artist'] = result['recordings'][0]['artist-credit'][0]['artist']
                            selected_release['recording'] = result['recordings'][0]
                            try:
                                selected_release['recordings']['releases'] = None
                            except Exception as e:
                                pass
                                #print e

                            releases.append(selected_release)

        # TODO: think about limits
        releases = releases[0:LIMIT_MB_RELEASES]

        if len(releases) > 0:
            releases = self.complete_releases(releases)
            releases = self.format_releases(releases)

        return releases




    def complete_releases(self, releases):

        log.info('got %s releases to complete' % len(releases))

        completed_releases = []

        for release in releases:
            if release['id'] in completed_releases:
                log.debug('already completed release with id: %s' % release['id'])
                releases.remove(release)

            else:
                log.debug('complete release with id: %s' % release['id'])

                r_id = release['id']
                rg_id = release['release-group']['id']

                #print 'r_id: %s' % r_id
                #print 'rg_id: %s' % rg_id


                release['label'] = None
                release['catalog-number'] = None
                release['discogs_url'] = None
                release['discogs_master_url'] = None
                release['discogs_image'] = None


                """
                get release details
                """
                inc = ('labels', 'artists', 'url-rels', 'label-rels',)
                url = 'http://%s/ws/2/release/%s/?fmt=json&inc=%s' % (MUSICBRAINZ_HOST, r_id, "+".join(inc))

                r = requests.get(url, timeout=5)
                result = r.json()
                #self.pp.pprint(result)

                # only apply label info if unique
                if 'label-info' in result and len(result['label-info']) == 1:
                    if 'label' in result['label-info'][0]:
                        release['label'] = result['label-info'][0]['label']
                    if 'catalog-number' in result['label-info'][0]:
                        release['catalog-number'] = result['label-info'][0]['catalog-number']

                # try to get discogs url
                if 'relations' in result:
                    for relation in result['relations']:
                        if relation['type'] == 'discogs':
                            log.debug('got discogs url from release: %s' % relation['url'])
                            release['discogs_url'] = relation['url']['resource']



                """
                get release-group details
                """
                inc = ('url-rels',)
                url = 'http://%s/ws/2/release-group/%s/?fmt=json&inc=%s' % (MUSICBRAINZ_HOST, rg_id, "+".join(inc))

                r = requests.get(url, timeout=5)
                result = r.json()
                #self.pp.pprint(result)

                # try to get discogs master-url
                if 'relations' in result:
                    for relation in result['relations']:
                        if relation['type'] == 'discogs':
                            log.debug('got discogs url from release: %s' % relation['url'])
                            release['discogs_master_url'] = relation['url']['resource']




                """
                assign cover image (if available)
                """
                if release['discogs_url']:
                    try:
                        release['discogs_image'] = discogs_image_by_url(release['discogs_url'], 'uri150')
                    except:
                        pass

                if not release['discogs_image']:
                    try:
                        release['discogs_image'] = discogs_image_by_url(release['discogs_master_url'], 'uri150')
                    except:
                        pass
                """
                finally try to get image from coverartarchive.org
                """
                if not release['discogs_image']:
                    url = 'http://coverartarchive.org/release/%s' % r_id
                    try:
                        r = requests.get(url, timeout=5)
                        result = r.json()
                        release['discogs_image'] = result['images'][0]['image']
                    except:
                        pass



                completed_releases.append(release['id'])



        return releases


    """
    formatting method, to have easy to use variables on client side
    """
    def format_releases(self, releases):

        log.info('got %s releases to format' % len(releases))

        formatted_releases = []

        completed_releases = []


        for release in releases:

            if release['id'] in completed_releases:
                log.debug('already formated release with id: %s' % release['id'])

            else:

                log.debug('formating release with id: %s' % release['id'])
                completed_releases.append(release['id'])

                self.pp.pprint(release)

                # release
                r = {}
                r['mb_id'] = None
                r['name'] = None
                r['status'] = None
                r['releasedate'] = None
                r['catalognumber'] = None
                r['country'] = None
                r['asin'] = None
                r['barcode'] = None

                if 'id' in release:
                    r['mb_id'] = release['id']

                if 'title' in release:
                    r['name'] = release['title']

                if 'status' in release:
                    r['status'] = release['status']

                if 'date' in release:
                    r['releasedate'] = release['date']

                if 'country' in release:
                    r['country'] = release['country']

                if 'catalog-number' in release:
                    r['catalognumber'] = release['catalog-number']


                # media
                m = {}
                m['mb_id'] = None
                m['name'] = None
                m['duration'] = None

                if 'recording' in release and release['recording']:

                    if 'title' in release['recording']:
                        m['name'] = release['recording']['title']

                    if 'id' in release['recording']:
                        m['mb_id'] = release['recording']['id']

                    if 'length' in release['recording']:
                        m['duration'] = release['recording']['length']




                # artist
                a = {}
                a['mb_id'] = None
                a['name'] = None

                if 'artist' in release and release['artist']:

                    if 'name' in release['artist']:
                        a['name'] = release['artist']['name']

                    if 'id' in release['artist']:
                        a['mb_id'] = release['artist']['id']




                # label
                l = {}
                l['mb_id'] = None
                l['name'] = None
                l['code'] = None


                if 'label' in release and release['label']:

                    if 'name' in release['label']:
                        l['name'] = release['label']['name']

                    if 'id' in release['label']:
                        l['mb_id'] = release['label']['id']

                    if 'label-code' in release['label']:
                        l['code'] = release['label']['label-code']







                # relation mapping
                rel = {}
                rel['discogs_url'] = None
                rel['discogs_image'] = None

                if 'discogs_image' in release and release['discogs_image']:
                    rel['discogs_image'] = release['discogs_image']

                if 'discogs_url' in release and release['discogs_url']:
                    rel['discogs_url'] = release['discogs_url']

                elif 'discogs_master_url' in release and release['discogs_master_url']:
                    rel['discogs_url'] = release['discogs_master_url']




                r['media'] = m
                r['artist'] = a
                r['label'] = l
                r['relations'] = rel


                formatted_releases.append(r)


        return formatted_releases



    def complete_musicbrainz(self, results):

        release_group_ids = []

        rgs = []

        master_releases = []

        # get all release-group-ids
        i = 0
        for r in results:

            if i > 3:
                break
            i+=1

            for release in r['recording']['release-list']:

                mb_release = musicbrainzngs.get_release_by_id(id=release['id'], includes=['release-groups'])
                release_group_id = mb_release['release']['release-group']['id']


                res = {}
                res['release_group_id'] = release_group_id
                res['recording'] = r


                if release_group_id not in release_group_ids:
                    release_group_ids.append(release_group_id)

                if res not in rgs:
                    rgs.append(res)




        #for id in release_group_ids:
        for rg in rgs:

            id = rg['release_group_id']
            r = rg['recording']


            result = musicbrainzngs.get_release_group_by_id(id=id, includes=['releases', 'url-rels'])

            releases = result['release-group']['release-list']

            try:
                relations = result['release-group']['url-relation-list']
                print
                print relations
                print
            except:
                relations = None


            try:
                sorted_releases = sorted(releases, key=lambda k: k['date'])
            except Exception as e:
                print "SORTING ERROR"
                sorted_releases = releases
                print e

            # sorted_releases.reverse()

            first_release = sorted_releases[0]

            print 'releases:'
            print releases

            print 'first release'
            print first_release

            # look up details for the first release
            result = musicbrainzngs.get_release_by_id(id=first_release['id'], includes=['labels', 'url-rels', 'recordings'])

            res = {}
            res['release'] = result['release']
            res['recording'] = r
            res['relations'] = relations
            master_releases.append(res)

        master_releases = self.format_master_releases(master_releases)

        return master_releases


    """
    pre-apply some formatting & structure to provide straighter trmplateing
    """
    def format_master_releases(self, master_releases):


        print
        print '***************************************************'
        print 'format_master_releases'
        print
        print master_releases
        print
        print '***************************************************'
        print


        releases = []

        for re in master_releases:

            release = re['release']
            recording = re['recording']
            relations = re['relations']

            print release

            print 'recording:'
            print recording

            print 'relations:'
            print relations

            r = {}

            r['mb_id'] = None
            r['name'] = None
            r['releasedate'] = None
            r['asin'] = None
            r['barcode'] = None
            r['status'] = None
            r['country'] = None

            # mapping
            try:
                r['mb_id'] = release['id']
            except:
                pass

            try:
                r['name'] = release['title']
            except:
                pass

            try:
                r['releasedate'] = release['date']
            except:
                pass

            try:
                r['asin'] = release['asin']
            except:
                pass

            try:
                r['barcode'] = release['barcode']
            except:
                pass

            try:
                r['status'] = release['status']
            except:
                pass

            try:
                r['country'] = release['country']
            except:
                pass


            # track mapping
            m = {}
            m['mb_id'] = None
            m['name'] = None
            m['duration'] = None

            try:
                m['mb_id'] = recording['recording']['id']
            except:
                pass

            try:
                m['name'] = recording['recording']['title']
            except:
                pass

            try:
                m['duration'] = recording['recording']['length']
            except:
                pass


            # try to get media position
            if 'medium-list' in release:
                print
                print 'got medium list'
                print '*************************************************************'
                print release['medium-list']
                print '*************************************************************'
                for el in release['medium-list'][0]['track-list']:
                    print
                    print el
                    print
                print '*************************************************************'
                print '*************************************************************'


            r['media'] = m

            # artist mapping
            a = {}
            a['mb_id'] = None
            a['name'] = None

            try:
                artist = recording['recording']['artist-credit'][0]['artist']
                print artist

                try:
                    a['mb_id'] = artist['id']
                except:
                    pass

                try:
                    a['name'] = artist['name']
                except:
                    pass
            except:
                pass


            r['artist'] = a


            # label related mapping
            l = {}
            l['mb_id'] = None
            l['name'] = 'Unknown'
            l['code'] = None
            l['catalognumber'] = None

            try:
                label = release['label-info-list'][0]['label']
                print label

                try:
                    l['mb_id'] = label['id']
                except:
                    pass

                try:
                    l['name'] = label['name']
                except:
                    pass

                try:
                    l['code'] = label['label-code']
                except:
                    pass

                try:
                    l['catalognumber'] = release['label-info-list'][0]['catalog-number']
                except:
                    pass

            except Exception as e:
                print e
                pass

            r['label'] = l

            # relation mapping
            rel = {}
            rel['discogs_url'] = None
            rel['discogs_image'] = None

            try:
                try:
                    for relation in relations:
                        if relation['type'] == 'discogs':
                            rel['discogs_url'] = relation['target']
                            rel['discogs_image'] = discogs_image_by_url(relation['target'], 'uri150')


                except Exception as e:
                    print e
                    pass

            except Exception as e:
                print e
                pass

            r['relations'] = rel

            if r not in releases:
                releases.append(r)

        return releases


    def mb_order_by_releasedate(self, releases):

        for release in releases:
            print release

        return releases
