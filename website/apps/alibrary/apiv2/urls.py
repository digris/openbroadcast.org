# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^playlist/$', views.playlist_list, name='playlist-list'),
    url(r'^playlist/(?P<uuid>[0-9A-Fa-f-]+)/$', views.playlist_detail, name='playlist-detail'),

    url(r'^track/$', views.media_list, name='media-list'),
    url(r'^track/(?P<uuid>[0-9A-Fa-f-]+)/$', views.media_detail, name='media-detail'),

]
