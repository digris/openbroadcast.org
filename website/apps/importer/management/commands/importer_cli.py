# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
import os
import sys
import locale
from collections import namedtuple
import collections
import codecs

from django.core.management import BaseCommand
from django.core.management import CommandError
from lib.util.sha1 import sha1_by_file
from django.core.files import File as DjangoFile
from mutagen import File as MutagenFile
from mutagen.easyid3 import EasyID3
from mutagen.easymp4 import EasyMP4


FileContainer = namedtuple('FileContainer', ['path',], verbose=True)
log = logging.getLogger(__name__)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('action')

        parser.add_argument('-p', '--path',
                            action='store',
                            dest='path',
                            help='path to scan (recursive)')



    def handle(self, *args, **options):

        print('')
        print("***********************************************************")
        print("* action: {}".format(options['action']))
        print("***********************************************************")
        print('')

        getattr(self, options['action'])(options)


    def scan_meta(self, options):

        path = options['path']

        print("***********************************************************")
        print("* path:   {}".format(path))
        print("***********************************************************")
        print('')

        if not os.path.exists(path):
            raise CommandError('Path does not exists/is not a directory: {}'.format(path))


        from importer.util.identifier import Identifier

        identifier = Identifier()

        extensions = [
            '.flac',
            '.mp3',
        ]

        if os.path.isfile(path):
            print '** SINGLE FILE'

            print extract_metadata(path)


            sys.exit()




        #log_f = open('/Users/ohrstrom/tmp/scanlog.txt', 'a')
        log_f = codecs.open('/Users/ohrstrom/tmp/scanlog.txt', 'a', "utf-8")



        for entry in rscandir(path):
            if os.path.isfile(entry):
                if os.path.splitext(entry)[1] in extensions:
                    artist_id = extract_metadata(entry, log_f)

                    if isinstance(artist_id, collections.Iterable):
                        str_to_write = ' ** '.join(artist_id)

                    else:
                        str_to_write = artist_id


                    print str_to_write
                    if str_to_write:
                        log_f.write(entry.decode('ascii', 'ignore') + ';' + str_to_write + '\n')

            else:
                pass
                #print('NON FILE:'),
                #print(entry)

        log_f.close()


def rscandir(path):
    for p in os.listdir(path):
        p = os.path.join(path, p)
        yield p
        if os.path.isdir(p):
            for q in rscandir(p):
                yield q


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
    'media_genres': [],
    'media_tags': [],
    'media_copyright': None,
    'media_comment': None,
    'media_bpm': None,
}

def extract_metadata(path, log_f=None):

    #log.info('Extracting metadata for: %s' % (path))

    enc = locale.getpreferredencoding()

    meta = None
    ext = os.path.splitext(path)[1]
    #log.debug('detected %s as extension' % ext)

    if ext:
        ext = ext.lower()

    if ext == '.mp3':
        try:
            meta = EasyID3(path)
        except Exception, e:
            log.debug('unable to process MP3')
            log_f.write(path + ';' + 'unable to process MP3: {}'.format(path) + '\n')

    if ext in ['.mp4', '.m4a']:
        try:
            meta = EasyMP4(path)
        except Exception, e:
            log.debug('unable to process M4A')
            log_f.write(path + ';' + 'unable to process M4A: {}'.format(path) + '\n')

    if not meta:
        try:
            meta = MutagenFile(path)
            #log.debug('using MutagenFile')
        except Exception, e:
            log.warning('even unable to open file with straight mutagen: %s' % e)
            log_f.write(path + ';' + 'unable to process mutagen: {}'.format(path) + '\n')

    dataset = dict(METADATA_SET)


    if meta:
        return meta.get('musicbrainz_artistid')

    else:
        return 'unable to extract metadata for: {}'.format(path)


