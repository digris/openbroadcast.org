# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option



CLI_LINE = '-----------------------------------------------------------'

class Command(BaseCommand):
    help = 'Clear resource cache. Depends on DGSPROXY_CACHE_DURATION setting.'

    option_list = BaseCommand.option_list + (
        make_option('--all',
            action='store_true',
            dest='clear_all',
            default=False,
            help='Clear all resources (ignores DGSPROXY_CACHE_DURATION)'),
        )

    def handle(self, *args, **options):

        from alibrary.models.mediamodels import Media

        media_to_fix = Media.objects.filter(processed=99)
        media_to_fix_count = media_to_fix.count()

        for m in media_to_fix[0:50]:
            m.processed = 0
            m.save()

        print 'reprocessed %s files' % media_to_fix_count

    def __repr__(self):
        return super(Command, self).__repr__()
