#-*- coding: utf-8 -*-
import os
import hashlib
import pprint
from optparse import make_option
import logging

from django.core.management.base import BaseCommand, NoArgsCommand




#######################################################################
# TODO: legacy commands. refactor to click!
#######################################################################





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

        if self.action == 'reprocess_masters':

            from tqdm import tqdm
            from alibrary.models import Media
            from base.audio.fileinfo import FileInfoProcessor

            items = Media.objects.filter(master_bitrate=None)[0:self.limit]

            for item in tqdm(items):
                if item.master and item.master.path:
                    file_processor = FileInfoProcessor(item.master.path)
                    if file_processor.audio_stream:

                        #print '+',

                        # print 'encoding: %s' % file_processor.encoding
                        # print 'filesize: %s' % file_processor.filesize
                        # print 'bitrate: %s' % file_processor.bitrate
                        # print 'samplerate: %s' % file_processor.samplerate
                        # print 'duration: %s' % file_processor.duration


                        Media.objects.filter(pk=item.pk).update(
                            master_encoding = file_processor.encoding,
                            master_filesize = file_processor.filesize,
                            master_bitrate = file_processor.bitrate,
                            master_samplerate = file_processor.samplerate,
                            #master_duration = file_processor.duration
                        )

                    else:
                        pass
                        #print '.',


        if self.action == 'warm_appearances_cache':

            from alibrary.models import Artist
            from tqdm import tqdm


            for item in tqdm(Artist.objects.order_by('-created').all()):

                item.get_releases()
                item.get_media()




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
                    if item.release and item.release.tags.count() > 0:
                        item.tags = item.release.tags
                        item.save()


        if self.action == 'set_parent_temporary_id':

            from alibrary.models import Label
            labels = Label.objects.exclude(parent__isnull=True)

            for label in labels:
                Label.objects.filter(pk=label.pk).update(parent_temporary_id=label.parent.pk)


        if self.action == 'update_label_tree':

            from alibrary.models import Label
            labels = Label.objects.exclude(parent_temporary_id__isnull=True)

            for label in labels:
                parent_label = Label.objects.get(pk=label.parent_temporary_id)
                Label.objects.filter(pk=label.pk).update(parent=parent_label)

                #Label.objects.filter(pk=label.pk).update(parent_temporary_id=label.parent.pk)




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
