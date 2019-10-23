# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^emission/$", views.emission_list, name="emission-list"),
    url(
        r"^emission/(?P<uuid>[0-9A-Fa-f-]+)/$",
        views.emission_detail,
        name="emission-detail",
    ),
    url(
        r"^channel/(?P<channel_uuid>[0-9A-Fa-f-]+)/emission/$",
        views.emission_list,
        name="channel-emission-list",
    ),
    # emission history for object
    # TODO: implement 'channel-aware' variant
    url(
        r"^history-for-object/(?P<obj_ct>[a-z-_\.]+):(?P<obj_uuid>[0-9A-Fa-f-]+)/$",
        views.emission_history,
        name="emission-history",
    ),
    # schedule data needed for radio site
    # TODO: implement multi-channel version
    url(r"^flattened-schedule/$", views.flattened_schedule, name="flattened-schedule"),
    # schedule data needed for playout / pypo
    # TODO: check implementation in pypo (currently not used)
    url(r"^playout-schedule/$", views.playout_schedule, name="playout-schedule"),
]
