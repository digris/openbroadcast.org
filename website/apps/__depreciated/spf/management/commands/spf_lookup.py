#-*- coding: utf-8 -*-

from optparse import make_option

from django.core.management.base import BaseCommand, NoArgsCommand

from obp_legacy.models import *
from spf.models import Request, Match
from spf.util.lookup import MediaLookup, LegacyLookup
from spf.util.match import MediaMatch


DEFAULT_LIMIT = 500
DEFAULT_OFFSET = 0

class SpfWorker(object):
    def __init__(self, *args, **kwargs):
        self.action = kwargs.get('action')

        self.limit = DEFAULT_LIMIT
        self.offset = DEFAULT_OFFSET

        try:
            self.swp_id = int(kwargs.get('swp_id'))
        except:
            self.swp_id = None

        self.verbosity = int(kwargs.get('verbosity', 1))

    def run(self):

        print 'walker'
        print 'action: %s' % self.action
        print 'swp_id: %s' % self.swp_id

        if self.action == 'lookup':
            print 'lookup mode'

            total_matches = 0
            items = []

            if self.swp_id:
                items = Request.objects.filter(swp_id=self.swp_id)
            else:
                items = Request.objects.filter(status=0)[self.offset:(self.limit + self.offset)]

            for item in items:
                ml = MediaLookup()

                try:
                    num_recordings, recordings, level = ml.run(item)
                    item.num_results = num_recordings
                    item.results_mb = recordings

                    if level > 1:
                        item.level = level
                    else:
                        level = None

                    item.status = 1

                except Exception, e:

                    print
                    print
                    print '********* ERROR ********************'
                    print e
                    print '************************************'

                    item.status = 99

                item.save()

                if num_recordings > 0:
                    total_matches += 1


                print '********'
                print recordings
                print '********'




            print
            print '############# SUMMARY ############'
            print 'num queried: %s' % items.count()
            print 'num matches: %s' % total_matches



        if self.action == 'match':
            print 'match mode'

            total_matches = 0
            items = []

            mm = MediaMatch()

            if self.swp_id:
                items = Request.objects.filter(swp_id=self.swp_id)
            else:
                items = Request.objects.filter(status=1, num_results__gte=1)[self.offset:(self.limit + self.offset)]

            for item in items:


                mm.match(item)

                print '---------------------------------------------'
                print 'swp_id:    %s' % item.swp_id
                print 'title:     %s' % item.title
                print 'num_results:   %s' % item.num_results
                print 'level:   %s' % item.level
                print





            print
            print '############# SUMMARY ############'
            print 'num queried: %s' % items.count()
            print 'num matches: %s' % total_matches



        if self.action == 'reset':
            print 'legacy mode'

            items = Request.objects.all()[self.offset:(self.limit + self.offset)]

            for item in items:
                item.num_results = None
                item.level = None
                item.status = 0
                item.results_mb = None
                item.save()



            print
            print '############# SUMMARY ############'
            print 'num queried: %s' % items.count()


            Match.objects.all().delete()


        if self.action == 'legacy':
            print 'legacy mode'

            total_matches = 0
            items = []

            if self.swp_id:
                items = Request.objects.filter(swp_id=self.swp_id)
            else:
                items = Request.objects.all()[self.offset:(self.limit + self.offset)]

            for item in items:
                ll = LegacyLookup()
                num_recordings, recordings = ll.run(item)
                #item.num_results = num_recordings
                #item.save()
                if num_recordings > 0:
                    total_matches += 1


                print '********'
                print recordings
                print '********'




            print
            print '############# SUMMARY ############'
            print 'num queried: %s' % items.count()
            print 'num matches: %s' % total_matches






class Command(NoArgsCommand):
    """
    Import directory structure into alibrary:

        manage.py import_folder --path=/tmp/assets/images
    """

    option_list = BaseCommand.option_list + (
        make_option('--action',
                    action='store',
                    dest='action',
                    default=None,
                    help='Import files located in the path into django-filer'),
        make_option('--swp_id',
                    action='store',
                    dest='swp_id',
                    default=None,
                    help='Specify an ID to run migration on'),
    )

    def handle_noargs(self, **options):
        worker = SpfWorker(**options)
        worker.run()
