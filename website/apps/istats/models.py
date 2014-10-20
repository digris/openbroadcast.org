from celery.task.control import inspect

from exporter.models import Export
from importer.models import ImportFile

class Stats(object):

    def __init__(self):
        self.celery_inspector = inspect()



    def get_server_stats(self):

        stats = []

        ts = {
                'key': 'exporter',
                'display': 'Exports',
                'queue': Export.objects.filter(status=2).count(),
                'estimate': Export.objects.filter(status=2).count() * 60 / 60,
        }
        stats.append(ts)

        ts = {
                'key': 'importer',
                'display': 'Imports',
                'queue': ImportFile.objects.filter(status=6).count(),
                'estimate': ImportFile.objects.filter(status=6).count() * 21 / 60,
        }
        stats.append(ts)

        ts = {
                'key': 'fingerprinter',
                'display': 'Scanning',
                'queue': ImportFile.objects.filter(status=3).count(),
                'estimate': ImportFile.objects.filter(status=3).count() * 33 / 60,
        }
        stats.append(ts)


        return stats