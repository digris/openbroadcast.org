from django.conf.urls.defaults import *
from django.views.generic import ListView

from django.views.generic.simple import direct_to_template

# app imports
from alibrary.models import Artist

# restfrom alibrary.resources import *

urlpatterns = patterns('',
                       
    (r'^aaaartists/$', ListView.as_view(
        #model=Artist,
        queryset=Artist.objects.order_by("name"),
        #context_object_name="artist_list",
    )),
                       
    url('^ajax/', include('alibrary.ajax.urls')),
    
    url(r'^crossdomain.xml$', direct_to_template, {'template': 'lib/crossdomain.xml', 'mimetype': 'application/xml'}),
    url(r'^crossdomain.xml/$', direct_to_template, {'template': 'lib/crossdomain.xml', 'mimetype': 'application/xml'}),


    
    
    # media                   
    #(r'^tracks/$', MediaListView.as_view()),              
    #url(r'^tracks/(?P<slug>[-\w]+)/$', MediaDetailView.as_view(), name='TrackDetailView'),
    
    # views to serve protected (buyed) files
    url(r'^releases/(?P<slug>[-\w]+)/download/(?P<format>[a-z0-9]+)/(?P<version>[a-z0-9]+)/$', 'alibrary.views.release_download', name='release-zip-view'),
    url(r'^tracks/(?P<slug>[-\w]+)/download/(?P<format>[a-z0-9]+)/(?P<version>[a-z0-9]+)/$', 'alibrary.views.media_download', name='media-zip-view'),
    
    # html5 stream
    url(r'^tracks/(?P<uuid>[-\w]+)/stream_html5/$', 'alibrary.views.stream_html5', name='alibrary-media-stream_html5'),
    
    
    # playlist urls (for embedding)
    url(r'^releases/(?P<slug>[-\w]+)/playlist/(?P<format>[a-z0-9]+)/(?P<version>[a-z0-9]+)/$', 'alibrary.views.release_playlist', name='release-playlist-view'),

    
    # REST-API urls
    # url(r'^api/$', direct_to_template, {'template': 'alibrary/api/index.html'}),

    
    
)