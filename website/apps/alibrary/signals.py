# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models.signals import post_save, pre_save
from django.dispatch.dispatcher import receiver

from models import Artist
from models import Media
from models import Release

@receiver(post_save, sender=Artist, dispatch_uid="create_activity_item")
def invalidate_artist_cache(sender, instance, created, **kwargs):
    instance.get_releases.invalidate(instance)
    instance.get_media.invalidate(instance)

@receiver(post_save, sender=Media, dispatch_uid="create_activity_item2")
def invalidate_related_artist_cache(sender, instance, created, **kwargs):
    instance.artist.get_releases.invalidate(instance.artist)
    instance.artist.get_media.invalidate(instance.artist)

