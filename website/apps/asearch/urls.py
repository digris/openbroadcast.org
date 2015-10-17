from django.conf.urls import *

urlpatterns = patterns('asearch.views',
    url(r'^autocomplete/$', 'autocomplete', name='asearch-autocomplete'),
)
