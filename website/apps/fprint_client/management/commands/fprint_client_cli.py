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

    id_list = Media.objects.exclude(
        master__isnull=True
    ).nocache().filter(
        master_duration__lte=(60 * 20),
        fprint_ingested__isnull=True
    ).values_list('id', flat=True)

    click.secho('{} media items to process'.format(id_list.count()), fg='cyan')

    if async:

        pool = Pool(processes=8)
        procs = []

        for id in id_list:
            # close connection, needed for multiprocessing
            connection.close()
            m = Media.objects.get(pk=id)
            #click.secho('{}'.format(m.pk), fg='cyan')
            procs.append(pool.apply_async(_ingest_fingerprint, args=(m,)))

        pool.close()
        pool.join()


    else:

        for id in id_list:
            m = Media.objects.get(pk=id)
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


