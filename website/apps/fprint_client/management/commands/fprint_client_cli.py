# -*- coding: utf-8 -*-

import time
import sys
import datetime
import djclick as click
from django.conf import settings
from django.utils import timezone
from django.db.models import Count

from multiprocessing import Pool

from ...utils import code_for_path
from ...api_client import FprintAPIClient

from alibrary.models import Media

DEFAULT_LIMIT = 100
MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT', None)

CHUNK_SIZE = 2


@click.group()
def cli():
    """Fingerprint CLI"""
    pass


@cli.command()
@click.option('--force', default=False, is_flag=True, help='Force to rebuild all fingerprints?')
def update_index(force):
    """
    update fingerpint index (via fprint service)
    """

    if force:
        _count = Media.objects.all().update(fprint_ingested=None)
        click.secho('Resetting all fingerprints. ({})'.format(_count), fg='cyan')

    qs = Media.objects.exclude(master__isnull=True).filter(fprint_ingested__isnull=True)

    pool = Pool()
    procs = []

    for m in qs.iterator():
        click.secho('{}'.format(m.pk), fg='cyan')
        procs.append(pool.apply_async(ingest_fingerprint, args=(m,)))

    pool.close()
    pool.join()


def ingest_fingerprint(media):
    """
    generates and ingests fingerprint for given media object
    """

    client = FprintAPIClient()

    try:

        if client.ingest_for_media(obj=media):
            Media.objects.filter(pk=media.pk).update(
                fprint_ingested=timezone.now()
            )

    except Exception as e:
        click.secho('unable to ingest fprint for media: {} - {}'.format(media.pk, e))
