# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^profile/$", views.profile_list, name="profile-list"),
    url(
        r"^profiles/(?P<user_id>\d+)/$",
        views.profile_detail,
        name="profile-detail-by-userid",
    ),
    url(
        r"^profiles/(?P<uuid>[0-9A-Fa-f-]+)/$",
        views.profile_detail,
        name="profile-detail",
    ),
]
