from django.conf.urls.defaults import *

urlpatterns = patterns('',
    #url(r'^jingle/(?P<uuid>[-\w]+)/stream_html5/base.mp3$', 'alibrary.views.stream_html5', name='alibrary-media-stream_html5'),
    url(r'^jingle/(?P<uuid>[-\w]+)/waveform/$', 'abcast.views.waveform', name='abcast-jingle-waveform'),

)