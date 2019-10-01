# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from abcast.views import StationListView, StationDetailView

urlpatterns = [
    url(r"^$", StationListView.as_view(), name="abcast-station-list"),
    url(
        r"^(?P<slug>[-\w]+)/$",
        StationDetailView.as_view(),
        name="abcast-station-detail",
    ),
]
