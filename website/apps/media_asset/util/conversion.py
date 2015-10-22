from __future__ import unicode_literals
import os
import logging
import audiotools
log = logging.getLogger(__name__)

def any_to_wav(src, dst=None):

    if not os.path.isfile(src):
        raise IOError('unable to access %s' % src)

    audiotools.open(src).convert(dst, audiotools.WaveAudio)

    log.debug('to wav: %s > %s' % (src, dst))

    if os.path.isfile(dst):
        return dst
