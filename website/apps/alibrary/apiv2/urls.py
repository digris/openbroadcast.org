# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter(schema_title='Library API')
router.register(r"artist", views.ArtistViewSet)
router.register(r"label", views.LabelViewSet)
router.register(r"release", views.ReleaseViewSet)
router.register(r"playlist", views.PlaylistViewSet)
router.register(r"track", views.MediaViewSet)

app_name = "alibrary"
urlpatterns = [


    # url(r"^playlist/$", views.playlist_list, name="playlist-list"),
    url(
        r"^playlist/collect/$",
        views.playlist_list_collect,
        name="playlist-list-collect",
    ),
    # url(
    #     r"^playlist/(?P<uuid>[0-9A-Fa-f-]+)/$",
    #     views.playlist_detail,
    #     name="playlist-detail",
    # ),
    # url(r"^artist/$", views.artist_list, name="artist-list"),
    # url(
    #     r"^artist/(?P<uuid>[0-9A-Fa-f-]+)/$", views.artist_detail, name="artist-detail"
    # ),
    # url(r"^label/$", views.label_list, name="label-list"),
    # url(
    #     r"^label/(?P<uuid>[0-9A-Fa-f-]+)/$", views.label_detail, name="label-detail"
    # ),
    # url(r"^release/$", views.release_list, name="release-list"),
    # url(
    #     r"^release/(?P<uuid>[0-9A-Fa-f-]+)/$",
    #     views.release_detail,
    #     name="release-detail",
    # ),
    # url(r"^track/$", views.media_list, name="media-list"),
    # url(r"^track/(?P<uuid>[0-9A-Fa-f-]+)/$", views.media_detail, name="media-detail"),
    url(r"^track/(?P<uuid>[0-9A-Fa-f-]+)/download-master/$", views.media_download_master, name="media-download-master"),

    # utilities
    url(
        r"^utils/merge-objects/$",
        views.ObjectMergeView.as_view(),
        name="utils-merge-objects",
    ),
    # router
    url(r"^", include(router.urls)),
]
