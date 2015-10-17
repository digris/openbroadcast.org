from django.conf.urls import patterns, url

urlpatterns = patterns('ratings.views',
    url(r'^vote/$', 'vote', name='ratings_vote'),
)