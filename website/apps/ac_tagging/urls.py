from django.conf.urls import patterns, url

urlpatterns = patterns('ac_tagging.views',
    url(r'^list$', 'list_tags', name='ac_tagging-list'),
)
