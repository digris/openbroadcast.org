#-*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import sys
from optparse import make_option
from django.contrib.auth.models import User
from django.conf import settings
from django.core.management.base import BaseCommand, NoArgsCommand

from massimporter.models import Massimport, MassimportFile

MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT', None)

class Massimporter(object):

    def __init__(self, command, *args, **kwargs):

        self.directory = kwargs.get('directory')
        self.rescan = kwargs.get('rescan')
        self.id = kwargs.get('id')
        self.reset_files = kwargs.get('reset_files')
        self.import_session = kwargs.get('import_session')
        self.username = kwargs.get('username')
        self.verbosity = int(kwargs.get('verbosity', 1))

        if self.directory:
            if not self.directory.startswith(MEDIA_ROOT):
                print 'directory has to be inside MEDIA_ROOT: {}'.format(MEDIA_ROOT)
                sys.exit(2)


    def list(self):
        """
        returns a list with status information for all existing sessions
        """

        massimports = Massimport.objects.order_by('status').all()

        print '--------------------------------------------------------------------'
        print 'id\tstatus\tfiles\tuser\tdirectory\t'
        print '--------------------------------------------------------------------'
        for item in massimports:
            print '{id}\t{status}\t{num_files}\t{username}\t{directory}'.format(
                id=item.pk,
                status=item.get_status_display(),
                username=item.user,
                num_files=item.files.count(),
                directory=item.directory,
            )


    def scan(self):

        massimport = Massimport.objects.get(pk=int(self.id))
        massimport.scan()

    def delete(self):

        Massimport.objects.get(pk=int(self.id)).delete()

    def update(self):

        massimport = Massimport.objects.get(pk=int(self.id))
        massimport.update()

    def status(self):

        massimport = Massimport.objects.get(pk=int(self.id))
        massimport.update()

        print '--------------------------------------------------------------------'
        print 'Status'
        print '--------------------------------------------------------------------'

        for status in MassimportFile.STATUS_CHOICES:
            count = massimport.files.filter(status=status[0]).count()
            if count:
                print('{}:    \t{}'.format(
                    status[1],
                    count
                ))










    def start(self):

        if not self.directory or not os.path.isdir(self.directory):
            print 'directory missing or does not exist'
            sys.exit(2)

        if not self.directory.endswith('/'):
            self.directory += '/'

        if Massimport.objects.filter(directory=self.directory).exists():
            print 'Massimport (ID: {}) already exists for: {}'.format(
                Massimport.objects.get(directory=self.directory).pk,
                self.directory
            )
            sys.exit(2)

        if not self.username or not User.objects.filter(username=self.username).exists():
            print 'username missing or user does not exist'
            sys.exit(2)

        massimport = Massimport(
            directory=self.directory,
            user=User.objects.get(username=self.username)
        )

        massimport.save()
        massimport.scan()

    def enqueue(self):

        massimport = Massimport.objects.get(pk=int(self.id))

        for item in massimport.files.all():
            item.enqueue()




class Command(BaseCommand):

    def add_arguments(self, parser):

        parser.add_argument('action')

        parser.add_argument('-d', '--directory',
                            dest='directory',
                            default=False,
                            help='Delete poll instead of closing it')

        parser.add_argument('-u', '--username',
                            dest='username',
                            default=False,
                            help='Delete poll instead of closing it')

        parser.add_argument('-i', '--id',
                            dest='id',
                            default=False,
                            help='Delete poll instead of closing it')

    def handle(self, *args, **options):

        action = options.get('action', None)

        worker = Massimporter(command=self, **options)
        command = getattr(worker, action)
        if command:
            command()


# class Command(NoArgsCommand):
#
#     option_list = BaseCommand.option_list + (
#         make_option('--directory',
#             action='store',
#             dest='directory',
#             help='Apsolute path to directory for import'),
#         make_option('--rescan',
#             action='store_true',
#             dest='rescan',
#             default=False,
#             help='Rescan directory (in case it exists)'),
#         make_option('--reset',
#             action='store_true',
#             dest='reset_files',
#             default=False,
#             help='Reset files when scnanning directory'),
#         make_option('--username',
#             action='store',
#             dest='username',
#             default='root',
#             help='Assign to username'),
#         make_option('--import_session',
#             action='store',
#             dest='import_session',
#             default=None,
#             help='Name for import-session to use'),
#         )
#
#     def handle_noargs(self, **options):
#
#         runner = Massimporter(**options)
#         runner.process()
