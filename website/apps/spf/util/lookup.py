import logging

import musicbrainzngs
from obp_legacy.models import *
log = logging.getLogger(__name__)


class MediaLookup(object):

    def __init__(self):
        log = logging.getLogger('util.migrator.__init__')
        musicbrainzngs.set_useragent("Example music app", "0.1", "http://example.com/music")
        #musicbrainzngs.set_hostname("mb.anorg.net")
        #musicbrainzngs.set_rate_limit(limit_or_interval=False)


    def mb_search(self, obj, level=5):

        log = logging.getLogger('util.lookup.mb_search')
        log.info('search for: %s' % obj.title)

        result = {}
        recordings = None
        num_recordings = 0

        title = obj.title
        credit = None
        """
        do some shizzle with the title
        """
        try:
            tt = title.split('(')
            title = tt[0]
            print 'stripped title: %s' % title
            credit = tt[1].replace('Featuring', '').replace(')', '').strip(' ')
            print 'credit: %s' % credit


        except Exception, e:
            print e
            pass


        """
        data preparation
        """
        extra_query = '';

        if obj.recording_datex:
            ry = obj.recording_datex.year
            extra_query += 'date:[%s-01-01 TO %s-12-31]' % (ry, ry)

        qdur = ''
        if obj.duration:
            print 'DURATION: %s' % obj.duration
            qdur = '%s' % (obj.duration / 2)
            print 'QDUR: %s' % qdur


        if level == 5:
            rs = musicbrainzngs.search_recordings(
                                                  #query=extra_query,
                                                  recordingaccent='%s' % title,
                                                  strict=True,
                                                  country='%s' % obj.recording_country,
                                                  qdur=qdur,
                                                  primarytype='Album',
                                                  artist='%s' % obj.main_artist,
                                                )


        if level == 4:
            rs = musicbrainzngs.search_recordings(
                                                  #query=extra_query,
                                                  recordingaccent='%s' % title,
                                                  strict=True,
                                                  country='%s' % obj.recording_country,
                                                  #qdur=qdur,
                                                  primarytype='Album',
                                                  artist='%s' % obj.main_artist,
                                                )


        if level == 3:
            rs = musicbrainzngs.search_recordings(
                                                  #query=extra_query,
                                                  recordingaccent='%s' % title,
                                                  strict=True,
                                                  country='%s' % obj.recording_country,
                                                  #qdur=qdur,
                                                  #primarytype='Album',
                                                  artist='%s' % obj.main_artist,
                                                )


        if level == 2:
            rs = musicbrainzngs.search_recordings(
                                                  #query=extra_query,
                                                  recordingaccent='%s' % title,
                                                  strict=True,
                                                  #country='%s' % obj.recording_country,
                                                  #qdur=qdur,
                                                  #primarytype='Album',
                                                  artist='%s' % obj.main_artist,
                                                )


        try:
            recordings = rs['recording-list']
            num_recordings = len(recordings)
        except:
            pass


        return num_recordings, recordings




    def run(self, obj):

        status = 1

        log = logging.getLogger('util.lookup.run')
        log.info('lookup request: %s' % obj.title)





        print
        print '---------------------------------------------'
        print 'swp_id:    %s' % obj.swp_id
        print 'title:     %s' % obj.title
        print 'country:   %s' % obj.recording_country
        print 'artist:    %s' % obj.main_artist
        print 'date:      %s' % obj.recording_datex
        print


        level = 5
        """ """
        num_recordings = 0
        while level > 0 and num_recordings < 1:
            num_recordings, recordings = self.mb_search(obj, level)
            level -= 1
            #time.sleep(2)


        #num_recordings, recordings = self.mb_search(obj, 5)


        #print rs
        #print recordings
        print 'num recordings: %s' % num_recordings
        print 'level used:     %s' % (level + 1)
        print
        print
        #time.sleep(1)


        return num_recordings, recordings, (level + 1)


class LegacyLookup(object):

    def __init__(self):
        log = logging.getLogger('util.migrator.__init__')



    def legacy_search(self, obj):

        log = logging.getLogger('util.lookup.legacy_search')
        log.info('search for: %s' % obj.title)

        result = {}
        recordings = None
        num_recordings = 0


        #lms = Medias.objects.using('legacy').filter(name='%s' % obj.title)
        lms = Medias.objects.using('legacy').filter(name='%s' % obj.title, artistsmedias__artist__name='%s' % obj.main_artist)


        recordings = lms
        num_recordings = lms.count()

        if lms.count() > 0:
            print '###########################################'
            print 'got legacy data!'
            for lm in lms:

                lams = lm.artistsmedias_set.all()
                #lams = lm.artistsmedias_set.filter(artist__name='%s' % obj.main_artist)
                obj.obp_legacy_id = lm.id
                obj.save()

                for la in lams:
                    print 'Artist: %s' % la.artist.name

        return num_recordings, recordings




    def run(self, obj):

        status = 1

        log = logging.getLogger('util.lookup.run')
        log.info('lookup request: %s' % obj.title)

        print
        print '---------------------------------------------'
        print 'swp_id:    %s' % obj.swp_id
        print 'title:     %s' % obj.title
        print 'country:   %s' % obj.recording_country
        print 'artist:    %s' % obj.main_artist
        print 'date:      %s' % obj.recording_datex
        print


        num_recordings, recordings = self.legacy_search(obj)


        #print rs
        #print recordings
        print 'num recordings: %s' % num_recordings
        print
        print


        return num_recordings, recordings