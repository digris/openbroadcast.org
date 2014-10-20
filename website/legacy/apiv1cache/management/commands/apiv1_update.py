# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option


from apiv1cache.models import ResourceMap


LIMIT = 10000


CLI_LINE = '-----------------------------------------------------------\n'

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



        from alibrary.models import Relation

        relations = Relation.objects.filter(service='discogs')

        num_updated = 0
        for relation in relations:
            try:
                print relation.url
                # try to get cache-map
                cached = ResourceMap.objects.get(v1_url=relation.url)
                print 'should be updated to: %s' % cached.v2_url
                if cached.v2_url[0:4] == 'http':
                    relation.url = cached.v2_url
                    relation.save()
                    num_updated += 1
            except Exception, e:
                pass

            print

        resources = ResourceMap.objects.filter(v2_url=None)[0:LIMIT]
        num_resources = resources.count()

        self.stdout.write('')
        self.stdout.write(CLI_LINE)
        self.stdout.write('loaded resources: %s' % num_resources)
        self.stdout.write(CLI_LINE)

        print 'updated: %s' % num_updated
