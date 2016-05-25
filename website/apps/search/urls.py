from django.conf.urls import patterns, url

urlpatterns = patterns('search.views',
    url(r'^$', 'index', name='search-index'),
    url(r'^autocomplete/$', 'autocomplete', name='search-autocomplete'),
)
