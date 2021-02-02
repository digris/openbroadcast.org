# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        r"^$",
        views.ReleaseListView.as_view(),
        name="alibrary-release-list",
    ),
    url(
        r"^(?P<uuid>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/(?:(?P<section>[-\w]+)/)?$",
        views.ReleaseDetailView.as_view(),
        name="alibrary-release-detail",
    ),
    url(
        r"^(?P<pk>\d+)-(?P<slug>[-\w]+)/$",
        views.ReleaseDetailViewLegacy.as_view(),
        name="alibrary-release-detail-legacy",
    ),
    url(
        r"^(?P<pk>\d+)/edit/$",
        views.ReleaseEditView.as_view(),
        name="alibrary-release-edit",
    ),
]
