#-*- coding: utf-8 -*-
import subprocess
import logging
from django.conf import settings
log = logging.getLogger(__name__)
__ALL__ = 'duration_audiotools', 'duration_ffmpeg'

FFPROBE_BINARY = getattr(settings, 'FFPROBE_BINARY')

def duration_audiotools(src):
    raise NotImplementedError


def duration_ffmpeg(src):

        try:
            probe_args = [
                FFPROBE_BINARY,
                src,
                '-loglevel',
                '-8',
                '-show_format'
            ]

            log.debug('calling %s' % ' '.join(probe_args))
            p = subprocess.Popen(probe_args, stdout=subprocess.PIPE)
            stdout = p.communicate()

            duration = stdout[0].split('duration=')[1]
            duration = float(duration.split("\n")[0]) * 1000

            log.debug('duration from ffmpeg: %s' % duration)

            return duration

        except Exception, e:
            log.warning(u'unable to process file at: %s - %S' % (src, e))
