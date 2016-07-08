# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from django.core.management.base import BaseCommand, NoArgsCommand, CommandError
from django.conf import settings
from tqdm import tqdm

MEDIA_ASSET_KEEP_DAYS = getattr(settings, 'MEDIA_ASSET_KEEP_DAYS', 60)

class CleanAssets(NoArgsCommand):

    help = 'Clean media assets not accessed for the last {0} days'.format(MEDIA_ASSET_KEEP_DAYS)

    def handle_noargs(self, **options):
        from media_asset.models import Format
        from media_asset.models import Waveform
        format_qs = Format.objects.filter(accessed__lte=datetime.now() - timedelta(days=MEDIA_ASSET_KEEP_DAYS)).nocache()
        waveform_qs = Waveform.objects.filter(accessed__lte=datetime.now() - timedelta(days=MEDIA_ASSET_KEEP_DAYS)).nocache()

        print 'format objects to delete:    {}'.format(format_qs.count())
        print 'waveform objects to delete:  {}'.format(waveform_qs.count())

        for i in tqdm(format_qs):
            i.delete()

        for i in tqdm(waveform_qs):
            i.delete()
