# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from .views import LicenseDetailView

urlpatterns = [
    url(
        r"^license/(?P<slug>[-\w]+)/$",
        LicenseDetailView.as_view(),
        name="alibrary-license-detail",
    )
]
