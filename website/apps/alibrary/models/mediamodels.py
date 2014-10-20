# python
import shutil
import time
import subprocess
import json
import ntpath

from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.core.files import File as DjangoFile
from django.core.urlresolvers import reverse

# TODO: only import needed settings
from settings import *

from django.conf import settings

from alibrary import settings as alibrary_settings



# django-extensions (http://packages.python.org/django-extensions/)
from django_extensions.db.fields import AutoSlugField
from lib.fields.uuidfield import UUIDField as RUUIDField

# cms
from cms.models import CMSPlugin, Page
from cms.models.fields import PlaceholderField
from cms.utils.placeholder import get_page_from_placeholder_if_exists

# filer
from filer.models.filemodels import *
from filer.models.foldermodels import *
from filer.models.audiomodels import *
from filer.models.imagemodels import *
from filer.fields.image import FilerImageField
from filer.fields.audio import FilerAudioField
from filer.fields.file import FilerFileField

from django_extensions.db.fields.json import JSONField

# private_files
#from private_files import PrivateFileField

# modules
#from taggit.managers import TaggableManager
from easy_thumbnails.files import get_thumbnailer

# audiotools (for conversion)
from audiotools import MetaData
import audiotools
import tempfile

# celery / task management
from celery.task import task


# shop
from shop.models import Product

# audio processing / waveform
from lib.audioprocessing.processing import create_wave_images, AudioProcessingException
from lib.fields.languages import LanguageField
from lib.signals.unsignal import disable_for_loaddata
# hash
from lib.util.sha1 import sha1_by_file

# echoprint
from ep.API import fp

# logging
import logging
log = logging.getLogger(__name__)
    
    
################
from alibrary.models.basemodels import *
from alibrary.models.artistmodels import *
from alibrary.models.playlistmodels import PlaylistItem, Playlist

from alibrary.util.slug import unique_slugify
from alibrary.util.storage import get_dir_for_object, OverwriteStorage

from alibrary.util.echonest import EchonestWorker
from caching.base import CachingMixin, CachingManager
import arating

USE_CELERYD = True
AUTOCREATE_ECHOPRINT = False

LOOKUP_PROVIDERS = (
    #('discogs', _('Discogs')),
    ('musicbrainz', _('Musicbrainz')),
)


VERSION_CHOICES = (
    ('original', _('Original')),
    ('remix', _('Remix')),
    ('cover', _('Cover')),
    ('live', _('Live Version')),
    ('studio', _('Studio Version')),
    ('radio', _('Radio Version')),
    ('demo', _('Demo Version')),
    ('other', _('Other')),
)

MEDIATYPE_CHOICES = (
    (_('Single content recording'), (
            ('song', _('Song')),
            ('acappella', _('A cappella')),
            ('soundeffects', _('Sound effects')),
            ('soundtrack', _('Soundtrack')),
            ('spokenword', _('Spokenword')),
            ('interview', _('Interview')),
            ('jingle', _('Jingle')),
        )
    ),
    (_('Multiple content recording'), (
            ('djmix', _('DJ-Mix')),
            ('concert', _('Concert')),
            ('liveact', _('Live Act (PA)')),
        )
    ),
    ('other', _('Other')),
    (None, _('Unknown')),
)




# TODO: depreciated
def clean_filename(filename):
    import unicodedata
    import string
    valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
    cleaned = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore')
    return ''.join(c for c in cleaned if c in valid_chars)

# TODO: depreciated
def masterpath_by_uuid(instance, filename):
    filename, extension = os.path.splitext(filename)
    folder = "private/%s/" % (instance.uuid.replace('-', '/')[5:])
    #filename = instance.uuid.replace('-', '/') + extension
    filename = u'master'
    return os.path.join(folder, "%s%s" % (clean_filename(filename).lower(), extension.lower()))




def upload_master_to(instance, filename):
    filename, extension = os.path.splitext(filename)
    return os.path.join(get_dir_for_object(instance), 'master%s' % extension.lower())



def audiotools_progress(x, y):
    p = (x * 100 / y)
    last_p = None
    if (p%10) == 0:
        pass
        #log.debug('conversion: %s' % p)

#class Media(CachingMixin, MigrationMixin):
class Media(MigrationMixin):

    # core fields
    uuid = RUUIDField(primary_key=False)
    name = models.CharField(max_length=255, db_index=True)
    slug = AutoSlugField(populate_from='name', editable=True, blank=True, overwrite=True)
    
    STATUS_CHOICES = (
        (0, _('Init')),
        (1, _('Ready')),
        (3, _('Working')),
        (4, _('File missing')),
        (5, _('File error')),
        (99, _('Error')),
    )
    status = models.PositiveIntegerField(default=0, choices=STATUS_CHOICES)


    
    publish_date = models.DateTimeField(blank=True, null=True)

    
    
    # processed & lock flag (needed for models that have maintenance/init/save tasks)
    PROCESSED_CHOICES = (
        (0, _('Waiting')),
        (1, _('Done')),
        (99, _('Error')),
    )
    processed = models.PositiveIntegerField(max_length=2, default=0, choices=PROCESSED_CHOICES)
    
    ECHOPRINT_STATUS_CHOICES = (
        (0, _('Init')),
        (1, _('Assigned')),
        (2, _('Error')),
        (99, _('Error')),
    )
    echoprint_status = models.PositiveIntegerField(max_length=2, default=0, choices=ECHOPRINT_STATUS_CHOICES)
        
    CONVERSION_STATUS_CHOICES = (
        (0, _('Init')),
        (1, _('Completed')),
        (2, _('Error')),
        (99, _('Error')),
    )
    conversion_status = models.PositiveIntegerField(max_length=2, default=0, choices=CONVERSION_STATUS_CHOICES)

    lock = models.PositiveIntegerField(max_length=1, default=0, editable=False)

    TRACKNUMBER_CHOICES = ((x, x) for x in range(1, 101))
    tracknumber = models.PositiveIntegerField(verbose_name=_('Track Number'), max_length=12, blank=True, null=True, choices=TRACKNUMBER_CHOICES)

    opus_number = models.CharField(max_length=200, blank=True, null=True)

    MEDIANUMBER_CHOICES = ((x, x) for x in range(1, 51))
    # a.k.a. "Disc number"
    medianumber = models.PositiveIntegerField(verbose_name=_('a.k.a. "Disc number'), blank=True, null=True, max_length=12, choices=MEDIANUMBER_CHOICES)
    

    mediatype = models.CharField(verbose_name=_('Type'), max_length=12, default='song', choices=MEDIATYPE_CHOICES)

    version = models.CharField(max_length=12, blank=True, null=True, default='track', choices=VERSION_CHOICES)


    description = models.TextField(verbose_name="Extra Description / Tracklist", blank=True, null=True)
    lyrics = models.TextField(blank=True, null=True)
    lyrics_language = LanguageField(blank=True, null=True)

    duration = models.PositiveIntegerField(verbose_name="Duration (in ms)", max_length=12, blank=True, null=True, editable=False)
    
    # relations
    release = models.ForeignKey('Release', blank=True, null=True, related_name='media_release', on_delete=models.SET_NULL)
    artist = models.ForeignKey('Artist', blank=True, null=True, related_name='media_artist')
    
    # user relations
    owner = models.ForeignKey(User, blank=True, null=True, related_name="media_owner", on_delete=models.SET_NULL)
    creator = models.ForeignKey(User, blank=True, null=True, related_name="media_creator", on_delete=models.SET_NULL)
    publisher = models.ForeignKey(User, blank=True, null=True, related_name="media_publisher", on_delete=models.SET_NULL)

    # identifiers
    isrc = models.CharField(verbose_name='ISRC', max_length=12, null=True, blank=True)
    
    # relations a.k.a. links
    relations = generic.GenericRelation(Relation)

    playlist_items = generic.GenericRelation(PlaylistItem, object_id_field="object_id")

    
    # tagging (d_tags = "display tags")
    d_tags = tagging.fields.TagField(max_length=1024, verbose_name="Tags", blank=True, null=True)
    
    # extra-artists
    # TODO: Fix this - guess should relate to Artist instead of Profession
    extra_artists = models.ManyToManyField('Artist', through='MediaExtraartists', blank=True, null=True)
    
    license = models.ForeignKey(License, blank=True, null=True, related_name='media_license', limit_choices_to={'selectable': True}, on_delete=models.PROTECT)
    
    # File related (old)
    #master = FilerAudioField(blank=True, null=True, related_name='media_master')
    #master_path = models.CharField(max_length=2048, null=True, blank=True, help_text="Master Path", editable=False)
    #folder = models.ForeignKey(Folder, blank=True, null=True, related_name='media_folder', editable=False, on_delete=models.SET_NULL)
    
    # File related (new)
    #master = models.FileField(max_length=1024, upload_to=masterpath_by_uuid, blank=True, null=True)
    filename = models.CharField(verbose_name=_('Filename'), max_length=256, blank=True, null=True)
    original_filename = models.CharField(verbose_name=_('Original filename'), max_length=256, blank=True, null=True)
    master = models.FileField(max_length=1024, upload_to=upload_master_to, blank=True, null=True)
    master_sha1 = models.CharField(max_length=64, db_index=True, blank=True, null=True)
    
    
    folder = models.CharField(max_length=1024, null=True, blank=True, editable=False)
    
    # File Data
    base_format = models.CharField(verbose_name=_('Format'), max_length=12, blank=True, null=True)
    base_filesize = models.PositiveIntegerField(verbose_name=_('Filesize'), blank=True, null=True)
    base_duration = models.FloatField(verbose_name=_('Duration'), blank=True, null=True)
    base_samplerate = models.PositiveIntegerField(verbose_name=_('Samplerate'), blank=True, null=True)
    base_bitrate = models.PositiveIntegerField(verbose_name=_('Bitrate'), blank=True, null=True)

    # echonest data
    echonest_id = models.CharField(max_length=20, blank=True, null=True)
    danceability = models.FloatField(null=True, blank=True)
    energy = models.FloatField(null=True, blank=True)
    liveness = models.FloatField(null=True, blank=True)
    loudness = models.FloatField(null=True, blank=True)
    speechiness = models.FloatField(null=True, blank=True)
    start_of_fade_out = models.FloatField(null=True, blank=True)
    echonest_duration = models.FloatField(null=True, blank=True)
    tempo = models.FloatField(null=True, blank=True)
    key = models.IntegerField(null=True, blank=True)

    sections = JSONField(blank=True, null=True)



    #force_migration = models.IntegerField(null=True, blank=True) # dummy field, to trigger mermission db-updates



    # tagging
    #tags = TaggableManager(blank=True)
    
    # manager
    objects = models.Manager()
    #objects = CachingManager()
    
    # auto-update
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)



    class Meta:
        app_label = 'alibrary'
        verbose_name = _('Track')
        verbose_name_plural = _('Tracks')
        ordering = ('medianumber', 'tracknumber', )

        permissions = (
            ('play_media', 'Play Track'),
            ('downoad_media', 'Download Track'),
            ('merge_media', 'Merge Tracks'),
            ('admin_media', 'Edit Track (extended)'),
            ('upload_media', 'Upload Track'),
        )
    
    
    def __unicode__(self):
        return self.name


    @property
    def duration_s(self):
        return self.get_duration(units='s')

    @property
    def duration_ms(self):
        return self.get_duration(units='ms')

    
    @property
    def classname(self):
        return self.__class__.__name__

    def get_versions(self):
        try:
            return reversion.get_for_object(self)
        except:
            return None
        
    
    def get_last_revision(self):
        try:
            return reversion.get_unique_for_object(self)[0].revision
        except:
            return None
        
    def get_last_editor(self):
        latest_revision = self.get_last_revision()
        if latest_revision:
            return latest_revision.user
        else:
            try:
                return User.objects.get(username='root')
            except:
                pass
            return None


    def get_lookup_providers(self):

        providers = []
        for key, name in LOOKUP_PROVIDERS:
            relations = self.relations.filter(service=key)
            relation = None
            if relations.count() == 1:
                relation = relations[0]

            providers.append({'key': key, 'name': name, 'relation': relation})

        return providers

    
    @models.permalink
    def get_absolute_url(self):
        return ('alibrary-media-detail', [self.slug])

    @models.permalink
    def get_edit_url(self):
        return ('alibrary-media-edit', [self.pk])

    def get_admin_url(self):
        from lib.util.get_admin_url import change_url
        return change_url(self)
    
    @models.permalink
    def get_stream_url(self):
        return ('en:alibrary-media-stream_html5', [self.uuid])

    @models.permalink
    def get_encode_url(self, format='mp3', bitrate='32'):
        #return ('alibrary-media-encode', [self.uuid, format, bitrate])
        return ('alibrary-media-encode', (), {'uuid': self.uuid, 'format': format, 'bitrate': bitrate})

    @models.permalink
    def get_waveform_url(self):
        return ('alibrary-media-waveform', [self.uuid])
    

    def get_api_url(self):
        return reverse('api_dispatch_detail', kwargs={  
            'api_name': 'v1',  
            'resource_name': 'library/track',
            'pk': self.pk  
        }) + ''
    
    def release_link(self):
        if self.release:
            return '<a href="%s">%s</a>' % (reverse("admin:alibrary_release_change", args=(self.release.id,)), self.release.name)
        return None
    
    release_link.allow_tags = True
    release_link.short_description = "Edit" 
    
    def get_playlink(self):
        return '/api/tracks/%s/#0#replace' % self.uuid
    
    
    def get_download_permissions(self):
        pass
    


    def generate_sha1(self):
        return sha1_by_file(self.master)
    

    @property
    def has_video(self):
        return self.relations.filter(service__in=['youtube', 'vimeo']).count() > 0

    @property
    def get_videos(self):
        return self.relations.filter(service__in=['youtube', 'vimeo'])


    @property
    def has_soundcloud(self):
        return self.relations.filter(service='soundcloud').exists()

    @property
    def get_soundcloud(self):
        return self.relations.filter(service='soundcloud').all()[0]
    

    # TODO: still needed?
    def get_products(self):
        return self.mediaproduct.all()
    
    
    # TODO: still needed?
    def get_download_url(self, format, version):
        
        return '%sdownload/%s/%s/' % (self.get_absolute_url(), format, version)
    
    
    def get_master_path(self):
        try:
            return self.master.path
        except Exception, e:
            log.warning('unable to get master path for: %s' % self.name)


    def get_directory(self, absolute=False):

        if self.folder and absolute:
            return os.path.join(settings.MEDIA_ROOT, self.folder)

        elif self.folder:
            return self.folder

        else:
            log.warning('unable to get directory path for: %s - %s' % (self.pk, self.name))
            return None


    
    # full absolute path
    def get_folder_path(self, subfolder=None):
        
        if not self.folder:
            return None
        
        if subfolder:
            folder = "%s/%s%s/" % (MEDIA_ROOT, self.folder, subfolder)
            if not os.path.isdir(folder):
                try:
                    os.mkdir(folder, 0755)
                except Exception, e:
                    pass
                
            return folder
                    
        return "%s/%s" % (MEDIA_ROOT, self.folder)
    
    """
    gets the 'real' file, eg flac-master, stream-preview etc.
    """
    def get_file(self, source, version):
        # TODO: implement...
        return self.master
    
    def get_stream_file(self, format, version):
        # TODO: improve...
        
        if format == 'mp3' and version == 'base':
            ext = os.path.splitext(self.master.path)[1][1:].strip() 
            if ext == 'mp3':
                return self.master
        
        filename = str(version) + '.' + str(format)
        file = File.objects.get(original_filename=filename, folder=self.folder)
        
        return file.file
    
    
    def get_default_stream_file(self):
        return self.get_stream_file('mp3', 'base')



    # TODO: depreciated version - remove
    """
    def get_cache_file(self, format, version):
        
        filename = str(version) + '.' + str(format)
        
        full_path = "%s%s" % (self.get_folder_path('cache'), filename)
        
        if not os.path.isfile(full_path):
            return None
        
        return full_path
    """

    def get_cache_file(self, format, version='base', absolute=True):

        versions_directory = os.path.join(self.get_directory(absolute=absolute), 'versions')
        path = os.path.join(versions_directory, '%s.%s' % (version, format))
        if absolute:
            path = os.path.join(settings.MEDIA_ROOT, path)
            if os.path.isfile(path):
                return path
        else:
            if os.path.isfile(os.path.join(settings.MEDIA_ROOT, path)):
                return path



        return None

    def get_playout_file(self, absolute=False):

        # at the moment unified to mp3 format
        abs_path = os.path.join(self.get_directory(absolute=True), 'versions', 'base.mp3')
        if os.path.islink(abs_path):
            abs_path = self.master.path

        if not absolute:
            abs_path = abs_path.replace(settings.MEDIA_ROOT + '/', '')

        return abs_path




    def get_waveform_image(self):
        
        waveform_image = self.get_cache_file('png', 'waveform')
        
        if not waveform_image:
            try:
                self.create_waveform_image.delay(self)
                waveform_image = None
                # waveform_image = self.get_cache_file('png', 'waveform')
            except Exception, e:
                log.warning('unable to request wafeform image for pk: %s' % self.pk)
                waveform_image = None
            
        return waveform_image
        

        
    def get_duration(self, units='ms'):
        duration = None
        if self.base_duration:
            if self.base_duration > 5:
                duration = self.base_duration * 1000

        if not self.master:
            return None


        if not duration:
            log.debug('duration from ffmpeg')
            from alibrary.util.duration import duration_ffmpeg
            duration = duration_ffmpeg(self.master.path)

        if not duration:
            log.debug('duration from audiotools')
            try:
                duration = self.get_audiofile().seconds_length() * 1000
            except Exception, e:
                log.warning('unable to get duration with audiotools: %s' % e)

        if duration and units == 'ms':
            return int(duration)

        if duration and units == 's':
            return duration / 1000

        return None
    
    """
    shortcut to audiotools api
    """
    def get_audiofile(self):

        try:
            return audiotools.open(self.get_master_path())

        except Exception, e:
            log.warning('unable to get audiofile audiotools: %s' % e)
            return None
        
        
        
        
    @property
    def appearances(self):
        return self.get_appearances()
        
    def get_appearances(self):
        ps = []
        try:
            pis = PlaylistItem.objects.filter(object_id=self.pk, content_type=ContentType.objects.get_for_model(self))
            ps = Playlist.objects.exclude(type='other').filter(items__in=pis).order_by('-type', '-created',).distinct()
        except Exception, e:
            print '### get_appearances error: %s' % e
            pass
        
        return ps
        
        
    
        
    
    """
    Conversion flow:
     - create target folder
       ***/cache/<media uuid>/
    
     - src -> temp-file in destination format (eg /tmp/xyz-tempfile.mp3)
     - add file to filer-folder (think about creating filermodel for cache-file)
     
    """
    # send task to celeryd
    # @task
    def convert(self, format, version):
        
        log = logging.getLogger('alibrary.mediamodels.convert')
        
        log.info('Media id: %s - Encoder: %s/%s' % (self.pk, format, version))
        
        status = 0
        
        dst_file = str(version) + '.' + str(format)
        #src_path = self.master.path
        src_path = self.get_master_path()
    
        tmp_directory = tempfile.mkdtemp()
        tmp_path = tmp_directory + '/' + dst_file
        
        log.info('Media id: %s - dst_file: %s' % (self.pk, dst_file))
        log.info('Media id: %s - src_path: %s' % (self.pk, src_path))
        log.info('Media id: %s - tmp_path: %s' % (self.pk, tmp_path))
        
        
        """
        print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        print 'Media id: %s - dst_file: %s' % (self.pk, dst_file)
        print 'Media id: %s - src_path: %s' % (self.pk, src_path)
        print 'Media id: %s - tmp_path: %s' % (self.pk, tmp_path)
        """

    
        """
        get duration (removed)
        # TODO: refactor to @property
        if not self.duration:
            try:
                self.duration = int(self.get_audiofile().seconds_length() * 1000)
            except Exception, e:
                print e
                self.duration = 0
        """
        
        """
        create a converted version of the master, stored in temp location
        """
        #try:
        print '*******************************************************'
        print 'Tmp file at: %s' % tmp_path
        print 'Source file at: %s' % src_path
        print 'Destination file at: %s' % dst_file
        print '*******************************************************'

        skip_conversion = False
        if format == 'mp3':
            # TODO: make compression variable / configuration dependant
            
            compression = '2'

            
            print 'Version: %s' % version

            if version == 'base':
                
                # skip conversino in case of mp3 - just use the original file
                ext = os.path.splitext(src_path)[1][1:].strip() 
                if ext == 'mp3':
                    print 'skip conversion - mp3 > mp3'
                    tmp_path = src_path
                    skip_conversion = True
                
                compression = '0'
                
            if version == 'low':
                compression = '6'
            
            
            
            if not skip_conversion:
                print '> AUDIOTOOLS: conversion to mp3'
                audiotools.open(src_path).convert(tmp_path, audiotools.MP3Audio, compression=compression, progress=self.convert_progress)

        
        if format == 'flac':
            # TODO: make compression variable / configuration dependant
            print '> AUDIOTOOLS: conversion to flac'
            audiotools.open(src_path).convert(tmp_path, audiotools.FlacAudio, progress=self.convert_progress)

        
        converted = True
        
        print '* END OF CONVERSION *******************************************'
        
        """
        finaly create a django file object and attach it to the medias cache folder
        """
        try:
            
            dst_final = self.get_folder_path('cache')
            
            print "Final Source: %s" % tmp_path
            print "Final Destination: %s" % dst_final + dst_file
            
            # TODO: just create a symlink in case of mp3
            # shutil.copy2(tmp_path, dst_final + dst_file)

            if skip_conversion:
                print "o conversion -> just symlinking to cache folder"
                if not os.path.lexists(dst_final + dst_file):
                    os.symlink(tmp_path, dst_final + dst_file)
            else:
                shutil.copy2(tmp_path, dst_final + dst_file)
            
            #tmp_file = DjangoFile(open(tmp_path), name=dst_file)


            status = 1
        
        except Exception, e:
            print "error adding file to the cache :( "
            status = 2
            print e
        
        
        """
        cleanup temp-files
        """
        try:
            shutil.rmtree(tmp_directory)
            pass
        except Exception, e:
            print e

        
        return status
        
        

    @task
    def grappher(self, width, height):
        """
        
        """
        pass
    
    
    @task
    def create_waveform_image(self):

        if self.master:
            tmp_directory = tempfile.mkdtemp()
    
            src_path = self.master.path;
            tmp_path = os.path.join(tmp_directory, 'tmp.wav')

            versions_directory = os.path.join(self.get_directory(absolute=True), 'versions')
            dst_path = os.path.join(versions_directory, 'waveform.png')
            
            #print 'create waveform'
            print 'src_path: %s' % src_path
            #print 'tmp_path: %s' % tmp_path
            print 'dst_path: %s' % dst_path

            """
            first try to convert using audiotools.
            if this fails, we try to force the process 'by hand'
            """

            try:
                log.debug('trying to convert to .wav using audiotools: %s' % src_path)
                audiotools.open(src_path).convert(tmp_path, audiotools.WaveAudio)
            except Exception, e:
                log.warning('unable to convert with audiotools: %s' % e)

                ext = os.path.splitext(src_path)[1]
                log.debug('have "%s" format' % ext)

                """
                different processing depending on audio format
                """
                if ext in ['.m4a', '.mp4']:
                    # decode using faad
                    pass
                elif ext in ['.mp5',]:
                    # just a placeholder
                    pass
                else:
                    # use lame for the rest
                    sox_binary = alibrary_settings.LAME_BINARY
                    log.debug('running: "%s %s %s"' % (sox_binary, src_path, tmp_path))

                    p = subprocess.Popen([
                        sox_binary, src_path, tmp_path
                    ], stdout=subprocess.PIPE)
                    stdout = p.communicate()

            

            
            args = (tmp_path, dst_path, None, 1800, 301, 2048)
            create_wave_images(*args)
            
            try:
                shutil.rmtree(tmp_directory)
            except Exception, e:

                print e
            
        return

 
       
    #@task
    def build_cache(self):
        
        # get settings
        formats_download = FORMATS_DOWNLOAD 
        waveform_sizes = WAVEFORM_SIZES
        
        
        # cleanup:
        # delete everything that 'could' be in the cache so far...
        print '# formats_download:'

        for format, variations in formats_download.iteritems():
            for variation in variations:
                
                filename = '%s_%s.%s' % ('download', variation, format)
                tmp_directory = self.convert_(filename, self.folder, format, variation)
                
                
                """
                if sucessfully converted, create a django/filer file from temp_file
                """
                if tmp_directory:
                    tmp_path =  tmp_directory + '/' + filename
                    try:
                        tmp_file = DjangoFile(open(tmp_path),name=filename)            
                        file, created = File.objects.get_or_create(
                                                        original_filename=tmp_file.name,
                                                        file=tmp_file,
                                                        folder=self.folder,
                                                        is_public=False)
                        self.status = 1
                    
                    except Exception, e:
                        self.status = 2
                        print e
                        
                        

                try:
                    shutil.rmtree(tmp_directory)
                except Exception, e:
                    print e
                    
                    
                self.save()
            
            

        
        
        # convert:
        # get needed output-formats
        
        
        # grappher:
        # get needed output-formats
        
        
        
        pass


    # TODO: implement!
    # access media versions
    def get_version(self, bitrate=320, format='mp3', absolute=False):

        path = ''

        if absolute:
            path = os.path.join(settings.MEDIA_ROOT, path)

        return path
       
       
       
    # create converted (mp3) versions of master file
    def create_versions(self):

        log.info('create versions for: %s | %s' % (self.pk, self.name))
        if USE_CELERYD:
            self.create_versions_task.delay(self)
        else:
            self.create_versions_task(self)

    # create converted (mp3) versions of master file
    @task
    def create_versions_task(obj):

        """
        for the moment we either
         - create a high-quality mp3 in case of non-MP3 files
         - or symlink the file if it is an MP3 already

         'versions' are stored in the sub-directory 'versions', following the pattern:
         <base/or/bitrate>.mp3
        """

        SUPPORTED_FORMATS = ['mp3', 'flac', 'aif', 'aiff', 'mp4', 'm4a', 'ogg', 'vorbis', 'wav']

        # check if 'versions' directory exists - if not create it
        versions_directory = os.path.join(obj.get_directory(absolute=True), 'versions')
        log.debug('versions directory: %s' % versions_directory)
        if versions_directory:
            if not os.path.exists(versions_directory):
                try:
                    os.makedirs(versions_directory, 0755)
                except:
                    pass

        else:
            log.warning('unable to create verisons dir: %s' % versions_directory)
            return

        # remove current files
        for file in os.listdir(versions_directory):
            file_path = os.path.join(versions_directory, file)
            try:
                log.debug('unlinking: %s' % file_path)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception, e:
                log.warning('unable to unlink: %s - %s' % (file_path, e))


        # check type of source file
        if not obj.master:
            raise Exception('master needed for conversion')

        if not os.path.isfile(obj.master.path):
            raise IOError('file does not exist: %s' % obj.master.path)


        master_format = os.path.splitext(obj.master.path)[1][1:].strip().lower()
        version_path = os.path.join(versions_directory, 'base.mp3')


        if not master_format in SUPPORTED_FORMATS:
            raise IOError('format not supported: %s' % obj.master.path)

        if master_format == 'mp3':
            log.debug('in MP3 format already: symlinking to vorsions folder: %s' % obj.master)
            if not os.path.lexists(version_path):
                os.symlink(obj.master.path, version_path)

        else:
            log.info('conversion needed: %s to MP3' % master_format)
            try:
                audiotools.open(obj.master.path).convert(
                    version_path,
                    audiotools.MP3Audio, compression=0, progress=audiotools_progress)
            except Exception, e:
                log.warning('audiotools exception: %s' % e)

                try:
                    log.info('trying with lame: %s' % alibrary_settings.LAME_BINARY)
                    p = subprocess.Popen([
                        alibrary_settings.LAME_BINARY, obj.master.path, version_path
                    ], stdout=subprocess.PIPE)
                    stdout = p.communicate()
                    print stdout
                except Exception, e:
                    log.warning('lame did fail as well: %s' % e)





            if os.path.isfile(version_path):
                log.info('conversion complete: %s' % version_path)
            else:
                log.warning('unable to convert: %s to MP3' % master_format)



        # self-check
        if os.path.isfile(version_path) or os.path.lexists(version_path):
            log.info('media %s - versions created' % obj.pk)
            obj.conversion_status = 1
            obj.save()
        else:
            log.warning('media %s - error creating versions' % obj.pk)
            obj.conversion_status = 99
            obj.save()






            
    """
    progress/callback functions
    TODO: unify calls
    """
    def convert_progress(self, x, y):
        p = (x * 100 / y)
        if (p%10) == 0:
            print p

        
    def progress_callback(self, percentage):
        pass
        #print 'waveform:',
        #print str(percentage)

    

    # TODO: depreciated
    def generate_media_versions(self):
        log = logging.getLogger('alibrary.mediamodels.generate_media_versions')
        self.generate_media_versions_task.delay(self)

    @task
    def generate_media_versions_task(obj):
        
        log = logging.getLogger('alibrary.mediamodels.generate_media_versions_task')
        
        log.info('Start conversion for Media: %s' % (obj.pk))
        print 'Start conversion for Media: %s' % (obj.pk)
        
        print 
        print '************************************************************'
        print 'Delete files from cache folder'
        folder = obj.get_folder_path('cache')
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            try:
                print 'Unlinking: %s' % file_path
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception, e:
                print e
        
        
        
        print 'Sleeping 0.2 secs.. To be sure the transaction is completed.'
        time.sleep(0.2)
        print
        

        formats_media = FORMATS_MEDIA
        
        for source, versions in formats_media.iteritems():
            for version in versions:
                print 'Media id: %s - Sending to Encoder: %s/%s' % (obj.pk, source, version)
                log.info('Media id: %s - Sending to Encoder: %s/%s' % (obj.pk, source, version))
                try:
                    obj.convert(source, version)
                except Exception, e:
                    print e
                    pass

        
        # check if everything went fine (= if cache files available)

        c = obj.get_cache_file('mp3', 'base')
        if c:
            print c            
            obj.conversion_status = 1;
            obj.save();
        else:
            obj.conversion_status = 2;
            obj.save();

        
        print "* EOL"
            
            




    def inject_metadata(self, format, version):
        
        """
        audiotools.MetaData
        """
        meta = MetaData()
        
        
        """
        prepare metadata object
        """
        # track-level metadata
        meta.track_name = self.name
        meta.track_number = self.tracknumber
        meta.media = 'DIGITAL'
        meta.isrc = self.isrc
        

            
        """ Needs fixing...
        for extra_artist in self.extra_artists.all():
            print extra_artist
        meta.performer_name =
        meta.composer_name =
        meta.conductor_name =
        """
        
        # release-level metadata
        if self.release:
            meta.album_name = self.release.name
            meta.catalog = self.release.catalognumber
            meta.track_total = len(self.release.media_release.all())
            
            if self.release.releasedate:
                try:
                    meta.year = str(self.release.releasedate.year)
                    meta.date = str(self.release.releasedate)
                    
                except Exception, e:
                    print e
            
            try:
                
                cover_image = self.release.cover_image if self.release.cover_image else self.release.main_image
                
                if meta.supports_images() and cover_image:
                    for i in meta.images():
                        meta.delete_image(i)
                        
                    opt = dict(size=(200, 200), crop=True, bw=False, quality=80)
                    image = get_thumbnailer(cover_image).get_thumbnail(opt)
                    meta.add_image(get_raw_image(image.path, 0))
                    
            except Exception, e:
                print e
                
            
        # artist-level metadata
        if self.artist:
            meta.artist_name = self.artist.name
                    
        # label-level metadata
        if self.release.label:
            pass
            # meta.artist_name = self.artist.name

        """
        get corresponding file and apply the metadata
        """
        cache_file = self.get_cache_file(format, version)
        try:
            audiotools.open(cache_file.path).set_metadata(meta)
        except Exception, e:
            print e
        return cache_file
    
    
    """
    creates an echoprint fp and post it to the 
    identification server
    """
    def update_echoprint(self):
        #self.update_echoprint_task.delay(self)
        self.update_echoprint_task(self)
        
    @task()
    def update_echoprint_task(obj):
        
        from settings import ECHOPRINT_CODEGEN_BIN

        status = 2
        
        
        ecb = ECHOPRINT_CODEGEN_BIN
        # ecb = 'echoprint-codegen'
        
        path = obj.get_master_path()

        if not path:
            log.warning('master_path not available: %s' % path)
            obj.echoprint_status = 2
            obj.save()
            return None

        log.debug('echoprint binary at: %s' % ecb)
        log.debug('update echoprint: %s' % path)

        p = subprocess.Popen([
            ecb, path,
        ], stdout=subprocess.PIPE)
        stdout = p.communicate()

        try:
            d = json.loads(stdout[0])
        except ValueError, e:
            log.error('unable to load JSON: %s' % e)
            log.error('stdout: %s' % stdout)

            return False

        # print d
        
        try:
            code = d[0]['code']
            version = d[0]['metadata']['version']
            duration = d[0]['metadata']['duration']
        except Exception, e:
            print e
            code = None
            version = None
            duration = None
            status = 2

        if code:
            
            try:
            
                print 'delete fingerprint on server id: %s' % obj.id 
                fp.delete("%s" % obj.id)
                
                print 'post new fingerprint:'
                code_pre = code
                id = obj.updated.isoformat('T')[:-7]
                id = obj.updated.isoformat()
                code = fp.decode_code_string(code)
                
                nfp = {
                        "track_id": "%s" % obj.id,
                        "fp": code,
                        #"artist": "%s" % obj.artist.id,
                        #"release": "%s" % obj.artist.id,
                        "track": "%s" % obj.uuid,
                        "length": duration,
                        "codever": "%s" % version,
                        "source": "%s" % "NRGFP",
                        "import_date": "%sZ" % id
                        }
                
                #print nfp
                
                print 'PRE INGEST'
                res = fp.ingest(nfp, split=False, do_commit=True)
                print 'POST INGEST'

                print 'getting code by id (check)'
    
                
                if fp.fp_code_for_track_id("%s" % obj.id):
                    print "ALL RIGHT!!! FP INSERTED!!"
                    status = 1
                    
                else:
                    status = 2
                    
                    
                    
                res = fp.best_match_for_query(code_string=code_pre)
                print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
                print res.score
                print res.match()
                print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
                    
                
                    
                    
                    
            except Exception, e:
                print e
                status = 2

        obj.echoprint_status = status
        obj.save()



    # Echoprint analyzer
    def echonest_analyze(self):

        log.info('Start echoprint_analyze: %s' % (self.pk))
        if USE_CELERYD:
            self.echonest_analyze_task.delay(self)
        else:
            self.echonest_analyze_task(self)

    @task
    def echonest_analyze_task(obj):

        ew = EchonestWorker()
        try:
            obj = ew.analyze(obj)
            obj.save()
        except Exception, e:
            print e




        
    def save(self, *args, **kwargs):

        log.debug('Media id: %s - Save' % (self.pk))

        # Assign a default license
        """ not applying default license anymore
        if not self.license:
            try:
                license = License.objects.filter(is_default=True)[0]
                self.license = license
                log.debug('applied default license: %s' % license.name)
            except Exception, e:
                log.warning('unable to apply default license: %s' % e)
        """
        

        # check if master changed. if yes we need to reprocess the cached files
        if self.uuid is not None:
            try:
                orig = Media.objects.filter(uuid=self.uuid)[0]
                if orig.master != self.master:
                    log.info('Media id: %s - Master changed from "%s" to "%s"' % (self.pk, orig.master, self.master))

                    # set 'original filename'
                    if not self.original_filename and self.master.name:
                        self.original_filename = self.master.name[0:250]

                    # reset processing flags
                    self.processed = 0
                    self.conversion_status = 0
                    self.echoprint_status = 0

            except Exception, e:
                pass
                #print e



        # sha1 for quick duplicate checks
        if self.master:
            self.master_sha1 = self.generate_sha1()
        else:
            self.master_sha1 = None


        unique_slugify(self, self.name)

        # update d_tags
        t_tags = ''
        for tag in self.tags:
            t_tags += '%s, ' % tag    
        
        self.tags = t_tags
        self.d_tags = t_tags

        # kind of ugly, clean empty relations
        for ea in MediaExtraartists.objects.filter(media=self):
            try:
                if not ea.artist:
                    ea.delete()
            except:
                pass

        super(Media, self).save(*args, **kwargs)




        
# media post save
@disable_for_loaddata
def media_post_save(sender, **kwargs):

    obj = kwargs['instance']
    log.info('Media id: %s - Processed state: %s' % (obj.pk, obj.processed))

    # create object directory ?
    if not obj.folder:
        log.debug('no directory for media %s - create it.' % obj.pk)
        directory = get_dir_for_object(obj)
        abs_directory = os.path.join(settings.MEDIA_ROOT, directory)

        try:
            if not os.path.exists(abs_directory):
                os.makedirs(abs_directory, 0755)

            obj.folder = directory
            log.info('creating directory: %s' % abs_directory)

            obj.save()

        except Exception, e:
            log.warning('unable to create directory: %s - %s' % (abs_directory, e))
            obj.folder = None
            obj.status = 99
            obj.save()


    if obj.status == 99:
        log.warning('media %s - status is error > return' % obj.pk)
        return


    # extract files 'hard facts'
    if obj.master and obj.processed != 1 and obj.processed != 99:
        log.info('Media id: %s - reprocess master at: %s' % (obj.pk, obj.master.path))

        try:
            obj.base_format = os.path.splitext(obj.master.path)[1][1:].lower()

            audiofile = audiotools.open(obj.master.path)

            obj.base_bitrate = audiofile.bits_per_sample()
            obj.base_samplerate = audiofile.sample_rate()
            obj.base_filesize = os.path.getsize(obj.master.path)
            obj.base_duration = audiofile.seconds_length()

            obj.processed = 1 # done

        except Exception, e:

            log.warning('media %s - unable to process: %s' % (obj.pk, e))

            obj.base_format = None
            obj.base_bitrate = None
            obj.base_samplerate = None
            obj.base_filesize = None
            obj.base_duration = None
            obj.processed = 99 # error

        obj.save()



    """
    # save/create directory
    if not obj.folder and obj.master:
        folder = "private/%s/" % (obj.uuid.replace('-', '/')[5:])
        log.info('Adding folder: %s' % (folder))
        obj.folder = folder
        obj.save()
    """

    if obj.master and obj.echoprint_status == 0:
        if AUTOCREATE_ECHOPRINT:
            log.info('Media id: %s - Echoprint' % (obj.pk))
            obj.update_echoprint()
        else:
            log.info('Media id: %s - skipping echoprint generation' % (obj.pk))

    # TODO: investigate!
    #if obj.master and obj.conversion_status == 0 and obj.echoprint_status != 0:
    if obj.master and obj.conversion_status == 0:
        log.info('Media id: %s - re-process conversion' % (obj.pk))
        obj.create_versions()
        """
        # TODO: depreciate
        obj.generate_media_versions()
        """

post_save.connect(media_post_save, sender=Media) 
        

def media_pre_delete(sender, **kwargs):
    
    log = logging.getLogger('alibrary.mediamodels.media_pre_delete')
    obj = kwargs['instance']

    # try to delete fingerprint
    try:
        log.info('delete fingerprint on server id: %s' % obj.id)
        fp.delete("%s" % obj.id)
    except Exception, e:
        log.warning('unable to delete fingerprint for media_id: %s - %s' % (obj.id, e))

pre_delete.connect(media_pre_delete, sender=Media)

from actstream import action
@disable_for_loaddata
def action_handler(sender, instance, created, **kwargs):

    if instance.get_last_editor() and instance.status == 1:
        log.debug('last editor seems to be: %s' % instance.get_last_editor())
        try:
            action.send(instance.get_last_editor(), verb='updated', target=instance)
        except Exception, e:
            print 'error calling action_handler: %s' % e

post_save.connect(action_handler, sender=Media)



arating.enable_voting_on(Media)

try:
    tagging.register(Media)
except:
    pass



class MediaExtraartists(models.Model):
    artist = models.ForeignKey('Artist', related_name='extraartist_artist', on_delete=models.CASCADE, blank=True, null=True)
    media = models.ForeignKey('Media', related_name='extraartist_media', on_delete=models.CASCADE, blank=True, null=True)
    # function = models.CharField(max_length=128, blank=True, null=True)
    profession = models.ForeignKey(Profession, verbose_name='Role/Profession', related_name='media_extraartist_profession', blank=True, null=True)

    class Meta:
        app_label = 'alibrary'
        ordering = ('artist__name', 'profession__name', )

    def __unicode__(self):
        if self.artist and self.profession:
            return 'Credited "%s" as "%s"' % (self.artist.name, self.profession.name)
        elif self.artist:
            return 'Credited "%s"' % (self.artist.name)
        else:
            return 'Credited "%s"' % self.pk





    
    


"""
CMS-Plugins
"""
class MediaPlugin(CMSPlugin):
    
    media = models.ForeignKey(Media)
    
    headline = models.BooleanField(verbose_name=_('Show headline (Track/Artist)'), default=False)
    
    def __unicode__(self):
        return self.media.name

    # meta
    class Meta:
        app_label = 'alibrary'


    
def get_raw_image(filename, type):
    try:
        f = open(filename, 'rb')
        data = f.read()
        f.close()

        return audiotools.Image.new(data, u'', type)
    except IOError:
        raise audiotools.InvalidImage(_(u"Unable to open file"))