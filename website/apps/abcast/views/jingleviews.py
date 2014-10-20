import os

from django.shortcuts import get_object_or_404
from django.conf import settings
from sendfile import sendfile

from abcast.models import Jingle


def waveform(request, uuid):
    
    obj = get_object_or_404(Jingle, uuid=uuid)

    if obj.get_cache_file('png', 'waveform'):
        waveform_file = obj.get_cache_file('png', 'waveform')
    else:
        waveform_file = os.path.join(settings.STATIC_ROOT, 'img/base/defaults/waveform.png')

    return sendfile(request, waveform_file)