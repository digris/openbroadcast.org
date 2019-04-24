# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from alibrary.views import PlaylistListView, PlaylistCreateView, PlaylistDetailView, PlaylistEditView, PlaylistDeleteView, playlist_convert

urlpatterns = [

    url(r'^$', PlaylistListView.as_view(scope='public'), name='alibrary-playlist-list'),
    url(r'^own/$', PlaylistListView.as_view(scope='own'), name='alibrary-playlist-list-own'),

    url(r'^create/$', PlaylistCreateView.as_view(), name='alibrary-playlist-create'),
    url(r'^(?P<slug>[-\w]+)/$', PlaylistDetailView.as_view(), name='alibrary-playlist-detail'),
    url(r'^(?P<pk>\d+)/edit/$', PlaylistEditView.as_view(), name='alibrary-playlist-edit'),
    url(r'^(?P<pk>\d+)/delete/$', PlaylistDeleteView.as_view(), name='alibrary-playlist-delete'),
    url(r'^(?P<pk>\d+)/convert/(?P<type>[-\w]+)/$', playlist_convert, name='alibrary-playlist-convert'),

]
