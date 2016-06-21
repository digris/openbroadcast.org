from django.db.models.signals import post_save, pre_save
from django.dispatch.dispatcher import receiver

from alibrary.models import Artist
from alibrary.models import Media

@receiver(post_save, sender=Artist, dispatch_uid="invalidate_artist_cache")
def invalidate_artist_cache(sender, instance, created, **kwargs):
    try:
        instance.get_releases.invalidate(instance)
        instance.get_media.invalidate(instance)
    except Exception as e:
        pass

@receiver(post_save, sender=Media, dispatch_uid="invalidate_related_artist_cache")
def invalidate_related_artist_cache(sender, instance, created, **kwargs):
    try:
        if instance.artist:
            instance.artist.get_releases.invalidate(instance.artist)
            instance.artist.get_media.invalidate(instance.artist)
    except Exception as e:
        pass
