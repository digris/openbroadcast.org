from django.conf.urls import patterns, url




from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^post/$', 'backfeed.views.post', name='backfeed-views-post'),
)

