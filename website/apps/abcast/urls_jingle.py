from django.conf.urls import url, patterns

urlpatterns = patterns('',
    url(r'^jingle/(?P<uuid>[-\w]+)/waveform/$', 'abcast.views.waveform', name='abcast-jingle-waveform'),
)
