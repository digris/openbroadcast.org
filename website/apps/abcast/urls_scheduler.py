# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from abcast import views

urlpatterns = [
    url(r"^$", views.SchedulerIndex.as_view(), name="scheduler-index"),
    url(
        r"^emssion/(?P<pk>\d+)/$",
        views.EmissionDetailView.as_view(),
        name="abcast-emission-detail",
    ),
]
