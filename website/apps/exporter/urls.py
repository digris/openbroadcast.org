# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from exporter import views
from exporter import views_ng

urlpatterns = [
    url(r"^$", views_ng.ExporterIndexView.as_view(), name="exporter-export-index"),
    url(
        r"^legacy/$", views.ExportListView.as_view(), name="exporter-export-list-legacy"
    ),
    url(
        r"^delete-all/$",
        views.ExportDeleteAllView.as_view(),
        name="exporter-export-delete-all",
    ),
    url(
        r"^delete/(?P<pk>\d+)/$",
        views.ExportDeleteView.as_view(),
        name="exporter-export-delete",
    ),
    url(
        r"^download/(?P<uuid>[^//]+)/(?P<token>[^//]+)/$",
        views.export_download,
        name="exporter-export-download",
    ),
]
