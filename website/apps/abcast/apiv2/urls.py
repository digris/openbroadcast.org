# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^emission/$', views.emission_list, name='emission-list'),
    url(r'^emission/(?P<uuid>[0-9A-Fa-f-]+)/$', views.emission_detail, name='emission-detail'),
    url(r'^channel/(?P<channel_uuid>[0-9A-Fa-f-]+)/emission/$', views.emission_list, name='channel-emission-list'),
]
