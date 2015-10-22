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

    #media = models.ForeignKey('alibrary.Media')

    class Meta:
        app_label = 'media_asset'
        verbose_name = _('Waveform')
        #ordering = ('format', 'version' )

    def __unicode__(self):
        return '%s' % (self.uuid)

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

        print obj.directory
        print obj.path

        if not os.path.isdir(obj.directory):
            os.makedirs(obj.directory)

        if obj.type == 'w':
            create_waveform_image(wav_path, obj.path)

        elif obj.type == 's':
            create_spectrogram_image(wav_path, obj.path)

        else:
            raise NotImplementedError('type %s not implemented' % obj.type)



        shutil.rmtree(tmp_directory)


        pass




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