# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from alibrary import views


urlpatterns = [
    url(r"^$", views.MediaListView.as_view(), name="alibrary-media-list"),
    url(
        r"^(?P<pk>\d+)-(?P<slug>[-\w]+)/$",
        views.MediaDetailView.as_view(),
        name="alibrary-media-detail",
    ),
    url(
        r"^(?P<pk>\d+)/edit/$",
        views.MediaEditView.as_view(),
        name="alibrary-media-edit",
    ),
]
