# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import hashlib
import logging
import os
import shutil
import subprocess
import tempfile

from celery import current_app
from celery.task import task
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.core.cache import cache
from django.utils.translation import ugettext as _
from django.template import defaultfilters
from base.mixins import TimestampedModelMixin, UUIDModelMixin
from base.fs.utils import clean_directory_tree_reverse

#from .tasks import process_waveform_task, process_format_task

log = logging.getLogger(__name__)

BASE_DIR = getattr(settings, 'BASE_DIR', None)
USE_CELERYD = getattr(settings, 'MEDIA_ASSET_USE_CELERYD', False)

MEDIA_ASSET_KEEP_DAYS = getattr(settings, 'MEDIA_ASSET_KEEP_DAYS', 60)

MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT', None)
ASSET_DIR = os.path.join(MEDIA_ROOT, 'media_asset')
LAME_BINARY = getattr(settings, 'LAME_BINARY', 'lame')
SOX_BINARY = getattr(settings, 'SOX_BINARY')
FAAD_BINARY = getattr(settings, 'FAAD_BINARY')

FORMAT_LOCK_EXPIRE = 60 * 1

class WaveformManager(models.Manager):

    def get_or_create_for_media(self, media, type, **kwargs):
        wait = kwargs.pop('wait', False)
        waveform, created = self.model.objects.get_or_create(media=media, type=type, **kwargs)

        log.debug('waveform - get or create for media: %s %s wait: %s (created: %s)' % (media.uuid, type, wait, created))

        if wait and (created or waveform.status < Waveform.DONE):
            # non-async behaviour
            waveform.process_waveform()

        return waveform


class Waveform(UUIDModelMixin, TimestampedModelMixin, models.Model):

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

    status = models.PositiveIntegerField(default=INIT, choices=STATUS_CHOICES)
    type = models.CharField(max_length=64, default=WAVEFORM, choices=TYPE_CHOICES, db_index=True)
    accessed = models.DateTimeField(auto_now_add=True)
    media = models.ForeignKey('alibrary.Media', null=True, related_name='waveforms', on_delete=models.CASCADE)
    media_uuid = models.UUIDField(blank=True, null=True)

    objects = WaveformManager()

    class Meta:
        app_label = 'media_asset'
        verbose_name = _('Waveform')
        unique_together = ('media', 'type')

    def __unicode__(self):
        return '%s' % (self.get_type_display())

    @property
    def directory(self):
        uuid = '%s' % self.media_uuid

        """
        we need to insert an attitional directory here - as else 32000 fs limit (ext3) could make problems
        """
        dir = uuid.replace('-', '/')
        dir = dir[:2] + '/' + dir[2:4] + '/' + dir[4:6] + '/' + dir[6:]

        return os.path.join(ASSET_DIR, 'waveform', dir)

    @property
    def path(self):
        return os.path.join(self.directory, self.type + '.png')

    #@current_app.task(filter=task_method, name='Waveform.process_waveform')
    def process_waveform(self):

        from util.conversion import any_to_wav
        from util.grapher import create_waveform_image, create_spectrogram_image

        # e.v. refactor later, so obj instead of self...
        obj = self
        file_created = False

        log.debug('processing waveform for media with pk: %s' % obj.media.pk)
        tmp_directory = tempfile.mkdtemp()
        tmp_path = os.path.join(tmp_directory, 'tmp.wav')
        wav_path = any_to_wav(src=obj.media.master.path, dst=tmp_path)

        if not os.path.isdir(obj.directory):
            try:
                os.makedirs(obj.directory)
            except:
                pass

        if obj.type == 'w':
            create_waveform_image(wav_path, obj.path)

        elif obj.type == 's':
            create_spectrogram_image(wav_path, obj.path)

        else:
            raise NotImplementedError('type %s not implemented' % obj.type)

        shutil.rmtree(tmp_directory)

        if os.path.isfile(obj.path):
            obj.status = Waveform.DONE
        else:
            obj.status = Waveform.ERROR

        obj.save()

    def save(self, *args, **kwargs):

        self.do_process = False
        if self.pk is None or self.status == Waveform.INIT:
            #self.status = Waveform.PROCESSING
            self.do_process = True

        if not self.media_uuid:
            self.media_uuid = self.media.uuid

        super(Waveform, self).save(*args, **kwargs)


# @receiver(post_save, sender=Waveform)
# def waveform_post_save(sender, instance, created, **kwargs):
#     do_process = getattr(instance, 'do_process', False)
#     log.debug('waveform_post_save - processing required: %s' % do_process)
#     if do_process:
#         if USE_CELERYD:
#             log.debug('sending job to task queue')
#             process_waveform_task.apply_async((instance.media.pk,))
#             #obj.process_waveform.apply_async(queue='grapher')
#         else:
#             log.debug('processing task in foreground')
#             process_waveform_task(media_pk=instance.media.pk)
#             #obj.process_waveform()


@receiver(pre_delete, sender=Waveform)
def waveform_pre_delete(sender, instance, **kwargs):
    obj = instance
    if os.path.isfile(obj.path):
        os.remove(obj.path)
        clean_directory_tree_reverse(obj.path)


class FormatManager(models.Manager):

    def get_or_create_for_media(self, media, encoding='mp3', quality='default', **kwargs):
        wait = kwargs.pop('wait', False)
        format, created = self.model.objects.get_or_create(media=media, encoding=encoding, quality=quality, **kwargs)

        log.debug(
            'version - get or create for media: %s %s %s wait: %s (created: %s)' % (media.uuid, encoding, quality, wait, created))

        if wait and (created or format.status < Waveform.DONE):
            # non-async behaviour
            format.process_format()

        return format


class Format(UUIDModelMixin, TimestampedModelMixin, models.Model):

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



    LAME_OPTIONS = {
        DEFAULT: '-b 256',
        LOFI: '-b 96',
        HIFI: '-b 320',
        PREVIEW: '-b 24',
    }

    status = models.PositiveIntegerField(default=INIT, choices=STATUS_CHOICES, db_index=True)
    encoding = models.CharField(max_length=4, default=MP3, choices=ENCODING_CHOICES, db_index=True)
    quality = models.CharField(max_length=16, default=DEFAULT, choices=QUALITY_CHOICES, db_index=True)
    filesize = models.PositiveIntegerField(verbose_name=_('Filesize'), blank=True, null=True)
    accessed = models.DateTimeField(auto_now_add=True)
    media = models.ForeignKey('alibrary.Media', null=True, related_name='formats', on_delete=models.CASCADE)
    media_uuid = models.UUIDField(blank=True, null=True)

    objects = FormatManager()

    class Meta:
        app_label = 'media_asset'
        verbose_name = _('Format')
        unique_together = ('media', 'encoding', 'quality')

    def __unicode__(self):
        return '%s - %s' % (self.get_encoding_display(), self.get_quality_display())


    @property
    def directory(self):
        uuid = str(self.media_uuid)

        """
        we need to insert an attitional directory here - as else 32000 fs limit could make problems
        """
        dir = uuid.replace('-', '/')
        dir = dir[:2] + '/' + dir[2:4] + '/' + dir[4:6] + '/' + dir[6:]

        return os.path.join(ASSET_DIR, 'format', dir)


    @property
    def path(self):
        return os.path.join(self.directory, self.quality + '.' + self.encoding)


    @property
    def relative_path(self):
        # TODO: improve handling of absolute/relative path
        dir = str(self.media_uuid).replace('-', '/')
        dir = dir[:2] + '/' + dir[2:4] + '/' + dir[4:6] + '/' + dir[6:]

        return os.path.join('media_asset', 'format', dir, self.quality + '.' + self.encoding)


    @property
    def filesize_display(self):
        if self.filesize:
            return defaultfilters.filesizeformat(self.filesize)


    #@current_app.task(bind=True, filter=task_method, name='Format.process_format')
    def process_format(self):

        from util.conversion import any_to_wav

        # e.v. refactor later, so obj instead of self...
        obj = self
        processed = False

        log.debug('processing format for media with pk: %s' % obj.media.pk)

        Format.objects.filter(pk=obj.pk).update(status=Format.PROCESSING)

        tmp_directory = None

        if not os.path.isdir(obj.directory):
            os.makedirs(obj.directory)

        if obj.quality == Format.DEFAULT and obj.encoding == obj.media.master_encoding:
            processed = True
            log.info('identical encodeing for source and target. file will be copied untouched')
            shutil.copy(obj.media.master.path, obj.path)

        if not processed:

            tmp_directory = tempfile.mkdtemp()
            tmp_path = os.path.join(tmp_directory, 'tmp.wav')
            wav_path = any_to_wav(src=obj.media.master.path, dst=tmp_path)

            if obj.encoding == 'mp3':

                log.info('%s encoded version requested.' % obj.encoding)

                command = [
                    LAME_BINARY,
                    wav_path,
                    Format.LAME_OPTIONS[obj.quality],
                    '--quiet',
                    obj.path
                ]

                log.debug('running: %s' % ' '.join(command))

                p = subprocess.Popen(command, stdout=subprocess.PIPE)
                stdout = p.communicate()

        if tmp_directory and os.path.isdir(tmp_directory):
            shutil.rmtree(tmp_directory)

        if os.path.isfile(obj.path):
            obj.status = Format.DONE
            obj.filesize = os.path.getsize(obj.path)
        else:
            obj.status = Format.ERROR
            obj.filesize = None

        obj.save()

    def save(self, *args, **kwargs):

        self.do_process = False
        if self.pk is None or self.status == Format.INIT:
            self.do_process = True
            #self.status = Format.PROCESSING

        if not self.media_uuid:
            self.media_uuid = self.media.uuid

        super(Format, self).save(*args, **kwargs)


# @receiver(post_save, sender=Format)
# def format_post_save(sender, instance, created, **kwargs):
#
#     do_process = getattr(instance, 'do_process', False)
#     log.debug('format_post_save - processing required: %s' % do_process)
#
#     if do_process:
#         if USE_CELERYD:
#             log.debug('sending job to task queue')
#             process_format_task.apply_async((instance.media.pk,))
#             #obj.process_format.apply_async(queue='convert')
#         else:
#             log.debug('processing task in foreground')
#             process_format_task(media_pk=instance.media.pk)
#             #obj.process_format()


@receiver(pre_delete, sender=Format)
def format_pre_delete(sender, instance, **kwargs):
    obj = instance
    if os.path.isfile(obj.path):
        os.remove(obj.path)
        clean_directory_tree_reverse(obj.path)


@task
def clean_assets(days_to_keep=MEDIA_ASSET_KEEP_DAYS):
    from datetime import datetime, timedelta

    format_qs = Format.objects.filter(accessed__lte=datetime.now() - timedelta(days=days_to_keep)).nocache()
    waveform_qs = Waveform.objects.filter(accessed__lte=datetime.now() - timedelta(days=days_to_keep)).nocache()

    log.info('cleaning assets. {0} formats and {1} waveforms'.format(format_qs.count(), waveform_qs.count()))

    # delete must be called on each item, to not skip post_delete actions.
    for i in format_qs:
        # don't delete cache if media is in at least one playlist
        if i.media.appearances.exists():
            continue
        i.delete()

    for i in waveform_qs:
        # don't delete cache if media is in at least one playlist
        if i.media.appearances.exists():
            continue
        i.delete()
