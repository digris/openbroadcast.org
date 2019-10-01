# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from arating import views

urlpatterns = [
    url(
        r"^(?P<content_type>[\w.]+)/(?P<object_id>\d+)/(?P<vote>-?\d{1})/$",
        views.vote,
        name="vote",
    ),
    url(r"^(?P<content_type>[\w.]+)/(?P<object_id>\d+)/$", views.vote, name="vote"),
]
