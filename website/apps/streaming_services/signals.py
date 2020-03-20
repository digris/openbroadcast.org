# -*- coding: utf-8 -*-
import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

from arating.models import Vote
from .clients.deezer import DeezerAPIClient

log = logging.getLogger(__name__)


def sync_favorites(rating, obj, user):

    if user.social_auth.filter(provider="deezer").exists():
        social_auth = user.social_auth.get(provider="deezer")
        client = DeezerAPIClient(
            user_id=social_auth.uid, access_token=social_auth.access_token
        )

        if rating > 0:
            client.add_to_favorites(obj)
        else:
            client.remove_from_favorites(obj)


@receiver(post_save, sender=Vote)
def vote_post_save(sender, instance, **kwargs):
    log.debug("vote saved: {}".format(instance))
    print("saved", instance)
    print("vote", int(instance.vote))

    sync_favorites(
        rating=int(instance.vote), obj=instance.content_object, user=instance.user
    )
