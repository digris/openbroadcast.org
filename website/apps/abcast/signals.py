from __future__ import unicode_literals

import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_elasticsearch_dsl.registries import registry

from .utils import notify
from .models import Emission, Channel

log = logging.getLogger(__name__)


@receiver(post_save, sender=Emission)
def emission_post_save(sender, instance, created, **kwargs):
    log.debug("emission saved - {} - {}".format(instance, instance.content_object))
    registry.update(instance.content_object)


@receiver(post_save, sender=Channel)
def channel_post_save(sender, instance, created, **kwargs):
    log.debug("channel saved - {}".format(instance))

    try:
        notify.start_play(instance.on_air, instance)
    except Exception as e:
        # TODO: propperly handle exceptions
        log.warning("unable to update metadata: {}".format(e))

    # registry.update(instance.content_object)
