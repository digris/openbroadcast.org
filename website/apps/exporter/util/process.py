# -*- coding: utf-8 -*-
import os
import time
import shutil
import logging

from django.conf import settings
from django.utils.translation import ugettext as _
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from easy_thumbnails.files import get_thumbnailer
from lib.util.filename import safe_name
from alibrary.util.relations import uuid_by_object
from exporter.util.dbox import Synchronizer
from atracker.util import create_event

PROJECT_DIR = getattr(settings, 'PROJECT_DIR', None)
FILENAME_FORMAT = getattr(settings, 'EXPORTER_FILENAME_FORMAT', '%s - %s - %s.%s')
IMAGE_FILENAME = 'cover.jpg'
CREATE_EVENTS = True # should events a.k.a. statistics be added?
INCLUDE_USER = True
INCLUDE_README = True
INCLUDE_HTML_README = True
INCLUDE_LICENSE = False
INCLUDE_PLAYLIST = True
DEFAULT_PLAYLIST_FORMAT = 'm3u'
AVAILABLE_FORMATS = ['mp3', ]
AVAILABLE_ARCHIVE_FORMATS = ['zip', ]

BASE_URL = 'https://www.openbroadcast.org'
#BASE_URL = 'http://local.openbroadcast.org:8080'


log = logging.getLogger(__name__)

class Process(object):

    def __init__(self):

        self.debug = False

        self.status = 0
        self.instance = None
        self.format = None
        self.playlist_format = DEFAULT_PLAYLIST_FORMAT
        self.target = None
        self.archive_dir = None
        self.archive_cache_dir = None
        self.archive_path = None
        self.current_site = Site.objects.get_current()
        self.messages = []
        self.file_list = []




    def run(self, instance, format='mp3', target='download', archive_format='zip'):

        self.instance = instance
        self.user = instance.user
        self.format = format.lower()
        self.target = target
        self.archive_format = archive_format


        # just for testing here
        dbox = Synchronizer(self.instance.user)
        if dbox.dbox_client:
            self.dbox = dbox

        if not self.format in AVAILABLE_FORMATS:
            raise Exception('Format not available.')

        if not self.archive_format in AVAILABLE_ARCHIVE_FORMATS:
            raise Exception('Archive format not available.')

        log.info('running export for "%s": %s - %s' % (self.user.username, self.format, self.target))

        if not self.prepare_directories():
            log.error('directories could not be created')
            self.status = 99
            return self.status

        export_items = self.instance.export_items.all()
        log.debug('%s item(s) to export' % len(export_items))

        for item in export_items:
            status, message = self.process_item(item)
            if message:
                self.messages.append(message)

        if self.target == 'download':
            log.info('download as target, compressing directory')
            shutil.make_archive(self.archive_path, self.archive_format, self.archive_cache_dir, verbose=1)

            if os.path.isfile(self.archive_path + '.%s' % self.archive_format):
                return 1, self.archive_path + '.%s' % self.archive_format, self.messages
            else:
                return 99, None, self.messages


        return self.status, None, self.messages



    def prepare_directories(self):


        if self.debug:
            path = os.path.join('export', 'cache', 'debug')
        else:
            path = os.path.join('export', 'cache', '%s-%s' % (time.strftime("%Y%m%d%H%M%S", time.gmtime()), self.instance.uuid))

        self.archive_dir = os.path.join(PROJECT_DIR, 'media', path)
        self.archive_cache_dir = os.path.join(self.archive_dir, 'cache')
        self.archive_path = os.path.join(self.archive_dir, 'archive') # .zip appended by 'make_archive'


        if not os.path.isdir(self.archive_cache_dir):
            os.makedirs(self.archive_cache_dir)

        log.debug('archive directory: %s' % self.archive_dir)
        log.debug('archive cache-directory: %s' % self.archive_cache_dir)
        log.debug('archive path: %s' % self.archive_path)

        return os.path.isdir(self.archive_cache_dir)


    def clear_cache(self):

        log.debug('cleaning cache: %s' % self.archive_dir)
        try:
            if not self.debug:
                shutil.rmtree(self.archive_dir, True)
        except Exception, e:
            pass


    def process_item(self, item):

        log.info('export ctype: %s | id: %s' % (item.content_type, item.object_id))

        media_set = None
        content_object = item.content_object
        image = None

        ct = item.content_type.name.lower()


        if ct == 'release':
            media_set = content_object.media_release.all()
            image = content_object.main_image
            if content_object.get_artist_display:
                item_rel_dir = os.path.join(
                    safe_name(content_object.get_artist_display()),
                    safe_name(content_object.name)
                )
            else:
                item_rel_dir = safe_name(content_object.get_artist_display())


        if ct == 'track':
            media_set = [content_object]
            if content_object.artist and content_object.release:
                item_rel_dir = os.path.join(
                    safe_name(content_object.artist.name),
                    safe_name(content_object.release.name)
                )
            elif content_object.artist:
                item_rel_dir = safe_name(content_object.artist.name)
            else:
                item_rel_dir = safe_name(content_object.name)


        if ct == 'playlist':
            media_set = []
            image = content_object.main_image
            for m in content_object.get_items():
                media_set.append(m.content_object)

            if content_object.user and content_object.user.get_full_name():
                item_rel_dir = '%s (%s)' % (
                    safe_name(content_object.name),
                    safe_name(content_object.user.get_full_name())
                )
            else:
                item_rel_dir = safe_name(content_object.name)


        item_cache_dir = os.path.join(
            self.archive_cache_dir,
            safe_name(item_rel_dir)
        )
        if not os.path.exists(item_cache_dir):
            os.makedirs(item_cache_dir)

        log.debug('%s tracks to export' % len(media_set))

        # process tracks
        for media in media_set:
            if self.process_media(media, item_cache_dir, item_rel_dir) and CREATE_EVENTS:
                create_event(self.instance.user, media, None, 'download')

        # process additional resources
        if image and os.path.isfile(image.path):
            try:
                shutil.copyfile(image.path, os.path.join(item_cache_dir, IMAGE_FILENAME))
            except Exception, e:
                print e

        if INCLUDE_README:
            self.process_readme(instance=content_object, cache_dir=item_cache_dir)

        if INCLUDE_HTML_README:
            try:
                self.process_html_readme(instance=content_object, cache_dir=item_cache_dir)
            except:
                pass

        if INCLUDE_LICENSE:
            self.process_license(instance=content_object, cache_dir=item_cache_dir, file_list=self.file_list)

        if INCLUDE_PLAYLIST:
            pass

        return None, None


    def process_media(self, media, item_cache_dir, item_rel_dir):
        """
        copy media to directory & applying metadata
        """
        filename = safe_name(FILENAME_FORMAT % (media.tracknumber, media.name, media.artist.name, self.format))
        file_path = os.path.join(item_cache_dir, filename)
        cache_file = media.get_cache_file('mp3', 'base')

        log.info('processing media: pk %s' % media.pk)
        #log.debug('cache file: %s' % cache_file)

        if not cache_file:
            self.messages.append((media, _('The file seems to be missing. Sorry.')))
            return

        try:
            shutil.copyfile(cache_file, file_path)

        except Exception, e:
            print e
            self.messages.append((media, e))
            return

        try:
            self.inject_metadata(file_path, media)

        except Exception, e:
            print e
            self.messages.append((media, e))
            return

        self.file_list.append({
            'filename': filename,
            'directory': item_rel_dir,
            'item': media
        })

        return True

        #if self.dbox:
        #    self.dbox.upload(file_path, filename)



    def process_readme(self, instance, cache_dir):

        from django.utils import translation
        translation.activate('en')

        log.debug('processing readme')
        template = 'exporter/txt/readme.txt'

        with open(os.path.join(cache_dir, 'readme.txt'), "w") as txt:
            str = render_to_string(template, {'object': instance, 'base_url': BASE_URL })
            txt.write(str.encode('utf8'))



    def process_html_readme(self, instance, cache_dir):

        from django.utils import translation
        translation.activate('en')

        log.debug('processing HTML readme')

        ct = instance.__class__.__name__.lower()

        # TODO: modularize
        if ct in ['release',]:
            template = 'exporter/assets/%s.html' % ct
            with open(os.path.join(cache_dir, 'readme.html'), "w") as txt:
                str = render_to_string(template, {'object': instance, 'base_url': BASE_URL })
                txt.write(str.encode('utf8'))


    def process_license(self, instance, cache_dir, file_list=[]):

        from django.utils import translation
        translation.activate('en')

        log.debug('processing license')
        template = 'exporter/txt/LICENSE.TXT'

        with open(os.path.join(cache_dir, 'LICENSE.TXT'), "w") as txt:
            str = render_to_string(template, {'object': instance, 'file_list': file_list})
            txt.write(str.encode('utf8'))





    def inject_metadata(self, path, media):

        if self.format == 'mp3':
            self.metadata_mp3_mutagen(path, media)
            #self.metadata_audiotools(path, media)

        return




    def metadata_mp3_mutagen(self, path, media):

        from mutagen.mp3 import MP3
        from mutagen.id3 import ID3, TRCK, TIT2, TPE1, TALB, TCON, TXXX, UFID, TSRC, TPUB, TMED, TRCK, TDRC

        try:
            tags = ID3(path)
        except Exception:
            """
            kindf of hackish - mutagen does complain if no id3 headers - so just create some
            """
            audio = MP3(path)
            audio["TIT2"] = TIT2(encoding=3, text=["Empty Title"])
            audio.save()
            tags = ID3(path)



        # reset tags
        tags.delete()

        # user data
        if INCLUDE_USER and self.user:
            tags.add(TXXX(encoding=3, desc='Open Broadcast User', text=u'%s' % self.user.email))



        # track-level metadata
        tags.add(TIT2(encoding=3, text=u'%s' % media.name))
        tags.add(UFID(encoding=3, owner='http://openbroadcast.org', data=u'%s' % media.uuid))

        tags.add(TXXX(encoding=3, desc='Open Broadcast API', text=u'http://%s%s' % (self.current_site.domain, media.get_api_url())))
        # remove genre
        tags.add(TCON(encoding=3, text=u''))
        tags.add(TMED(encoding=3, text=u'Digital Media'))
        if media.tracknumber:
            tags.add(TRCK(encoding=3, text=u'%s' % media.tracknumber))
        if media.isrc:
            tags.add(TSRC(encoding=3, text=u'%s' % media.isrc))

        if uuid_by_object(media, 'musicbrainz'):
            tags.add(UFID(encoding=3, owner='http://musicbrainz.org', data=u'%s' % uuid_by_object(media, 'musicbrainz')))

        # release-level metadata
        if media.release:
            tags.add(TALB(encoding=3, text=u'%s' % media.release.name))
            if media.release.catalognumber:
                tags.add(TXXX(encoding=3, desc='CATALOGNUMBER', text=u'%s' % media.release.catalognumber))
            if media.release.releasedate:
                tags.add(TDRC(encoding=3, text=u'%s' % media.release.releasedate.year))
            if media.release.release_country:
                tags.add(TXXX(encoding=3, desc='MusicBrainz Album Release Country', text=u'%s' % media.release.release_country.iso2_code))
            if media.release.totaltracks and media.tracknumber:
                tags.add(TRCK(encoding=3, text=u'%s/%s' % (media.tracknumber, media.release.totaltracks)))
            if media.release.releasedate:
                tags.add(TDRC(encoding=3, text=u'%s' % media.release.releasedate.year))

            if uuid_by_object(media.release, 'musicbrainz'):
                tags.add(TXXX(encoding=3, desc='MusicBrainz Album Id', text=u'%s' % uuid_by_object(media.release, 'musicbrainz')))

        # artist-level metadata
        if media.artist:
            tags.add(TPE1(encoding=3, text=u'%s' % media.artist.name))
            if uuid_by_object(media.artist, 'musicbrainz'):
                tags.add(TXXX(encoding=3, desc='MusicBrainz Artist Id', text=u'%s' % uuid_by_object(media.artist, 'musicbrainz')))

        # label-level metadata
        if media.release and media.release.label:
            tags.add(TPUB(encoding=3, text=u'%s' % media.release.label.name))

        tags.save(v1=0)

        return



    def metadata_audiotools(self, path, media):

        from audiotools import MetaData
        import audiotools

        meta = MetaData()

        # release-level metadata
        if media.release and media.release.main_image:

            if meta.supports_images() and os.path.exists(media.release.main_image.path):
                opt = dict(size=(200, 200), crop=True, bw=False, quality=80)
                image = get_thumbnailer(media.release.main_image).get_thumbnail(opt)
                meta.add_image(get_raw_image(image.path, 0))

        audiotools.open(path).update_metadata(meta)

        return



def get_raw_image(filename, type):

    import audiotools

    try:
        f = open(filename, 'rb')
        data = f.read()
        f.close()

        return audiotools.Image.new(data, u'', type)
    except IOError:
        raise audiotools.InvalidImage(u'Unable to open file')