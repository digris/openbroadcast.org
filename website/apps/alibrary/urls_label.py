# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        r"^$",
        views.LabelListView.as_view(),
        name="alibrary-label-list",
    ),
    url(
        r"^(?P<uuid>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/(?:(?P<section>[-\w]+)/)?$",
        views.LabelDetailView.as_view(),
        name="alibrary-label-detail",
    ),
    url(
        r"^(?P<pk>\d+)-(?P<slug>[-\w]+)/$",
        views.LabelDetailViewLegacy.as_view(),
        name="alibrary-label-detail-legacy",
    ),
    url(
        r"^(?P<pk>\d+)/edit/$",
        views.LabelEditView.as_view(),
        name="alibrary-label-edit",
    ),
    url(
        r"^(?P<pk>\d+)/statistics-download/$",
        views.LabelStatisticsDownloadView.as_view(),
        name="alibrary-label-statistics-download",
    ),
]
