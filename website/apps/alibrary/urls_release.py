# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^$", views.ReleaseListView.as_view(), name="alibrary-release-list"),
    url(
        r"^(?P<pk>\d+)-(?P<slug>[-\w]+)/$",
        views.ReleaseDetailViewLegacy.as_view(),
        name="alibrary-release-detail-legacy",
    ),
    url(
        r"^(?P<pk>\d+)/edit/$", views.ReleaseEditView.as_view(), name="alibrary-release-edit"
    ),
    url(
        r"^(?P<uuid>[0-9a-f-]+)/(?:(?P<section>[-\w]+)/)?$",
        views.ReleaseDetailView.as_view(),
        name="alibrary-release-detail",
    ),
]
