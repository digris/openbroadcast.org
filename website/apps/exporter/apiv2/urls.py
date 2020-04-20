# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter(schema_title='Exporter API')
router.register(r"export", views.ExportViewSet)

app_name = "exporter"
urlpatterns = [
    url(r"^", include(router.urls)),
]
