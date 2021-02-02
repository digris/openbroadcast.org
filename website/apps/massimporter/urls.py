# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        r"^massimporter/$",
        views.MassimportListView.as_view(),
        name="massimporter-import-list",
    ),
    url(
        r"^massimporter/(?P<uuid>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$",
        views.MassimportDetailView.as_view(),
        name="massimporter-import-detail",
    ),
]
