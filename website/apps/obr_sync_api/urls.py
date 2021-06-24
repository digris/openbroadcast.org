# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter(schema_title="OBR Sync API")
router.register(r"media", views.MediaViewSet)
router.register(r"artists", views.ArtistViewSet)
router.register(r"releases", views.ReleaseViewSet)
router.register(r"playlists", views.PlaylistViewSet)
router.register(r"profiles", views.ProfileViewSet)

app_name = "obr-sync"
urlpatterns = [
    url(r"^", include(router.urls)),
]
