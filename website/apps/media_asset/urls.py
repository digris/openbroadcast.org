# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import include, url
from views import WaveformView, FormatView

urlpatterns = [
    url(r'^waveform/(?P<type>[-\w]+)/(?P<media_uuid>[-\w]+).png$', WaveformView.as_view(), name='mediaasset-waveform'),
    url(r'^format/(?P<media_uuid>[-\w]+)/(?P<quality>[-\w]+).(?P<encoding>[-\w]+)$', FormatView.as_view(), name='mediaasset-format'),
]
