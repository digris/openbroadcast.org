#-*- coding: utf-8 -*-
import logging
import shutil
from django.conf import settings
from django.core.management.base import NoArgsCommand

MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT', None)

log = logging.getLogger(__name__)

class MediaFix(object):
    def __init__(self, * args, **kwargs):
        self.verbosity = int(kwargs.get('verbosity', 1))

    def copy_from_import(self):

        from alibrary.models import Media

        print
        print '-----------------------------------------------'
        print 'replacing corrupt files with import versions'
        print '-----------------------------------------------'
        print

        qs = Media.objects.filter(base_format='m4a', id__gte=387750)

        print 'files in qs:   %s' % qs.count()

        for m in qs:

            print '%s' % (m.name)

            src = m.importfile_media.all()[0].file.path
            dst = m.master.path

            print 'src: %s' % src
            print 'dst: %s' % dst

            shutil.copy(src, dst)

            print






class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        media_fix = MediaFix(**options)
        media_fix.copy_from_import()
