#-*- coding: utf-8 -*-
import hashlib
import pprint
import logging

from pyechonest.util import EchoNestAPIError
from pyechonest import track
from pyechonest import config as echonest_config


log = logging.getLogger(__name__)

ECHONEST_API_KEY = 'DC7YKF3VYN7R0LG1M'

DEFAULT_LIMIT = 200


def md5_for_file(f, block_size=2 ** 20):
    md5 = hashlib.md5()
    while True:
        data = f.read(block_size)
        if not data:
            break
        md5.update(data)
    return md5.hexdigest()


class EchonestWorker(object):

    def __init__(self, *args, **kwargs):
        self.pp = pprint.PrettyPrinter(indent=4)
        self.pp.pprint = lambda d: None
        echonest_config.ECHO_NEST_API_KEY=ECHONEST_API_KEY


    def analyze(self, item):

        log.info('analyze')

        #md5 = '96fa0180d225f14e9f8cbfffbf5eb81d'

        t = None

        if item.echonest_id:
            try:
                log.debug('query by echonest id: %s' % item.echonest_id)
                t = track.track_from_id(item.echonest_id)
            except EchoNestAPIError, e:
                print e

        if not t:
            try:
                f = open(item.master.path)
                md5 = md5_for_file(f);
                log.debug('query by md5: %s' % md5)
                t = track.track_from_md5(md5)
            except EchoNestAPIError, e:
                print e


        if not t:
            try:
                log.debug('query by file: %s' % item.master.path)
                f = open(item.master.path)
                t = track.track_from_file(f, 'mp3')
            except EchoNestAPIError, e:
                print e


        if t:
            item.echonest_id = t.id

            t.get_analysis()

            #print t
            print t.id
            print t.analysis_url
            print
            print 'danceability:      %s' % t.danceability
            print 'energy:            %s' % t.energy
            print 'key:               %s' % t.key
            print 'liveness:          %s' % t.liveness
            print 'loudness:          %s' % t.loudness
            print 'speechiness:       %s' % t.speechiness
            print 'duration:          %s' % t.duration
            print 'start_of_fade_out: %s' % t.start_of_fade_out
            print 'tempo:             %s' % t.tempo

            item.danceability = t.danceability
            item.energy = t.energy
            item.key = t.key
            item.liveness = t.liveness
            item.loudness = t.loudness
            item.speechiness = t.speechiness
            item.echonest_duration = t.duration
            item.start_of_fade_out = t.start_of_fade_out
            item.tempo = t.tempo
            item.sections = t.sections

            self.pp.pprint(t.meta)
            self.pp.pprint(t.sections)


        return item

        # r = requests.get(t.analysis_url)
        # self.pp.pprint(r.json())


