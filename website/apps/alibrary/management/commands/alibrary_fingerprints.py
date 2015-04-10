#-*- coding: utf-8 -*-
import sys
from optparse import make_option
from django.core.management.base import BaseCommand, NoArgsCommand


# echoprint
from ep.API import fp

# models
#

# logging
import logging
log = logging.getLogger(__name__)

DEFAULT_LIMIT = 1000


class Fingerprinter(object):
    def __init__(self, * args, **kwargs):
        self.delete_fingerprints = kwargs.get('delete_fingerprints')
        self.create_fingerprints = kwargs.get('create_fingerprints')
        self.show_stats = kwargs.get('show_stats')
        self.force_action = kwargs.get('force_action')
        self.limit = int(kwargs.get('limit', DEFAULT_LIMIT))
        self.verbosity = int(kwargs.get('verbosity', 1))

    def run(self):

        if self.delete_fingerprints:

            print
            print '********************************************************'
            print '* delete all fingerprints'
            print '********************************************************'

            from alibrary.models import Media

            if raw_input('are you sure? [y/N]: ').lower() == 'y':
                fp.erase_database(True)
                print
                Media.objects.all().update(echoprint_status=0)
                Media.objects.all().update(echoprint_id=None)
                print 'done'

            else:
                print
                print 'exiting'
                sys.exit(0)
            
            
        if self.create_fingerprints:

            print
            print '********************************************************'
            print '* (re-)create fingerprints'
            print '********************************************************'

            from alibrary.models import Media
            
            qs = Media.objects.exclude(master='')
            if not self.force_action:
                qs = qs.filter(echoprint_status=0)

            qs = qs[0:self.limit]


            num_total = qs.count()
            num_done = 0
            for object in qs:
                print object.pk
                object.update_echoprint()
                num_done += 1
                print '%0.2f%% - %s/%s' % ((float(num_done) / float(num_total) * 100), num_done, num_total)


        if self.show_stats:

            print
            print '********************************************************'
            print '* fingerprint stats'
            print '********************************************************'

            from alibrary.models import Media

            qs = Media.objects.all()


            print ' - num. total:     %s' % qs.count()
            print ' - num. init:      %s' % qs.filter(echoprint_status=0).count()
            print ' - num. assigned:  %s' % qs.filter(echoprint_status=1).count()
            print ' - num. error:     %s' % qs.filter(echoprint_status__in=[2, 99]).count()
            print

            


class Command(NoArgsCommand):
    """
    Import directory structure into the filer ::

        manage.py --path=/tmp/assets/images
        manage.py --path=/tmp/assets/news --folder=images
    """

    option_list = BaseCommand.option_list + (
        make_option('--delete',
            action='store_true',
            dest='delete_fingerprints',
            default=False,
            help='Delete all fingerprints'),
        make_option('--create',
            action='store_true',
            dest='create_fingerprints',
            default=False,
            help='Create fingerprints'),
        make_option('--force',
            action='store_true',
            dest='force_action',
            default=False,
            help='Enforce action'),
        make_option('--limit',
            action='store',
            dest='limit',
            default=DEFAULT_LIMIT,
            help='Limit objects to process'),
        make_option('--stats',
            action='store_true',
            dest='show_stats',
            default=False,
            help='Display stats'),
        )

    def handle_noargs(self, **options):
        fprinter = Fingerprinter(**options)
        fprinter.run()
