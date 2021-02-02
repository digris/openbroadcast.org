# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        r"^$",
        views.PlaylistListView.as_view(scope="public"),
        name="alibrary-playlist-list",
    ),
    url(
        r"^(?P<uuid>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$",
        views.PlaylistDetailView.as_view(),
        name="alibrary-playlist-detail-legacy",
    ),
    url(
        r"^own/$",
        views.PlaylistListView.as_view(scope="own"),
        name="alibrary-playlist-list-own",
    ),
    url(
        r"^create/$",
        views.PlaylistCreateView.as_view(),
        name="alibrary-playlist-create",
    ),
    url(
        r"^(?P<pk>\d+)/edit/$",
        views.PlaylistEditView.as_view(),
        name="alibrary-playlist-edit-legacy",
    ),
    url(
        r"^(?P<pk>\d+)/delete/$",
        views.PlaylistDeleteView.as_view(),
        name="alibrary-playlist-delete",
    ),
    url(
        r"^(?P<pk>\d+)/convert/(?P<playlist_type>[-\w]+)/$",
        views.playlist_convert,
        name="alibrary-playlist-convert",
    ),
    url(
        r"^(?P<uuid>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/(?:(?P<section>[-\w]+)/)?$",
        views.PlaylistDetailView.as_view(),
        name="alibrary-playlist-detail",
    ),
    url(
        r"^edit/(?P<uuid>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/(?:(?P<section>[-\w]+)/)?$",
        views.PlaylistEditView.as_view(),
        name="alibrary-playlist-edit",
    ),
]
