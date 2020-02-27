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
        r"^(?P<uuid>[0-9a-f-]+)/$",
        views.PlaylistDetailView.as_view(),
        name="alibrary-playlist-detail",
    ),
    url(
        r"^(?P<pk>\d+)/edit/$",
        views.PlaylistEditView.as_view(),
        name="alibrary-playlist-edit",
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
]
