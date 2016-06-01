from django.conf.urls import patterns, url

urlpatterns = patterns('',
    (r'^popup/$', 'aplayer.views.popup'),
)
