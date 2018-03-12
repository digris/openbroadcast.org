# -*- coding: utf-8 -*-

import time
import sys
import datetime
import requests
import subprocess
import json
import djclick as click
from django.db import connections, connection
from django.conf import settings
from django.utils import timezone


from multiprocessing import Pool

from ...utils import code_from_path
from ...api_client import FprintAPIClient

from alibrary.models import Media

DEFAULT_LIMIT = 100
MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT', None)

CHUNK_SIZE = 2


ECHOPRINT_CODEGEN_BINARY = 'echoprint-codegen'

# FPRINT_API_URL = 'http://10.40.10.214:8000'
FPRINT_API_URL = 'http://172.20.10.240:8000'
#FPRINT_API_URL = 'http://127.0.0.1:7777'


@click.group()
def cli():
    """Fingerprint CLI"""
    pass


@cli.command()
@click.option('--force', default=False, is_flag=True, help='Force to rebuild all fingerprints?')
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




@cli.command()
@click.option('--limit', default=100, type=int)
@click.option('--offset', default=0, type=int)
def test_media(limit, offset):

    qs = Media.objects.exclude(
        master__isnull=True
    ).nocache().filter(
        master_duration__lte=(60 * 20),
        fprint_ingested__isnull=False
    )

    for item in qs[offset:(offset + limit)]:

        click.secho(u'testing fprint: {} - {}'.format(item.uuid, item.name), fg='cyan')

        command = [
            ECHOPRINT_CODEGEN_BINARY,
            item.master.path
        ]

        p = subprocess.Popen(command, stdout=subprocess.PIPE, close_fds=True)

        data = json.loads(p.stdout.read())[0]

        url = '{}/api/v1/fprint/identify/'.format(FPRINT_API_URL)

        r = requests.post(url, json=data)

        results = r.json()

        if results:
            top_match = results[0]
            uuid = top_match['uuid']
            score = top_match['score']

            if str(uuid) == str(item.uuid):
                click.secho(u'score: {}'.format(score), fg='green')
            else:
                click.secho(u'score: {}'.format(score), fg='yellow')
        else:
            click.secho(u'no results for: {}'.format(item.uuid), fg='red')


