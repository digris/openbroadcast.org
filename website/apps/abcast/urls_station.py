# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from abcast import views

urlpatterns = [
    url(r"^$", views.StationListView.as_view(), name="abcast-station-list"),
    # url(
    #     r"^(?P<uuid>[0-9A-Fa-f-]+)/$",
    #     views.StationDetailView.as_view(),
    #     name="abcast-station-detail",
    # ),
    url(
        r"^(?P<uuid>[0-9a-f-]+)/(?:(?P<section>[-\w]+)/)?$",
        views.StationDetailView.as_view(),
        name="abcast-station-detail",
    ),
]
