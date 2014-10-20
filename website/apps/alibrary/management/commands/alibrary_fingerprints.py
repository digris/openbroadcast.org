#-*- coding: utf-8 -*-
from optparse import make_option

from django.core.management.base import BaseCommand, NoArgsCommand


# echoprint
from ep.API import fp

# models
#

# logging
import logging
log = logging.getLogger(__name__)


class Fingerprinter(object):
    def __init__(self, * args, **kwargs):
        self.do_delete = kwargs.get('delete')
        self.do_create = kwargs.get('create')
        self.verbosity = int(kwargs.get('verbosity', 1))

    def run(self):

        if self.do_delete:
            from alibrary.models import Media
            print 'delete fingerprints'
            fp.erase_database(True)
            
            
        if self.do_create:
            from alibrary.models import Media
            print 'create fingerprints'
            
            media = Media.objects.exclude(master='')
            for m in media:
                print m.name
                m.update_echoprint()
            
            


class Command(NoArgsCommand):
    """
    Import directory structure into the filer ::

        manage.py --path=/tmp/assets/images
        manage.py --path=/tmp/assets/news --folder=images
    """

    option_list = BaseCommand.option_list + (
        make_option('--delete',
            action='store_true',
            dest='delete',
            default=False,
            help='Delete all fingerprints'),
        make_option('--create',
            action='store_true',
            dest='create',
            default=False,
            help='Create fingerprints'),

        )

    def handle_noargs(self, **options):
        fprinter = Fingerprinter(**options)
        fprinter.run()
