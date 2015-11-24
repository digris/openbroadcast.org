# -*- coding: utf-8 -*-
import sys
from django.core.management.base import NoArgsCommand, CommandError
from django.db.models.loading import get_model

MODELS_TO_RESET = (

    # alibrary
    'alibrary.Media',
    'alibrary.Release',
    'alibrary.Artist',
    'alibrary.Label',
    'alibrary.Relation',
    'alibrary.Distributor',
    'alibrary.Playlist',

    # importer
    'importer.Import',
    'importer.ImportFile',
    'importer.ImportItem',

    # exporter
    'exporter.Export',
    'exporter.ExportItem',

    # media_asset
    'media_asset.Waveform',
    'media_asset.Format',

    # abcast
    'abcast.Emission',

)

LIMIT_PER_DELETE = 1000


class ResetDatabase(NoArgsCommand):
    help = 'Resets all platform data'

    def handle_noargs(self, **options):

        if not raw_input("%s (y/N): " % 'Are your 100% sure to continue? Everything will be wiped out!!').lower() == 'y':
            sys.exit(1)

        for entry in MODELS_TO_RESET:
            app_label, model_name = entry.split(".")
            model = get_model(app_label=app_label, model_name=model_name)
            qs = model.objects.all().nocache()

            print
            print
            print '---------------------------------------------------'
            print 'deleting all instances of %s' % entry
            print '---------------------------------------------------'
            print

            while qs.count() > 0:
                print 'got %s entries for deletion - model: %s' % (qs.count(), entry)
                for item in qs[0:LIMIT_PER_DELETE]:
                    item.delete()
                    #print '.',
                    sys.stdout.write('.')
                    sys.stdout.flush()
                print
                qs = model.objects.all().nocache()


