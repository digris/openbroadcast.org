# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

import logging

from celery import shared_task
from django.utils import timezone



from fprint_client.api_client import FprintAPIClient

log = logging.getLogger(__name__)


@shared_task
def ingest_fprint_for_media(media_id):

    from alibrary.models import Media
    obj = Media.objects.get(pk=media_id)

    client = FprintAPIClient()
    result = client.ingest_for_media(obj)

    if result:
        log.info('Media id: {} - ingested fprint'.format(obj.pk))
        type(obj).objects.filter(pk=obj.pk).update(
            fprint_ingested=timezone.now()
        )
    else:
        log.warning('Media id: {} - unable to ingest fprint'.format(obj.pk))



@shared_task
def delete_fprint_for_media(media_id):

    from alibrary.models import Media
    obj = Media.objects.get(pk=media_id)

    log.info('Media id: {} - delete fprint'.format(obj.pk))
    client = FprintAPIClient()

    result = client.delete_for_media(obj)

