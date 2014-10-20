#-*- coding: utf-8 -*-
import os
import hashlib
import pprint
from optparse import make_option
import logging

from django.core.management.base import BaseCommand, NoArgsCommand


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


class MaintenanceWorker(object):
    def __init__(self, *args, **kwargs):
        self.action = kwargs.get('action')
        self.delete_missing = kwargs.get('delete_missing')
        self.pp = pprint.PrettyPrinter(indent=4)
        #self.pp.pprint = lambda d: None

        try:
            self.limit = int(kwargs.get('limit'))
        except:
            self.limit = DEFAULT_LIMIT

        try:
            self.id = int(kwargs.get('id'))
        except:
            self.id = None

        self.verbosity = int(kwargs.get('verbosity', 1))

    def run(self):

        log.info('maintenance walker')
        log.info('action: %s' % self.action)

        if self.action == 'check_media':

            from alibrary.models import Media


            if self.id:
                items = Media.objects.filter(id=self.id)
            else:
                items = Media.objects.filter()[0:self.limit]

            for item in items:

                delete = False

                if not item.master:
                    log.info('no master for: %s' % item)
                    if self.delete_missing:
                        log.info('delete item: %s' % item)
                        delete = True

                else:
                    log.debug('got master for: %s' % item)
                    log.debug('path: %s' % item.master.path)
                    #print item.master.path

                    if os.path.isfile(item.master.path):
                        size = b = os.path.getsize(item.master.path)
                        log.debug('filesize: %s' % size)
                        if size < 10:
                            log.debug('size too small or zero > delete: %s' % size)

                    else:
                        log.debug('file does not exist')
                        delete = True

                if delete and self.delete_missing:
                    log.info('delete item: %s' % item)
                    item.delete()

                if not delete:
                    item.status = 1
                    item.save()


        if self.action == 'echonest_media':

            from alibrary.models import Media

            if self.id:
                items = Media.objects.filter(id=self.id)
            else:
                items = Media.objects.filter(echonest_id=None)[0:self.limit]

            for item in items:
                log.info('analyze: %s' % item)
                item.echonest_analyze()


        if self.action == 'clean_playlists':

            from alibrary.models import PlaylistItem
            from alibrary.models import Media

            items = PlaylistItem.objects.all()

            for item in items:
                log.info('clean: %s' % item.pk)
                if not item.content_object:
                    log.info('no content object > delete: %s' % item.pk)
                    item.delete()
                # m = Media.objects.get(pk=item.)


        if self.action == 'self_check_playlists':

            from alibrary.models.playlistmodels import self_check_playlists

            # reset
            # ps = Playlist.objects.all()
            # ps.update(status=1)

            self_check_playlists()


        if self.action == 'degrade_playlists':
            from alibrary.models.playlistmodels import Playlist
            ps = Playlist.objects.filter(type='broadcast').exclude(status=1)

            ps.update(type='playlist', status=1)




        if self.action == 'map_tags':

            from alibrary.models import Media


            if self.id:
                items = Media.objects.filter(id=self.id)
            else:
                items = Media.objects.filter()[0:self.limit]

            for item in items:

                if item.tags.count() < 1:
                    print item
                    print 'map release tags'
                    if item.release and item.release.tags.count() > 0:
                        item.tags = item.release.tags
                        item.save()




        if self.action == 'echonest_media__':

            from alibrary.models import Media
            from pyechonest.util import EchoNestAPIError
            from pyechonest import track
            from pyechonest import config as echonest_config
            echonest_config.ECHO_NEST_API_KEY=ECHONEST_API_KEY

            if self.id:
                items = Media.objects.filter(id=self.id)
            else:
                items = Media.objects.filter(status=0)[0:self.limit]

            for item in items:
                log.info('analyze: %s' % item)




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

                    print t
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

                    self.pp.pprint(t.meta)
                    self.pp.pprint(t.sections)


                    item.save()

                # r = requests.get(t.analysis_url)
                # self.pp.pprint(r.json())


class Command(NoArgsCommand):
    """
    Import directory structure into alibrary:

        manage.py import_folder --path=/tmp/assets/images
    """

    option_list = BaseCommand.option_list + (
        make_option('--action',
                    action='store',
                    dest='action',
                    default=None,
                    help='action to perform'),
        make_option('--id',
                    action='store',
                    dest='id',
                    default=None,
                    help='Specify an ID to run migration on'),
        make_option('--limit',
                    action='store',
                    dest='limit',
                    default=None,
                    help='Specify an ID to run migration on'),
        make_option('--delete_missing',
                    action='store_true',
                    dest='delete_missing',
                    default=None,
                    help='Delete missing items'),
    )

    def handle_noargs(self, **options):
        worker = MaintenanceWorker(**options)
        worker.run()
