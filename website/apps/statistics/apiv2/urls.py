# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from django.conf.urls import url

from . import views

app_name = "statistics"
urlpatterns = [
    url(
        r"^usage-statistics/(?P<obj_ct>[a-z-_\.]+):(?P<obj_uuid>[0-9A-Fa-f-]+)/$",
        views.UsageStatisticsView.as_view(),
        name="usage-statistics",
    )
]
