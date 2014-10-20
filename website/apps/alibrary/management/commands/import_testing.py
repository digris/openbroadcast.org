#-*- coding: utf-8 -*-
from optparse import make_option

from django.core.management.base import BaseCommand, NoArgsCommand

from alibrary.models import Release
from filer.models.filemodels import File
from filer.models.audiomodels import Audio
from filer.models.imagemodels import Image


class FolderImporter(object):
    
    def __init__(self, * args, **kwargs):
        self.id = kwargs.get('id')


    def walker(self):
        print 'Walker...'
        
        if self.id:
            r = Release.objects.get(pk=int(self.id))
            print r




class Command(NoArgsCommand):

    option_list = BaseCommand.option_list + (
        make_option('--id',
            action='store',
            dest='id',
            default=False,
            help='The ID'),
        )

    def handle_noargs(self, **options):
        folder_importer = FolderImporter(**options)
        folder_importer.walker()
