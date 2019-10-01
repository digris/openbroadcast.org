# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from .tasks import request_check_for_media, delete_check_for_media

__version__ = "0.0.1"

default_app_config = "media_preflight.apps.MediaPreflightConfig"

log = logging.getLogger(__name__)


@receiver(post_save, sender="alibrary.Media")
def media_post_save(sender, instance, created, **kwargs):

    # initialize preflight if master file changed
    if (
        instance.master
        and hasattr(instance, "_master_changed")
        and instance._master_changed
    ):

        from .models import PreflightCheck

        preflight_check, _c = PreflightCheck.objects.get_or_create(media=instance)
        log.debug(
            "initialized preflight check - media id: {} - check id: {}".format(
                instance.pk, preflight_check.pk
            )
        )


@receiver(post_delete, sender="alibrary.Media")
def media_post_delete(sender, instance, **kwargs):

    if hasattr(instance, "preflight_check") and instance.preflight_check:

        instance.preflight_check.delete()
