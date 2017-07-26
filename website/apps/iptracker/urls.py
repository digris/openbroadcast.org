# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from .views import IPTrackerView

urlpatterns = [
    url(r'^$', IPTrackerView.as_view(), name='iptracker-index'),
]
