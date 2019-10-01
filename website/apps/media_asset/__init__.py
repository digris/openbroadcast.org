# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.dispatch import receiver
from django.db.models.signals import post_save

from .tasks import process_assets_for_media

__version__ = "0.0.1"

default_app_config = "media_asset.apps.MediaassetConfig"


@receiver(post_save, sender="alibrary.Media")
def media_post_save(sender, instance, created, **kwargs):

    process_assets_for_media.apply_async((instance.pk,))
