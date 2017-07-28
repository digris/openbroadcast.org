from django.conf.urls import url, include
from actstream.views import ActionListView, ActionDetailView

urlpatterns = [
    url(r'^$', ActionListView.as_view(), name='actstream-action-list'),
    url(r'^de__tail/(?P<slug>[-\w]+)/$', ActionDetailView.as_view(), name='actstream-action-detail'),
    url(r'^', include('actstream.urls'))
]
