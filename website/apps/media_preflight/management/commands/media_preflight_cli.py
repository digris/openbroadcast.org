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

from alibrary.models import Media
from media_preflight.models import PreflightCheck

DEFAULT_LIMIT = 100


@click.group()
def cli():
    """Media Preflight CLI"""
    pass


@cli.command()
@click.option('--limit', default=DEFAULT_LIMIT, help='Limit number of entries to process')
@click.option('--force', default=False, is_flag=True, help='Force to run preflight on all tracks')
@click.option('--async', default=False, is_flag=True, help='Run in async mode (multiprocessing Pool)')
def request_checks(limit, force, async):
    """
    requests preflight checks (via preflight service)
    """

    if force:
        _count = PreflightCheck.objects.all().delete()
        click.secho('Deleted all existing preflighjt checks. ({})'.format(_count), fg='cyan')

    id_list = Media.objects.exclude(
        #master__isnull=True
        master=''
    ).nocache().filter(
        preflight_check__isnull=True
    ).values_list('id', flat=True)

    click.secho('{} media items to process'.format(id_list.count()), fg='cyan')

    if async:

        pool = Pool(processes=8)
        procs = []

        for id in id_list[0:limit]:
            # close connection, needed for multiprocessing
            connection.close()
            m = Media.objects.get(pk=id)
            #click.secho('{}'.format(m.pk), fg='cyan')
            procs.append(pool.apply_async(_request_check, args=(m,)))

        pool.close()
        pool.join()


    else:

        for id in id_list[0:limit]:
            m = Media.objects.get(pk=id)
            _request_check(m)


def _request_check(media):
    """
    requests preflight check for media on preflight api
    """

    connection.close()

    try:
        _p, _c = PreflightCheck.objects.get_or_create(media=media)


    except Exception as e:
        click.secho('unable to request preflight check for media: {} - {}'.format(media.pk, e))

