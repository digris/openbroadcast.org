# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r"^check/(?P<uuid>[0-9A-Fa-f-]+)/$",
        views.preflight_check_detail,
        name="preflight-check-detail",
    )
]
