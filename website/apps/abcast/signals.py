from __future__ import unicode_literals

import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_elasticsearch_dsl.registries import registry

from .models import Emission

log = logging.getLogger(__name__)


@receiver(post_save, sender=Emission)
def emission_post_save(sender, instance, created, **kwargs):

    log.debug(
        "emission saved - {} - {}".format(
            instance, instance.content_object
        )
    )

    registry.update(instance.content_object)
