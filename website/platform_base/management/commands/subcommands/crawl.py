# -*- coding: utf-8 -*-
import sys
from django.core.management.base import NoArgsCommand, CommandError, BaseCommand
from platform_base.management.commands.subcommands.base import SubcommandsCommand
from alibrary.util.api_crawler import MBCeawler
from alibrary.models import Artist, Media
from tqdm import tqdm
import time
from django.conf import settings
import logging
import requests
import xmltodict
import json
import types
from django.db.models import Q
from django.db.models.functions import Length

log = logging.getLogger(__name__)

MUSICBRAINZ_HOST = getattr(settings, 'MUSICBRAINZ_HOST', None)

class CrawlIdentifiersCommand(SubcommandsCommand):

    help = 'complete missing identifiers: isni, isrc, iswc'

    def handle(self, *args, **options):


        qs = Media.objects.annotate(isrc_length=Length('isrc')).filter(isrc_length__lt=1, relations__service='musicbrainz').nocache()
        print 'num media: {}'.format(qs.count())

        for item in tqdm(qs):
        #for item in qs:

            url = item.relations.filter(service='musicbrainz')[0].url
            provider_id = url.split('/')[-1]

            #print provider_id

            if not len(provider_id) == 36:
                provider_id = None

            if provider_id:

                inc = ('isrcs',)
                api_url = 'http://%s/ws/2/recording/%s/?fmt=json&inc=%s' % (MUSICBRAINZ_HOST, provider_id, "+".join(inc))

                r = requests.get(api_url)

                if not r.status_code == 200:
                    print 'url: {}'.format(api_url)
                    print 'request error: {}'.format(r.text)

                data = r.json()
                isrc_code = None
                if 'isrcs' in data:
                    isrcs = data['isrcs']
                    if isinstance(isrcs, types.ListType) and len(isrcs) > 0:
                        isrc_code = isrcs[0]
                    elif isinstance(isrcs, types.StringType):
                        isrc_code = isrcs

                if isrc_code:
                    print isrc_code
                    Media.objects.filter(pk=item.pk).update(isrc=isrc_code)



        qs = Artist.objects.annotate(isni_code_length=Length('isni_code')).filter(isni_code_length__lt=1, relations__service='musicbrainz').nocache()
        print 'artists: {}'.format(qs.count())

        for item in tqdm(qs):
            url = item.relations.filter(service='musicbrainz')[0].url
            provider_id = url.split('/')[-1]

            if not len(provider_id) == 36:
                return

            api_url = 'http://%s/ws/2/artist/%s/?fmt=xml' % (MUSICBRAINZ_HOST, provider_id)
            r = requests.get(api_url)

            if not r.status_code == 200:
                print 'url: {}'.format(api_url)
                print 'request error: {}'.format(r.text)

            else:

                item_metadata = json.loads(json.dumps(xmltodict.parse(r.text)))['metadata']['artist']
                isni_code = None

                if 'isni-list' in item_metadata and 'isni' in item_metadata['isni-list']:
                    isni_code = item_metadata['isni-list']['isni']
                    if isinstance(isni_code, types.ListType):
                        isni_code = isni_code[0]

                if isni_code:
                    print 'ISNI: {}'.format(isni_code)
                    Artist.objects.filter(pk=item.pk).update(isni_code=isni_code)
        #
        #
        # qs = Artist.objects.annotate(ipi_code_length=Length('ipi_code')).filter(ipi_code_length__lt=1, relations__service='musicbrainz').nocache()
        # print 'artists: {}'.format(qs.count())
        #
        # for item in tqdm(qs):
        #     url = item.relations.filter(service='musicbrainz')[0].url
        #     provider_id = url.split('/')[-1]
        #
        #     if not len(provider_id) == 36:
        #         return
        #
        #     api_url = 'http://%s/ws/2/artist/%s/?fmt=xml' % (MUSICBRAINZ_HOST, provider_id)
        #     r = requests.get(api_url)
        #
        #     if not r.status_code == 200:
        #         print 'url: {}'.format(api_url)
        #         print 'request error: {}'.format(r.text)
        #
        #     else:
        #
        #         item_metadata = json.loads(json.dumps(xmltodict.parse(r.text)))['metadata']['artist']
        #         ipi_code = None
        #
        #         if ipi_code:
        #             print 'IPI:  {}'.format(ipi_code)
        #             Artist.objects.filter(pk=item.pk).update(ipi_code=ipi_code)





class MBCrawlerCommand(SubcommandsCommand):
    help_string = 'Crawl musicbrainz and complete missing information.'
    command_name = 'crawl_mb'
    subcommands = {
        'identifiers': CrawlIdentifiersCommand,
    }