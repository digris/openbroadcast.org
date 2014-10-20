#-*- coding: utf-8 -*-
import re
import hashlib
import pprint
from optparse import make_option
import logging

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand, NoArgsCommand


log = logging.getLogger(__name__)

ECHONEST_API_KEY = 'DC7YKF3VYN7R0LG1M'
MUSICBRAINZ_HOST = getattr(settings, 'MUSICBRAINZ_HOST', None)
DISCOGS_HOST = getattr(settings, 'DISCOGS_HOST', None)
DEFAULT_LIMIT = 200


def md5_for_file(f, block_size=2 ** 20):
    md5 = hashlib.md5()
    while True:
        data = f.read(block_size)
        if not data:
            break
        md5.update(data)
    return md5.hexdigest()


class MetaWorker(object):
    def __init__(self, *args, **kwargs):
        self.action = kwargs.get('action')
        self.delete_missing = kwargs.get('delete_missing')
        self.pp = pprint.PrettyPrinter(indent=4)
        #self.pp.pprint = lambda d: None

        try:
            self.limit = int(kwargs.get('limit'))
        except:
            self.limit = DEFAULT_LIMIT

        try:
            self.id = int(kwargs.get('id'))
        except:
            self.id = None

        self.verbosity = int(kwargs.get('verbosity', 1))

    def run(self):

        log.info('maintenance walker')
        log.info('action: %s' % self.action)

        if self.action == 'lifespan':

            from alibrary.models import Artist
            from alibrary.models import APILookup


            if self.id:
                items = Artist.objects.filter(id=self.id)
            else:
                items = Artist.objects.all().order_by('name')[0:self.limit]

            for item in items:

                delete = False

                if not item.date_start:
                    log.info('no date_start for: %s' % item)
                    ctype = ContentType.objects.get_for_model(item)
                    al, created = APILookup.objects.get_or_create(content_type=ctype, object_id=item.id, provider='musicbrainz')
                    data = al.get_from_api()
                    al.delete()

                    if data and 'life-span' in data:
                        print data['life-span']
                        save = False
                        if 'begin' in data['life-span'] and data['life-span']['begin']:
                            date = data['life-span']['begin']
                            log.debug('got date: %s' % (date))
                            # TODO: rework field
                            if len(date) == 4:
                                date = '%s-00-00' % (date)
                            elif len(date) == 7:
                                date = '%s-00' % (date)
                            elif len(date) == 10:
                                date = '%s' % (date)

                            re_date = re.compile('^\d{4}-\d{2}-\d{2}$')
                            if re_date.match(date) and date != '0000-00-00':
                                item.date_start = '%s' % date
                                save = True

                        if 'end' in data['life-span'] and data['life-span']['end']:
                            date = data['life-span']['end']
                            log.debug('got date: %s' % (date))
                            # TODO: rework field
                            if len(date) == 4:
                                date = '%s-00-00' % (date)
                            elif len(date) == 7:
                                date = '%s-00' % (date)
                            elif len(date) == 10:
                                date = '%s' % (date)

                            re_date = re.compile('^\d{4}-\d{2}-\d{2}$')
                            if re_date.match(date) and date != '0000-00-00':
                                item.date_end = '%s' % date
                                save = True


                        if save:
                            try:
                                item.save()
                            except:
                                pass
                    #print data[0]['life-span']



        if self.action == 'lyrics':
            # using http://sahib.github.io/python-glyr/

            from alibrary.models import Media
            import plyr

            ms = Media.objects.filter(lyrics=None)

            print 'tracks without lyrics: %s' % ms.count()

            for m in ms:

                if m.name and m.artist.name:

                    print '%s - %s' % (m.name, m.artist.name)

                    q = plyr.Query(get_type='lyrics', artist=u'%s' % m.artist.name, title=u'%s' % m.name, parallel=10, verbosity=2, fuzzyness=2)
                    result = q.commit()

                    try:
                        if len(result) > 0:
                            m.lyrics = result[0].data
                            m.save()

                    except UnicodeError as err:
                        print('Cannot display lyrics, conversion failed:', err)






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
        make_option('--id',
                    action='store',
                    dest='id',
                    default=None,
                    help='Specify an ID to run migration on'),
        make_option('--limit',
                    action='store',
                    dest='limit',
                    default=None,
                    help='Specify an ID to run migration on'),
        make_option('--delete_missing',
                    action='store_true',
                    dest='delete_missing',
                    default=None,
                    help='Delete missing items'),
    )

    def handle_noargs(self, **options):
        worker = MetaWorker(**options)
        worker.run()
