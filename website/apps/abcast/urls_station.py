from django.conf.urls.defaults import *

from abcast.views import StationListView, StationDetailView

urlpatterns = patterns('',   
    url(r'^$', StationListView.as_view(), name='abcast-station-list'),
    url(r'^(?P<slug>[-\w]+)/$', StationDetailView.as_view(), name='abcast-station-detail'),
)