# -*- coding: utf-8 -*-
import datetime
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import Http404, HttpResponseRedirect
from django.http import HttpResponse
from django.views.generic import View
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from models import Waveform
from alibrary.models import Media

WAVEFORM_TYPES = ['s', 'w']

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

        waveform_data = open(waveform.path, "rb").read()
        return HttpResponse(waveform_data, content_type='image/png')





