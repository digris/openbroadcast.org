# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from . import views

app_name = 'foo'
urlpatterns = [
    # media (a.k.a. track)
    url(r'^track/$', views.MediaListView.as_view(), name='media-list'),
    url(r'^track/(?P<pk>\d+)-(?P<slug>[-\w]+)/$', views.MediaDetailView.as_view(), name='media-detail'),
    url(r'^track/(?P<pk>\d+)/edit/$', views.MediaEditView.as_view(), name='media-edit'),
]
