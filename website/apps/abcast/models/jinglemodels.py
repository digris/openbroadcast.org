# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""
models here nit in use currently. major refactoring required befor integrating
"""

import logging
import os
import shutil
import tempfile

import audiotools
from abcast.models import Station
from alibrary.models import Artist
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext as _
from django_extensions.db.fields import AutoSlugField
from mutagen import File as MutagenFile
from mutagen.easyid3 import EasyID3
from base.mixins import TimestampedModelMixin, UUIDModelMixin

log = logging.getLogger(__name__)

MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT', None)

def clean_filename(filename):
    import unicodedata
    import string
    valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
    cleaned = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore')
    return ''.join(c for c in cleaned if c in valid_chars)

def masterpath_by_uuid(instance, filename):
    filename, extension = os.path.splitext(filename)
    folder = "private/%s/" % (instance.uuid.replace('-', '/')[5:])
    filename = u'master'
    return os.path.join(folder, "%s%s" % (clean_filename(filename).lower(), extension.lower()))


class JingleSet(TimestampedModelMixin, UUIDModelMixin, models.Model):

    name = models.CharField(
        max_length=200, db_index=True
    )
    slug = AutoSlugField(
        populate_from='name',
        editable=True, blank=True, overwrite=True
    )
    description = models.TextField(
        verbose_name="Extra Description",
        blank=True, null=True
    )
    main_image = models.ImageField(
        verbose_name=_('Image'),
        upload_to='abcast/station',
        null=True, blank=True
    )
    station = models.ForeignKey(
        Station,
        blank=True, null=True,
        related_name="jingleset_station",
        on_delete=models.SET_NULL
    )
    objects = models.Manager()

    class Meta:
        app_label = 'abcast'
        verbose_name = _('Jingle-Set')
        verbose_name_plural = _('Jingle-Sets')
        ordering = ('created', )

    def __unicode__(self):
        return self.name


class Jingle(TimestampedModelMixin, UUIDModelMixin, models.Model):

    name = models.CharField(max_length=200, db_index=True)
    slug = AutoSlugField(populate_from='name', editable=True, blank=True, overwrite=True)

    PROCESSED_CHOICES = (
        (0, _('Waiting')),
        (1, _('Done')),
        (2, _('Error')),
    )
    processed = models.PositiveIntegerField(default=0, choices=PROCESSED_CHOICES)

    CONVERSION_STATUS_CHOICES = (
        (0, _('Init')),
        (1, _('Completed')),
        (2, _('Error')),
    )
    conversion_status = models.PositiveIntegerField(default=0, choices=CONVERSION_STATUS_CHOICES)
    lock = models.PositiveIntegerField(default=0, editable=False)


    TYPE_CHOICES = (
        ('jingle', _('Jingle')),
        ('placeholder', _('Placeholder')),
    )
    type = models.CharField(verbose_name=_('Type'), max_length=12, default='jingle', choices=TYPE_CHOICES)
    description = models.TextField(verbose_name="Extra Description", blank=True, null=True)
    duration = models.PositiveIntegerField(verbose_name="Duration (in ms)", blank=True, null=True, editable=True)

    # relations
    user = models.ForeignKey(User, blank=True, null=True, related_name="jingle_user", on_delete=models.SET_NULL)
    artist = models.ForeignKey(Artist, blank=True, null=True, related_name='jingle_artist')
    set = models.ForeignKey(JingleSet, blank=True, null=True, related_name="jingle_set", on_delete=models.SET_NULL)

    master = models.FileField(max_length=1024, upload_to=masterpath_by_uuid, blank=True, null=True)
    master_sha1 = models.CharField(max_length=64, db_index=True, blank=True, null=True)
    folder = models.CharField(max_length=1024, null=True, blank=True, editable=False)
    objects = models.Manager()

    class Meta:
        app_label = 'abcast'
        verbose_name = _('Jingle')
        verbose_name_plural = _('Jingles')
        ordering = ('created', )

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return 'abjast-jingle-detail', [self.slug]

    @models.permalink
    def get_stream_url(self):
        return 'abjast-jingle-stream_html5', [self.uuid]

    @models.permalink
    def get_waveform_url(self):
        return 'abcast-jingle-waveform', [self.uuid]

    def get_folder_path(self, subfolder=None):
        if not self.folder:
            return None

        if subfolder:
            folder = "%s/%s%s/" % (MEDIA_ROOT, self.folder, subfolder)
            if not os.path.isdir(folder):
                os.mkdir(folder, 0755)
            return folder

        return "%s/%s" % (MEDIA_ROOT, self.folder)


    def get_cache_file(self, format, version):

        filename = str(version) + '.' + str(format)
        full_path = "%s%s" % (self.get_folder_path('cache'), filename)
        if not os.path.isfile(full_path):
            return None

        return full_path



    def get_waveform_image(self):

        waveform_image = self.get_cache_file('png', 'waveform')

        if not waveform_image:
            try:
                self.create_waveform_image()
                waveform_image = self.get_cache_file('png', 'waveform')
            except Exception as e:
                waveform_image = None

        return waveform_image

    #@task
    def create_waveform_image(self):

        raise NotImplemented('create_waveform_image not implemented for jingles yet')



    def process(self):
        iext = None
        try:
            iext = os.path.splitext(self.master.path)[1].lower()
            iext = iext[1:]
            audiofile = audiotools.open(self.master.path)

            base_format = iext
            base_bitrate = audiofile.bits_per_sample()
            base_samplerate = audiofile.sample_rate()
            base_filesize = os.path.getsize(self.master.path)
            base_duration = audiofile.seconds_length()

            try:
                base_duration = float(audiofile.total_frames()) / float(audiofile.sample_rate()) * 1000
                print 'frames: %s' % audiofile.total_frames()
                print 'rate: %s' % audiofile.sample_rate()
                print base_duration
                print
            except:
                pass

            self.processed = 1
        except Exception as e:
            print e
            base_bitrate = None
            base_samplerate = None
            base_filesize = None
            base_duration = None
            self.processed = 2

        """  
        self.base_format = iext
        self.base_bitrate = base_bitrate
        self.base_samplerate = base_samplerate
        self.base_filesize = base_filesize
        """
        self.duration = base_duration

        meta = None
        try:
            meta = EasyID3(self.master.path)
            log.debug('using EasyID3')
        except Exception as e:
            meta = MutagenFile(self.master.path)
            log.debug('using MutagenFile')


        if 'title' in meta:
            self.name = meta['title'][0]
        if 'artist' in meta:
            self.artist, created = Artist.objects.get_or_create(name=meta['artist'][0])

        self.save()

        try:
            self.create_waveform_image()
        except:
            pass
        return

    def save(self, *args, **kwargs):

        log.info('Jingle id: %s - Save' % self.pk)

        if self.uuid is not None:
            try:
                #orig = Media.objects.get(uuid=self.uuid)
                orig = Jingle.objects.filter(uuid=self.uuid)[0]
                if orig.master != self.master:
                    log.info('Jingle id: %s - master changed from "%s" to "%s"' % (self.uuid, orig.master, self.master))
                    self.processed = 0
                    self.conversion_status = 0

            except Exception as e:
                print e
                pass

        super(Jingle, self).save(*args, **kwargs)


def jingle_post_save(sender, **kwargs):

    obj = kwargs['instance']

    # save the folder path
    if not obj.folder and obj.master:
        folder = "private/%s/" % (obj.uuid.replace('-', '/'))
        log.info('Adding folder: %s' % folder)
        obj.folder = folder
        obj.save()

    #log.info('Jingle id: %s - Processed state: %s' % (obj.pk, obj.processed))

    if obj.master and obj.processed == 0:

        log.info('Media id: %s - Re-Process' % obj.pk)
        obj.process()


post_save.connect(jingle_post_save, sender=Jingle)
