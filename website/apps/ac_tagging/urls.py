from django.conf.urls.defaults import *

urlpatterns = patterns('ac_tagging.views',
    url(r'^list$', 'list_tags', name='ac_tagging-list'),
)
