# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.db.models.signals import post_save, pre_save
from django.dispatch.dispatcher import receiver

from media_preflight.models import PreflightCheck


@receiver(post_save, sender="alibrary.Media")
def media_post_save(sender, instance, created, **kwargs):

    if (
        instance.master
        and hasattr(instance, "_master_changed")
        and instance._master_changed
    ):

        try:
            preflight_check = PreflightCheck.objects.get(media=instance)
            preflight_check.status = PreflightCheck.STATUS_PENDING
            preflight_check.save()

        except PreflightCheck.DoesNotExist:
            preflight_check = PreflightCheck(
                media=instance, status=PreflightCheck.STATUS_PENDING
            )
            preflight_check.save()
