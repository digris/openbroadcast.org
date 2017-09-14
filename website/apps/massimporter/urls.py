# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^massimporter/$', views.MassimportListView.as_view(), name='massimporter-import-list'),
    url(r'^massimporter/(?P<uuid>[0-9a-f-]+)/$', views.MassimportDetailView.as_view(), name='massimporter-import-detail'),

]
