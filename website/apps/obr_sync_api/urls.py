# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter(schema_title="OBR Sync API")
# alibrary
router.register(r"media", views.MediaViewSet)
router.register(r"artists", views.ArtistViewSet)
router.register(r"releases", views.ReleaseViewSet)
router.register(r"playlists", views.PlaylistViewSet)
# profiles
router.register(r"profiles", views.ProfileViewSet)
# abcast
router.register(r"emissions", views.EmissionViewSet)
# arating
router.register(r"votes", views.VoteViewSet)

app_name = "obr-sync"
urlpatterns = [
    url(r"^", include(router.urls)),
    url(
        r"^media/(?P<uuid>[0-9A-Fa-f-]+)/download-master/$",
        views.MediaMasterDwonloadView.as_view(),
    ),
]
