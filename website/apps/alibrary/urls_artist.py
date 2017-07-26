# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from .views import ArtistDetailView, ArtistListView, ArtistEditView, artist_autocomplete

urlpatterns = [
    url(r'^autocomplete/$', artist_autocomplete, name='alibrary-artist-autocomplete'),
    url(r'^$', ArtistListView.as_view(), name='alibrary-artist-list'),
    url(r'^(?P<pk>\d+)-(?P<slug>[-\w]+)/$', ArtistDetailView.as_view(), name='alibrary-artist-detail'),
    url(r'^(?P<pk>\d+)/edit/$', ArtistEditView.as_view(), name='alibrary-artist-edit'),
]
