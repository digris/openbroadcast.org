# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
from django.db.models.signals import post_save
from django.dispatch import receiver


class MediaassetConfig(AppConfig):
    name = 'media_asset'
    verbose_name = "Media Asset App"

    def ready(self):
        setup_signals()


def setup_signals():

    from .models import Waveform, Format

    # @receiver(post_save, sender='alibrary.Media')
    # def media_post_save(sender, instance, created, **kwargs):
    #
    #     print 'media post save'
    #
    #     Waveform.objects.get_or_create_for_media(media=instance, type=Waveform.WAVEFORM)
    #     Waveform.objects.get_or_create_for_media(media=instance, type=Waveform.SPECTROGRAM)
    #     Format.objects.get_or_create_for_media(media=instance, encoding=Format.MP3, quality=Format.DEFAULT)
