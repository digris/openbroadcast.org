# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^playlist/$', views.playlist_list, name='playlist-list'),
    url(r'^playlist/(?P<uuid>[0-9A-Fa-f-]+)/$', views.playlist_detail, name='playlist-detail'),

    url(r'^artist/$', views.artist_list, name='artist-list'),
    url(r'^artist/(?P<uuid>[0-9A-Fa-f-]+)/$', views.artist_detail, name='artist-detail'),

    url(r'^release/$', views.release_list, name='release-list'),
    url(r'^release/(?P<uuid>[0-9A-Fa-f-]+)/$', views.release_detail, name='release-detail'),

    url(r'^track/$', views.media_list, name='media-list'),
    url(r'^track/(?P<uuid>[0-9A-Fa-f-]+)/$', views.media_detail, name='media-detail'),

]
