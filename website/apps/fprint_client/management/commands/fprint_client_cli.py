# -*- coding: utf-8 -*-

import time
import sys
import datetime
import djclick as click
from django.db import connections, connection
from django.conf import settings
from django.utils import timezone


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
@click.option('--async', default=False, is_flag=True, help='Run in async mode (multiprocessing Pool)')
def update_index(force, async):
    """
    update fingerpint index (via fprint service)
    """

    if force:
        _count = Media.objects.all().update(fprint_ingested=None)
        click.secho('Resetting all fingerprints. ({})'.format(_count), fg='cyan')

    qs = Media.objects.exclude(master__isnull=True).filter(fprint_ingested__isnull=True)

    if async:

        pool = Pool()
        procs = []

        for m in qs:
            click.secho('{}'.format(m.pk), fg='cyan')
            procs.append(pool.apply_async(_ingest_fingerprint, args=(m,)))

        pool.close()
        pool.join()


    else:

        for m in qs:
            _ingest_fingerprint(m)


def _ingest_fingerprint(media):
    """
    generates and ingests fingerprint for given media object
    """

    # close connection, needed for multiprocessing
    # https://stackoverflow.com/questions/8242837/django-multiprocessing-and-database-connections
    connection.close()

    client = FprintAPIClient()

    try:

        if client.ingest_for_media(obj=media):
            Media.objects.filter(pk=media.pk).update(
                fprint_ingested=timezone.now()
            )

    except Exception as e:
        click.secho('unable to ingest fprint for media: {} - {}'.format(media.pk, e))
