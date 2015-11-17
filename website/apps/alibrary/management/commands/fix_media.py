#-*- coding: utf-8 -*-
import logging
import subprocess
from django.conf import settings
from django.core.management.base import NoArgsCommand

log = logging.getLogger(__name__)

FFPROBE_BINARY = getattr(settings, 'FFPROBE_BINARY')

class MediaFix(object):
    def __init__(self, * args, **kwargs):
        self.verbosity = int(kwargs.get('verbosity', 1))

    def fix_mp3_durations(self):

        from alibrary.models import Media

        print
        print '-----------------------------------------------'
        print "Trying to fix media durations"
        print '-----------------------------------------------'
        print

        qs = Media.objects.filter(base_samplerate=22050, base_format='mp3', base_duration__lt=10)

        print 'Num. tracks:        %s' % Media.objects.count();
        print 'Without duration:   %s' % qs.count();

        for m in qs[0:10]:

            print '%s - %s' % (m.base_duration, m.name)

            try:
                p = subprocess.Popen([
                    FFPROBE_BINARY, m.master.path, "-show_format"
                ], stdout=subprocess.PIPE)
                stdout = p.communicate()

                dur = stdout[0].split('duration=')[1]
                dur = dur.split("\n")[0]
                print float(dur)

                m.base_duration = dur
                m.save()
            except Exception, e:
                print 'ERROR'
                print e

            print




        

class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        media_fix = MediaFix(**options)
        # file_importer.walker()
        media_fix.fix_mp3_durations()
