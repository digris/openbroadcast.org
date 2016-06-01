from django.conf.urls import patterns, url, include
from actstream.views import ActionListView, ActionDetailView

urlpatterns = patterns('actstream.views',
    url(r'^$', ActionListView.as_view(), name='actstream-action-list'),
    url(r'^de__tail/(?P<slug>[-\w]+)/$', ActionDetailView.as_view(), name='actstream-action-detail'),
    url(r'^', include('actstream.urls'))
)
