# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from views import WaveformView

urlpatterns = patterns('media_asset.views',
    url(r'^waveform/(?P<type>[-\w]+)/(?P<media_uuid>[-\w]+).png$', WaveformView.as_view(), name='mediaasset-waveform'),
)
