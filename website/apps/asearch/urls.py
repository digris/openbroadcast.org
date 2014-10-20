from django.conf.urls.defaults import *

urlpatterns = patterns('asearch.views',
    url(r'^autocomplete/$', 'autocomplete', name='asearch-autocomplete'),
)
