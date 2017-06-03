# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import logging
import os
import subprocess
import uuid
import arating
import audiotools
import reversion
import tagging
from base.audio.fileinfo import FileInfoProcessor
from cacheops import invalidate_obj
from celery.task import task
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver
from django.utils.translation import ugettext as _
from django_extensions.db.fields import AutoSlugField
from django_extensions.db.fields.json import JSONField
from ep.API import fp
from lib.fields.languages import LanguageField
from base.signals.unsignal import disable_for_loaddata
from lib.util.sha1 import sha1_by_file
from tagging.registry import register as tagging_register
from alibrary import settings as alibrary_settings
from alibrary.models.basemodels import MigrationMixin, License, Relation, Profession
from alibrary.models.playlistmodels import PlaylistItem, Playlist
from alibrary.util.echonest import EchonestWorker
from alibrary.util.slug import unique_slugify
from alibrary.util.storage import get_dir_for_object

log = logging.getLogger(__name__)

USE_CELERYD = getattr(settings, 'ALIBRARY_USE_CELERYD', False)
AUTOCREATE_ECHOPRINT = getattr(settings, 'ALIBRARY_AUTOCREATE_ECHOPRINT', True)

LAME_BINARY = getattr(settings, 'LAME_BINARY')
SOX_BINARY = getattr(settings, 'SOX_BINARY')
FAAD_BINARY = getattr(settings, 'FAAD_BINARY')

LOOKUP_PROVIDERS = (
    #('discogs', _('Discogs')),
    ('musicbrainz', _('Musicbrainz')),
)

VERSION_CHOICES = (
    ('original', _('Original')),
    ('track', _('Track')),
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
            ('radioshow', _('Radio show')),
        )
    ),
    ('other', _('Other')),
    (None, _('Unknown')),
)


VALID_BITRATES = [
    56, 64, 96, 128, 160, 196, 256, 320
]

LOSSLESS_CODECS = [
    'wav', 'aif', 'aiff', 'flac',
]


def upload_master_to(instance, filename):
    filename, extension = os.path.splitext(filename)
    return os.path.join(get_dir_for_object(instance), 'master%s' % extension.lower())

class Media(MigrationMixin):

    STATUS_CHOICES = (
        (0, _('Init')),
        (1, _('Ready')),
        (3, _('Working')),
        (4, _('File missing')),
        (5, _('File error')),
        (99, _('Error')),
    )

    ECHOPRINT_STATUS_CHOICES = (
        (0, _('Init')),
        (1, _('Assigned')),
        (2, _('Error')),
        (3, _('File not suitable')),
        (99, _('Error')),
    )

    TRACKNUMBER_CHOICES = ((x, x) for x in range(1, 301))

    MEDIANUMBER_CHOICES = ((x, x) for x in range(1, 51))

    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False
    )
    lock = models.PositiveIntegerField(
        default=0, editable=False
    )
    name = models.CharField(
        max_length=255, db_index=True
    )
    slug = AutoSlugField(
        populate_from='name',
        editable=True, blank=True, overwrite=True
    )
    status = models.PositiveIntegerField(
        default=0,
        choices=STATUS_CHOICES
    )
    created = models.DateTimeField(
        auto_now_add=True, editable=False
    )
    updated = models.DateTimeField(
        auto_now=True, editable=False
    )
    publish_date = models.DateTimeField(
        blank=True, null=True
    )
    echoprint_status = models.PositiveIntegerField(
        default=0,
        choices=ECHOPRINT_STATUS_CHOICES
    )
    tracknumber = models.PositiveIntegerField(
        verbose_name=_('Track Number'),
        blank=True, null=True,
        choices=TRACKNUMBER_CHOICES
    )
    opus_number = models.CharField(
        max_length=200, blank=True, null=True
    )
    medianumber = models.PositiveIntegerField(
        verbose_name=_('a.k.a. "Disc number'),
        blank=True, null=True,
        choices=MEDIANUMBER_CHOICES
    )
    mediatype = models.CharField(
        verbose_name=_('Type'),
        max_length=128, default='song',
        choices=MEDIATYPE_CHOICES
    )
    version = models.CharField(
        max_length=12, blank=True, null=True,
        default='track',
        choices=VERSION_CHOICES
    )
    description = models.TextField(
        verbose_name="Extra Description / Tracklist",
        blank=True, null=True
    )
    lyrics = models.TextField(
        blank=True, null=True
    )
    lyrics_language = LanguageField(
        blank=True, null=True
    )

    duration = models.PositiveIntegerField(
        verbose_name="Duration (in ms)",
        blank=True, null=True, editable=False
    )

    # relations
    release = models.ForeignKey(
        'alibrary.Release',
        blank=True, null=True, on_delete=models.SET_NULL,
        related_name='media_release'
    )
    artist = models.ForeignKey(
        'alibrary.Artist',
        blank=True, null=True,
        related_name='media_artist'
    )

    # user relations
    owner = models.ForeignKey(
        User,
        blank=True, null=True, on_delete=models.SET_NULL,
        related_name="media_owner"
    )
    creator = models.ForeignKey(
        User,
        blank=True, null=True, on_delete=models.SET_NULL,
        related_name="media_creator"
    )
    last_editor = models.ForeignKey(
        User,
        blank=True, null=True, on_delete=models.SET_NULL,
        related_name="media_last_editor"
    )
    publisher = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL,
        related_name="media_publisher"
    )

    # identifiers
    isrc = models.CharField(
        verbose_name='ISRC',
        max_length=12, null=True, blank=True
    )

    # relations a.k.a. links
    relations = GenericRelation(Relation)
    playlist_items = GenericRelation(
        PlaylistItem,
        object_id_field="object_id"
    )

    # tagging (d_tags = "display tags")
    d_tags = tagging.fields.TagField(
        verbose_name="Tags",
        max_length=1024, blank=True, null=True
    )

    # provide 'multi-names' for artist crediting, like: Artist X feat. Artist Y & Artist Z
    media_artists = models.ManyToManyField(
        'alibrary.Artist',
        blank=True,
        through='MediaArtists',
        related_name="credited",
    )

    # extra-artists
    extra_artists = models.ManyToManyField(
        'alibrary.Artist',
        blank=True,
        through='MediaExtraartists'
    )

    license = models.ForeignKey(
        License,
        blank=True, null=True, on_delete=models.PROTECT,
        related_name='media_license',
        limit_choices_to={'selectable': True}
    )

    filename = models.CharField(
        verbose_name=_('Filename'),
        max_length=256, blank=True, null=True
    )
    original_filename = models.CharField(
        verbose_name=_('Original filename'),
        max_length=256, blank=True, null=True
    )

    folder = models.CharField(
        max_length=1024, null=True, blank=True, editable=False
    )

    #######################################################################
    # File Data
    #######################################################################
    base_format = models.CharField(
        verbose_name=_('Format'),
        max_length=12, blank=True, null=True
    )
    base_filesize = models.PositiveIntegerField(
        verbose_name=_('Filesize'),
        blank=True, null=True
    )
    base_duration = models.FloatField(
        verbose_name=_('Duration'),
        blank=True, null=True
    )
    base_samplerate = models.PositiveIntegerField(
        verbose_name=_('Samplerate'),
        blank=True, null=True
    )
    base_bitrate = models.PositiveIntegerField(
        verbose_name=_('Bitrate'),
        blank=True, null=True
    )

    #######################################################################
    # master audio-file data
    # TODO: all version- & conversion based data will be refactored.
    # the media model should just hold information about the associated master file
    #######################################################################
    master = models.FileField(max_length=1024, upload_to=upload_master_to, blank=True, null=True)
    master_sha1 = models.CharField(max_length=64, db_index=True, blank=True, null=True)
    master_encoding = models.CharField(max_length=16, blank=True, null=True)
    master_bitrate = models.PositiveIntegerField(verbose_name=_('Bitrate'), blank=True, null=True)
    master_filesize = models.PositiveIntegerField(verbose_name=_('Filesize'), blank=True, null=True)
    master_samplerate = models.PositiveIntegerField(verbose_name=_('Samplerate'), blank=True, null=True)
    master_duration = models.FloatField(verbose_name=_('Duration'), blank=True, null=True)

    #######################################################################
    # echonest data
    #######################################################################
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

    #######################################################################
    # fprint data
    #######################################################################
    fprint_ingested = models.DateTimeField(null=True, blank=True, editable=False)

    objects = models.Manager()

    class Meta:
        app_label = 'alibrary'
        verbose_name = _('Track')
        verbose_name_plural = _('Tracks')
        ordering = ('medianumber', 'tracknumber', 'name')

        permissions = (
            ('play_media', 'Play Track'),
            ('downoad_media', 'Download Track'),
            ('merge_media', 'Merge Tracks'),
            ('reassign_media', 'Re-assign Tracks'),
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
    def is_lossless(self):
        if self.master_encoding and self.master_encoding.lower() in LOSSLESS_CODECS:
            return True

    @property
    def bitrate(self):
        if not self.is_lossless:
            return self.master_bitrate

    @property
    def classname(self):
        return self.__class__.__name__


    @property
    def main_image(self):
        """main image referes to release image if available"""
        if self.release:
            return self.release.main_image

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

    def get_absolute_url(self):
        return reverse('alibrary-media-detail', kwargs={
            'pk': self.pk,
            'slug': self.slug,
        })

    def get_edit_url(self):
        return reverse("alibrary-media-edit", args=(self.pk,))

    def get_admin_url(self):
        return reverse("admin:alibrary_media_change", args=(self.pk,))


    # TODO: depreciated
    def get_stream_url(self):
        return reverse('alibrary-media-stream_html5', kwargs={'uuid': self.uuid})

    def get_api_url(self):
        return reverse('api_dispatch_detail', kwargs={
            'api_name': 'v1',
            'resource_name': 'library/track',
            'uuid': self.uuid
        })

    # TODO: refactor to admin module
    def release_link(self):
        if self.release:
            return '<a href="%s">%s</a>' % (reverse("admin:alibrary_release_change", args=(self.release.id,)), self.release.name)
        return None

    release_link.allow_tags = True
    release_link.short_description = "Edit"

    # TODO: depreciated
    def get_playlink(self):
        return '/api/tracks/%s/#0#replace' % self.uuid

    # TODO: depreciated
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

    """
    compose artist display as string
    """
    def get_artist_display(self):

        artist_str = ''
        artists = self.get_mediaartists()
        if len(artists) > 1:
            try:
                for artist in artists:
                    if artist['join_phrase']:
                        artist_str += ' %s ' % artist['join_phrase']
                    artist_str += artist['artist'].name
            except:
                artist_str = artists[0].name
        else:
            try:
                artist_str = artists[0].name
            except:

                try:
                    artist_str = self.artist.name
                except:
                    artist_str = _('Unknown Artist')

        return artist_str


    def get_mediaartists(self):

        artists = []
        if self.media_artists.count() > 0:
            for media_artist in self.media_mediaartist.all():
                artists.append({'artist': media_artist.artist, 'join_phrase': media_artist.join_phrase})
            return artists

        return artists


    def get_master_path(self):
        try:
            return self.master.path
        except Exception as e:
            log.warning('unable to get master path for: %s' % self.name)


    def get_directory(self, absolute=False):

        if self.folder and absolute:
            return os.path.join(settings.MEDIA_ROOT, self.folder)

        elif self.folder:
            return self.folder

        else:
            log.warning('unable to get directory path for: %s - %s' % (self.pk, self.name))
            return None


    def get_file(self, source, version):
        # TODO: implement...
        return self.master



    def get_playout_file(self, absolute=False):

        abs_path = self.master.path
        if not absolute:
            abs_path = abs_path.replace(settings.MEDIA_ROOT + '/', '')

        return abs_path

    def get_duration(self, units='ms'):

        if not self.master_duration:
            return

        if units == 'ms':
            return int(self.master_duration * 1000)

        if units == 's':
            return int(self.master_duration)


    """
    TODO: check usage.
    """
    @property
    def appearances(self):
        return self.get_appearances()

    def get_appearances(self):
        ps = []
        try:
            pis = PlaylistItem.objects.filter(object_id=self.pk, content_type=ContentType.objects.get_for_model(self))
            ps = Playlist.objects.exclude(type='other').filter(items__in=pis).order_by('-type', '-created',).nocache().distinct()
        except Exception as e:
            pass

        return ps


    """
    creates an echoprint fp and post it to the
    identification server
    """
    def update_echoprint(self):
        #self.update_echoprint_task.delay(self)
        self.update_echoprint_task(self)

    @task()
    def update_echoprint_task(obj):

        status = 2

        ECHOPRINT_CODEGEN_BINARY = getattr(settings, 'ECHOPRINT_CODEGEN_BINARY', None)

        log.debug('update echoprint, using binary: {}'.format(ECHOPRINT_CODEGEN_BINARY))

        path = obj.get_master_path()

        if not path:
            log.warning('master_path not available: %s' % path)
            obj.echoprint_status = 2
            obj.save()
            return None

        log.debug('update echoprint: %s' % path)
        #log.debug('codegen binary: %s' % ECHOPRINT_CODEGEN_BINARY)

        p = subprocess.Popen([
            ECHOPRINT_CODEGEN_BINARY, path,
        ], stdout=subprocess.PIPE, close_fds=True)
        stdout = p.communicate()

        try:
            d = json.loads(stdout[0])
        except ValueError as e:
            log.error('unable to load JSON: %s' % e)

            return False

        # print d

        try:
            code = d[0]['code']
            version = d[0]['metadata']['version']
            duration = d[0]['metadata']['duration']

        except Exception as e:
            log.error('unable to extract code: %s' % e)

            code = None
            version = None
            duration = None
            status = 2

        # skip file if longer than 12 minutes
        if duration and duration > (60 * 12):
            log.debug('file longer than 12 minutes > skipping echoprint ingestion')
            obj.echoprint_status = 3
            obj.save()
            return



        if code:

            try:

                fp.delete(b"%s" % obj.id)

                id = obj.updated.isoformat()
                code = fp.decode_code_string(code)

                nfp = {
                    b"track_id": "%s" % obj.id,
                    b"fp": code,
                    b"track": "%s" % obj.uuid,
                    b"length": duration,
                    b"codever": "%s" % version,
                    b"source": "%s" % "NRGFP",
                    b"import_date": "%sZ" % id
                }

                # ingest fingerprint into database
                fp.ingest(nfp, split=False, do_commit=True)

                # try to look up track by id
                code_for_track = fp.fp_code_for_track_id("%s" % obj.id)
                if code_for_track:
                    log.info('successfully ingested fingerprint for %s' % obj.id)
                    status = 1
                else:
                    log.warning('unable to ingest fingerprint for %s' % obj.id)
                    status = 2

            except Exception as e:
                log.warning('unable to ingest fingerprint: {}'.format(e))
                status = 2

        obj.echoprint_status = status
        obj.save()



    # echonest analyzer
    def echonest_analyze(self):

        log.info('Start echonest_analyze: %s' % (self.pk))
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


    def process_master_info(self, save=False):

        # read key information from master file
        if self.master:
            file_processor = FileInfoProcessor(self.master.path)
            if file_processor.audio_stream:
                self.master_encoding = file_processor.encoding
                self.master_filesize = file_processor.filesize
                self.master_bitrate = file_processor.bitrate
                self.master_samplerate = file_processor.samplerate
                self.master_duration = file_processor.duration

            else:
                log.warning('unable to process audio file')

            if save:
                self.save()




    def save(self, *args, **kwargs):

        # Assign a default license
        """
         - not applying default license anymore
         - applying default license again: #898
        """
        if not self.license:
            try:
                license = License.objects.filter(is_default=True)[0]
                self.license = license
                log.debug('applied default license: %s' % license.name)
            except Exception as e:
                log.warning('unable to apply default license: {}'.format(e))


        self.master_changed = False
        if self.uuid is not None:
            try:
                orig = Media.objects.filter(uuid=self.uuid)[0]
                if orig.master != self.master:
                    self.master_changed = True
            except:
                pass

        if self.master_changed:
            self.process_master_info()

        # check if master changed. if yes we need to reprocess the cached files
        if self.uuid is not None:

            try:
                orig = Media.objects.filter(uuid=self.uuid)[0]
                if orig.master != self.master:
                    log.info('Media id: %s - Master changed from "%s" to "%s"' % (self.pk, orig.master, self.master))

                    # set 'original filename'
                    if not self.original_filename and self.master.name:
                        try:
                            self.original_filename = self.master.name[0:250]
                        except Exception as e:
                            pass

                    # reset processing flags
                    # TODO: this should be refactored / removed. Only master_* related informations are extracted.
                    self.echoprint_status = 0

            except Exception as e:
                log.warning('unable to update master: {}'.format(e))

        if self.version:
            self.version = self.version.lower()

        if self.mediatype:
            self.mediatype = self.mediatype.lower()


        # sha1 for quick duplicate checks
        if self.master and not self.master_sha1:
            self.master_sha1 = self.generate_sha1()
        else:
            self.master_sha1 = None

        unique_slugify(self, self.name)

        # pretty of ugly, clean empty relations
        for ea in MediaExtraartists.objects.filter(media__pk=self.pk):
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

    if obj.master and obj.echoprint_status == 0:
        if AUTOCREATE_ECHOPRINT:
            log.info('Media id: %s - generate echoprint' % (obj.pk))
            obj.update_echoprint()
        else:
            log.info('Media id: %s - skipping echoprint generation' % (obj.pk))

    if not obj.folder:
        log.debug('no directory for media %s - create it.' % obj.pk)
        directory = get_dir_for_object(obj)
        abs_directory = os.path.join(settings.MEDIA_ROOT, directory)

        try:
            if not os.path.exists(abs_directory):
                os.makedirs(abs_directory, 0755)

            obj.folder = directory
            log.info('creating directory: %s' % abs_directory)

        except Exception as e:
            log.warning('unable to create directory: %s - %s' % (abs_directory, e))
            obj.folder = None
            obj.status = 99

    invalidate_obj(obj)

post_save.connect(media_post_save, sender=Media)


def media_pre_delete(sender, **kwargs):

    obj = kwargs['instance']

    # delete associated master file
    if obj.master and os.path.isfile(obj.master.path):
        os.unlink(obj.master.path)

    # try to delete fingerprint
    try:
        fp.delete(b"%s" % obj.id)
    except Exception as e:
        log.warning('unable to delete fingerprint for media_id: %s - %s' % (obj.id, e))

pre_delete.connect(media_pre_delete, sender=Media)



arating.enable_voting_on(Media)

try:
    tagging_register(Media)
except Exception as e:
    pass


class MediaExtraartists(models.Model):

    artist = models.ForeignKey(
        'alibrary.Artist',
        related_name='extraartist_artist',
        blank=True, null=True, on_delete=models.CASCADE
    )
    media = models.ForeignKey(
        'Media',
        related_name='extraartist_media',
        blank=True, null=True, on_delete=models.CASCADE
    )
    profession = models.ForeignKey(
        Profession,
        verbose_name='Role/Profession',
        related_name='media_extraartist_profession',
        blank=True, null=True
    )

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


@receiver(post_delete, sender=MediaExtraartists)
def media_extraartists_post_delete(sender, instance, **kwargs):
    # clear caches
    from alibrary.models import Artist
    Artist.get_releases.invalidate(instance.artist)
    Artist.get_media.invalidate(instance.artist)


class MediaArtists(models.Model):

    artist = models.ForeignKey(
        'alibrary.Artist',
        related_name='artist_mediaartist',
        on_delete=models.CASCADE
    )
    media = models.ForeignKey(
        'Media',
        related_name='media_mediaartist',
        on_delete=models.CASCADE
    )
    join_phrase = models.CharField(
        verbose_name="join phrase",
        max_length=12, blank=True, null=True,
        default=None,
        choices=alibrary_settings.ARTIST_JOIN_PHRASE_CHOICES
    )
    position = models.PositiveIntegerField(
        null=True, blank=True
    )

    class Meta:
        app_label = 'alibrary'
        verbose_name = _('Artist (title credited)')
        verbose_name_plural = _('Artists (title credited)')
        ordering = ('position', )


    def __unicode__(self):

        if self.join_phrase:
            return u'%s credited with "%s" on %s' % (self.artist, self.join_phrase, self.media)
        else:
            return u'%s on %s' % (self.artist, self.media)

@receiver(post_delete, sender=MediaArtists)
def media_artists_post_delete(sender, instance, **kwargs):

    # clear caches
    from alibrary.models import Artist
    Artist.get_releases.invalidate(instance.artist)
    Artist.get_media.invalidate(instance.artist)


def get_raw_image(filename, type):
    try:
        f = open(filename, 'rb')
        data = f.read()
        f.close()

        return audiotools.Image.new(data, u'', type)
    except IOError:
        raise audiotools.InvalidImage(_(u"Unable to open file"))
