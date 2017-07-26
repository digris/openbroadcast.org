# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from alibrary.views import LicenseDetailView

urlpatterns = [
    url(r'^licenses/(?P<slug>[-\w]+)/$', LicenseDetailView.as_view(), name='alibrary-license-detail'),
]
