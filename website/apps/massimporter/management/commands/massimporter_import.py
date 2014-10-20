#-*- coding: utf-8 -*-
import os
import sys
from optparse import make_option
from django.core.management.base import BaseCommand, NoArgsCommand

from massimporter.models import Massimport

#from importer.models import Import, ImportFile

class Massimporter(object):
    def __init__(self, * args, **kwargs):
        self.directory = kwargs.get('directory')
        self.rescan = kwargs.get('rescan')
        self.reset_files = kwargs.get('reset_files')
        self.import_session = kwargs.get('import_session')
        self.username = kwargs.get('username')
        self.verbosity = int(kwargs.get('verbosity', 1))

        print
        print '/////////////////////////////////////////////////////////////'
        print '//                   Massimporter                          //'
        print '/////////////////////////////////////////////////////////////'
        print
        print 'directory:      %s' % self.directory
        print 'import_session: %s' % self.import_session
        print 'username:       %s' % self.username
        print



    def process(self):

        if not self.directory:
            print 'directory is required!'
            sys.exit(2)

        massimport, created = Massimport.objects.get_or_create(directory=self.directory)

        print 'massimport: %s' % massimport
        print 'created:    %s' % created

        if created or self.rescan:
            print 'RESCANNING'

            massimport.scan_directory(reset=self.reset_files)


            
            
            
            


class Command(NoArgsCommand):

    option_list = BaseCommand.option_list + (
        make_option('--directory',
            action='store',
            dest='directory',
            help='Apsolute path to directory for import'),
        make_option('--rescan',
            action='store_true',
            dest='rescan',
            default=False,
            help='Rescan directory (in case it exists)'),
        make_option('--reset',
            action='store_true',
            dest='reset_files',
            default=False,
            help='Reset files when scnanning directory'),
        make_option('--username',
            action='store',
            dest='username',
            default='root',
            help='Assign to username'),
        make_option('--import_session',
            action='store',
            dest='import_session',
            default=None,
            help='Name for import-session to use'),
        )

    def handle_noargs(self, **options):
        
        runner = Massimporter(**options)
        runner.process()
