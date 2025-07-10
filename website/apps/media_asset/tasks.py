import logging

from celery import shared_task

log = logging.getLogger(__name__)


@shared_task
def process_assets_for_media(media_pk):
    from alibrary.models import Media
    from .models import Waveform, Format

    media = Media.objects.get(pk=media_pk)

    log.info(f"process assets for media id: {media.pk}")

    if not media.master:
        return

    waveform, waveform_created = Waveform.objects.get_or_create(
        media=media, type=Waveform.WAVEFORM
    )
    format, format_created = Format.objects.get_or_create(
        media=media, encoding=Format.MP3, quality=Format.DEFAULT
    )

    if waveform_created:
        waveform.process_waveform()

    if format_created:
        format.process_format()
