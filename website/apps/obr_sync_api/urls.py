# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter(schema_title="OBR Sync API")
router.register(r"artists", views.ArtistViewSet)

app_name = "obr-sync"
urlpatterns = [
    url(r"^", include(router.urls)),
]
