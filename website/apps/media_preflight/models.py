# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

import logging

from django.conf import settings
from django.core.urlresolvers import reverse_lazy, reverse
from rest_framework.reverse import reverse as api_reverse
from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from jsonfield import JSONField

from .tasks import request_check_for_media, delete_check_for_media

SITE_URL = getattr(settings, 'SITE_URL')

log = logging.getLogger(__name__)

@python_2_unicode_compatible
class PreflightCheck(models.Model):

    STATUS_INIT = 0
    STATUS_PROCESSING = 1
    STATUS_DONE = 2
    STATUS_ERROR = 99

    STATUS_CHOICES = (
        (STATUS_INIT, 'Initialized'),
        (STATUS_PROCESSING, 'Processing'),
        (STATUS_DONE, 'Done'),
        (STATUS_ERROR, 'Error'),
    )

    status = models.PositiveSmallIntegerField(
        _('Status'),
        choices=STATUS_CHOICES,
        default=STATUS_INIT,
        blank=False, null=False,
        db_index=True,
    )

    media = models.OneToOneField(
        'alibrary.Media',
        related_name='preflight_check',
        null=True, blank=False
    )

    result = JSONField(
        null=True, blank=True
    )

    preflight_ok = models.BooleanField(
        default=False
    )

    def __str__(self):
        return '{}'.format(self.pk)

    @property
    def uuid(self):
        """
        no independent uuid needed/wished here. mapps to media uuis
        """
        if self.media:
            return self.media.uuid

    def get_api_url(self):

        url = reverse('api:preflight-check-detail', kwargs={
            'uuid': self.uuid
        })
        return '{}{}'.format(SITE_URL, url)



@receiver(pre_save, sender=PreflightCheck)
def preflight_check_pre_save(sender, instance, **kwargs):
    """
    initiate preflight check (intermediate step here to handle async)
    """

    if instance.result:

        instance.status = PreflightCheck.STATUS_DONE

        if instance.result['errors']:
            instance.preflight_ok = False

        if instance.result['checks']:

            duration_preflight = instance.result['checks'].get('duration_preflight')
            duration_master = instance.media.master_duration

            #print('diff: {}'.format(abs(duration_preflight - duration_master)))

            if duration_preflight and  (abs(duration_preflight - duration_master) < 2.0):
                instance.preflight_ok = True

            else:
                instance.preflight_ok = False
                instance.result['errors']['duration'] = 'duration mismatch - master: {} preflight: {}'.format(
                    duration_master, duration_preflight
                )





@receiver(post_save, sender=PreflightCheck)
def preflight_check_post_save(sender, instance, created, **kwargs):
    """
    initiate preflight check (intermediate step here to handle async)
    """

    if instance.status < PreflightCheck.STATUS_PROCESSING:
        PreflightCheck.objects.filter(pk=instance.pk).update(status=PreflightCheck.STATUS_PROCESSING)
        request_check_for_media.apply_async((instance.media,))
        #request_check_for_media(instance.media)


@receiver(post_delete, sender=PreflightCheck)
def preflight_check_post_delete(sender, instance, **kwargs):
    """
    delete remote resource.
    """
    if instance.media:
        delete_check_for_media.apply_async((instance.media,))
        #delete_check_for_media(instance.media)
