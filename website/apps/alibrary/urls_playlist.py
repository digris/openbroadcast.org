from django.conf.urls import url, patterns

# app imports
from alibrary.views import PlaylistListView, PlaylistCreateView, PlaylistDetailView, PlaylistEditView, PlaylistDeleteView, playlist_convert
urlpatterns = patterns('',

    url(r'^$', PlaylistListView.as_view(), name='alibrary-playlist-list'),
    
    url(r'^type/(?P<type>[-\w]+)/user/(?P<user>[-\w]+)/', PlaylistListView.as_view(), name='alibrary-playlist-type-list'),
    url(r'^type/(?P<type>[-\w]+)/', PlaylistListView.as_view(), name='alibrary-playlist-type-list'),
    url(r'^user/(?P<user>[-\w]+)/', PlaylistListView.as_view(), name='alibrary-playlist-user-list'),
    
    url(r'^create/$', PlaylistCreateView.as_view(), name='alibrary-playlist-create'),
    url(r'^(?P<slug>[-\w]+)/$', PlaylistDetailView.as_view(), name='alibrary-playlist-detail'),
    url(r'^(?P<pk>\d+)/edit/$', PlaylistEditView.as_view(), name='alibrary-playlist-edit'),
    url(r'^(?P<pk>\d+)/delete/$', PlaylistDeleteView.as_view(), name='alibrary-playlist-delete'),
    url(r'^(?P<pk>\d+)/convert/(?P<type>[-\w]+)/$', playlist_convert, name='alibrary-playlist-convert'),


)