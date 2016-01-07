# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url, patterns

from .views import IPTrackerView

urlpatterns = patterns('exporter.views',
    url(r'^$', IPTrackerView.as_view(), name='iptracker-index'),
)