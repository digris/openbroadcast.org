# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from django.core.management.base import NoArgsCommand, CommandError
from tqdm import tqdm

NUM_DAYS_KEEP = 2

class CleanAssets(NoArgsCommand):
    help = 'Clean media assets not accessed for the last {0} days'.format(NUM_DAYS_KEEP)

    def handle_noargs(self, **options):
        from media_asset.models import Format
        from media_asset.models import Waveform
        format_qs = Format.objects.filter(accessed__lte=datetime.now() - timedelta(days=NUM_DAYS_KEEP)).nocache()
        waveform_qs = Waveform.objects.filter(accessed__lte=datetime.now() - timedelta(days=NUM_DAYS_KEEP)).nocache()

        print 'format objects to delete:    {}'.format(format_qs.count())
        print 'waveform objects to delete:  {}'.format(waveform_qs.count())

        for i in tqdm(format_qs):
            i.delete()

        for i in tqdm(waveform_qs):
            i.delete()
