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
        r"^(?P<uuid>[0-9A-Fa-f-]+)/(?:(?P<section>[-\w]+)/)?$",
        views.StationDetailView.as_view(),
        name="abcast-station-detail",
    ),
    # url(
    #     r"^(?P<uuid>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/(?:(?P<section>[-\w]+)/)?$",
    #     views.StationDetailView.as_view(),
    #     name="abcast-station-detail",
    # ),
]
