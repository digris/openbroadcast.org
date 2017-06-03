#-*- coding: utf-8 -*-

import time
import sys
import datetime
import djclick as click
from django.conf import settings
from django.utils import timezone
from django.db.models import Count

from ...utils import code_for_path
from ...api_client import FprintAPIClient

from alibrary.models import Media


DEFAULT_LIMIT = 100
MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT', None)


@click.group()
def cli():
    pass



@cli.command()
def rebuild_index():

    client = FprintAPIClient()

    qs = Media.objects.exclude(master__isnull=True)
    qs.update(fprint_ingested=None)

    for m in qs:
        click.secho('{}'.format(m.master.path), fg='cyan')

        # code = code_for_path(m.master.path)

        if client.ingest_for_media(obj=m):

            Media.objects.filter(pk=m.pk).update(
                fprint_ingested=timezone.now()
            )

    print qs.count()



