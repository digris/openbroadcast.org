# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
import os
import shutil
import uuid
import audiotools
import tempfile
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _
from django.dispatch import receiver
from django.db.models.signals import post_save
from celery import current_app
from celery.contrib.methods import task_method
from util.conversion import any_to_wav
from util.grapher import create_waveform_image, create_spectrogram_image
log = logging.getLogger(__name__)

BASE_DIR = getattr(settings, 'BASE_DIR', None)
USE_CELERY = getattr(settings, 'MEDIA_ASSET_USE_CELERY', False)
ASSET_DIR = os.path.join(BASE_DIR, 'media', 'media_asset')

class WaveformManager(models.Manager):

    def get_or_create_for_media(self, media, type, **kwargs):
        waveform, created = self.model.objects.get_or_create(media=media, type=type, **kwargs)
        log.debug('get_or_create_for_media: %s %s (created: %s)' % (media, type, created))
        return waveform

class Waveform(models.Model):

    INIT = 0
    DONE = 1
    PROCESSING = 2
    ERROR = 99
    STATUS_CHOICES = (
        (INIT, _(u'initial')),
        (DONE, _(u'completed')),
        (PROCESSING, _(u'processing')),
        (ERROR, _(u'error')),
    )

    WAVEFORM = 'w'
    SPECTROGRAM = 's'
    TYPE_CHOICES = (
        (WAVEFORM, _(u'Waveform')),
        (SPECTROGRAM, _(u'Spectrogram')),
    )

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    status = models.PositiveIntegerField(default=INIT, choices=STATUS_CHOICES)
    type = models.CharField(max_length=64, default=WAVEFORM, choices=TYPE_CHOICES)
    media = models.ForeignKey('alibrary.Media', null=True, related_name='versions', on_delete=models.CASCADE)

    objects = WaveformManager()

    class Meta:
        app_label = 'media_asset'
        verbose_name = _('Waveform')

    def __unicode__(self):
        return '%s - %s' % (self.uuid, self.type)

    @property
    def directory(self):
        return os.path.join(ASSET_DIR, 'waveform', self.media.uuid.replace('-', '/'))

    @property
    def path(self):
        return os.path.join(self.directory, self.type + '.png')

    @current_app.task(filter=task_method, name='Waveform.process_waveform')
    def process_waveform(self):

        # e.v. refactor later, so obj instead of self...
        obj = self

        log.debug('processing waveform for media with pk: %s' % obj.media.pk)
        tmp_directory = tempfile.mkdtemp()
        tmp_path = os.path.join(tmp_directory, 'tmp.wav')
        wav_path = any_to_wav(src=obj.media.master.path, dst=tmp_path)

        if not os.path.isdir(obj.directory):
            os.makedirs(obj.directory)

        if obj.type == 'w':
            create_waveform_image(wav_path, obj.path)

        elif obj.type == 's':
            create_spectrogram_image(wav_path, obj.path)

        else:
            raise NotImplementedError('type %s not implemented' % obj.type)

        shutil.rmtree(tmp_directory)

@receiver(post_save, sender=Waveform)
def waveform_post_save(sender, instance, created, **kwargs):
    obj = instance
    log.info('waveform_post_save - created: %s' % created)
    if created or 1 == 1:
        if USE_CELERY:
            log.debug('sending job to task queue')
            obj.process_waveform.apply_async()
        else:
            log.debug('processing task in foreground')
            obj.process_waveform()




class FormatManager(models.Manager):

    def get_or_create_for_media(self, media, encoding, quality, **kwargs):

        version, created = self.model.objects.get_or_create(media=media, encoding=encoding, quality=quality, **kwargs)
        log.debug('get_or_create_for_media: %s %s %s (created: %s)' % (media, encoding, quality, created))

        return version


class Format(models.Model):

    INIT = 0
    DONE = 1
    PROCESSING = 2
    ERROR = 99
    STATUS_CHOICES = (
        (INIT, _(u'initial')),
        (DONE, _(u'completed')),
        (PROCESSING, _(u'processing')),
        (ERROR, _(u'error')),
    )

    MP3 = 'mp3'
    AAC = 'aac'
    ENCODING_CHOICES = (
        (MP3, _(u'MP3')),
        (AAC, _(u'AAC')),
    )

    DEFAULT = 'default'
    LOFI = 'lo'
    HIFI = 'hi'
    PREVIEW = 'preview'
    QUALITY_CHOICES = (
        (DEFAULT, _(u'Default')),
        (LOFI, _(u'Lo-Fi')),
        (HIFI, _(u'Hi-Fi')),
        (PREVIEW, _(u'Preview')),
    )

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    status = models.PositiveIntegerField(default=INIT, choices=STATUS_CHOICES)
    encoding = models.CharField(max_length=4, default=MP3, choices=ENCODING_CHOICES, db_index=True)
    quality = models.CharField(max_length=16, default=DEFAULT, choices=QUALITY_CHOICES, db_index=True)

    media = models.ForeignKey('alibrary.Media', null=True, related_name='formats', on_delete=models.CASCADE)

    objects = FormatManager()

    class Meta:
        app_label = 'media_asset'
        verbose_name = _('Format')

    def __unicode__(self):
        return '%s - %s - %s' % (self.uuid, self.encoding, self.quality)

    @property
    def directory(self):
        return os.path.join(ASSET_DIR, 'format', self.quality, self.encoding, self.media.uuid.replace('-', '/'))

    @property
    def path(self):
        return os.path.join(self.directory, self.quality + '.' + self.encoding)

    @current_app.task(filter=task_method, name='Format.process_format')
    def process_format(self):

        # e.v. refactor later, so obj instead of self...
        obj = self

        log.debug('processing format for media with pk: %s' % obj.media.pk)
        tmp_directory = tempfile.mkdtemp()
        tmp_path = os.path.join(tmp_directory, 'tmp.wav')
        wav_path = any_to_wav(src=obj.media.master.path, dst=tmp_path)

        if not os.path.isdir(obj.directory):
            os.makedirs(obj.directory)

        shutil.rmtree(tmp_directory)

#@receiver(post_save, sender=Format)
def format_post_save(sender, instance, created, **kwargs):
    obj = instance
    log.info('format_post_save - created: %s' % created)
    if created or 1 == 1:
        if USE_CELERY:
            log.debug('sending job to task queue')
            obj.process_format.apply_async()
        else:
            log.debug('processing task in foreground')
            obj.process_format()
