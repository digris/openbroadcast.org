# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from importer import views

urlpatterns = [
    url(r"^$", views.ImportListView.as_view(), name="importer-import-list"),
    url(r"^create/$", views.ImportCreateView.as_view(), name="importer-import-create"),
    url(
        r"^(?P<pk>\d+)/$",
        views.ImportUpdateView.as_view(),
        name="importer-import-update",
    ),
    url(
        r"^delete-all/$",
        views.ImportDeleteAllView.as_view(),
        name="importer-import-delete-all",
    ),
    url(
        r"^delete/(?P<pk>\d+)/$",
        views.ImportDeleteView.as_view(),
        name="importer-import-delete",
    ),
    url(
        r"^modify/(?P<pk>\d+)/$",
        views.ImportModifyView.as_view(),
        name="importer-import-modify",
    ),
]
