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
        log.info("Media id: %s - ingested fprint", obj.pk)
        type(obj).objects.filter(pk=obj.pk).update(fprint_ingested=timezone.now())
    else:
        log.warning("Media id: %s - unable to ingest fprint", obj.pk)


@shared_task
def delete_fprint_for_media(media_uuid):

    log.info("Media id: %s - delete fprint", media_uuid)
    client = FprintAPIClient()

    client.delete_for_media(media_uuid)
