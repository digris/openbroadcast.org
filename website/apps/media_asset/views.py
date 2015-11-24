# -*- coding: utf-8 -*-
import logging
import os

import time
from alibrary.models import Media
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import View


from models import Waveform, Format

log = logging.getLogger(__name__)

WAVEFORM_TYPES = [
    's', 'w'
]

class WaveformView(View):
    """
    test with:
    http://local.openbroadcast.org:8080/media-asset/waveform/s/a9de1c5a-c1ca-4786-b5be-fdb5046ef212.png
    """
    def get(self, request, *args, **kwargs):

        media_uuid = kwargs.get('media_uuid', None)
        type = kwargs.get('type', None)
        media = get_object_or_404(Media, uuid=media_uuid)

        waveform, waveform_created = Waveform.objects.get_or_create(media=media, type=type)
        # if waveform_created:
        #     waveform.status = Waveform.PROCESSING
        #     waveform.save()

        print 'created: %s' %  waveform_created

        print 'uuid: %s' % media_uuid
        print 'type: %s' % type
        print 'path: %s' % waveform.path


        # hack to wait until file is ready
        while waveform.status in [Waveform.INIT, Waveform.PROCESSING]:
            log.debug('waveform not ready yet. sleep for a while')
            time.sleep(2)
            waveform.refresh_from_db()

        # set access timestamp
        Waveform.objects.filter(pk=waveform.pk).update(accessed=timezone.now())

        waveform_data = open(waveform.path, "rb").read()
        return HttpResponse(waveform_data, content_type='image/png')


class FormatView(View):
    """
    test with:
    http://local.openbroadcast.org:8080/media-asset/format/10240118-cb99-40f6-92f9-e964dd3372e4/default.mp3
    http://local.openbroadcast.org:8080/media-asset/format/10240118-cb99-40f6-92f9-e964dd3372e4/lo.mp3
    """
    def get(self, request, *args, **kwargs):

        media_uuid = kwargs.get('media_uuid', None)
        quality = kwargs.get('quality', None)
        encoding = kwargs.get('encoding', None)
        media = get_object_or_404(Media, uuid=media_uuid)

        stream_permission = False

        if request.user and request.user.has_perm('alibrary.play_media'):
            stream_permission = True


        if not stream_permission:
            log.warning('unauthorized attempt by "%s" to download: %s - "%s"' % (request.user.username if request.user else 'unknown', media.pk, media.name))
            raise PermissionDenied


        format, format_created = Format.objects.get_or_create(media=media, quality=quality, encoding=encoding)
        # if waveform_created:
        #     waveform.status = Waveform.PROCESSING
        #     waveform.save()

        print 'created: %s' %  format_created

        print 'uuid: %s' % media_uuid
        print 'quality: %s' % quality
        print 'encoding: %s' % encoding
        print 'path: %s' % format.path


        # hack to wait until file is ready
        while format.status in [Format.INIT, Format.PROCESSING]:
            log.debug('format not ready yet. sleep for a while')
            time.sleep(2)
            format.refresh_from_db()

        try:
            from atracker.util import create_event
            create_event(request.user, media, None, 'stream')
        except:
            pass

        # set access timestamp
        Format.objects.filter(pk=format.pk).update(accessed=timezone.now())


        data = open(format.path, "rb").read()
        #return HttpResponse(data, content_type='audio/mpeg')

        response = HttpResponse(data, content_type='audio/mpeg')
        response['Content-Length'] = format.filesize

        return response


