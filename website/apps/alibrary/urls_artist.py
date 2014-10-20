from django.conf.urls.defaults import *

# app imports
from alibrary.views import ArtistDetailView, ArtistListView, ArtistEditView, artist_autocomplete

urlpatterns = patterns('',
                       
    url(r'^autocomplete/$', artist_autocomplete, name='alibrary-artist-autocomplete'),
      
    url(r'^$', ArtistListView.as_view(), name='alibrary-artist-list'),              
    url(r'^(?P<slug>[-\w]+)/$', ArtistDetailView.as_view(), name='alibrary-artist-detail'),
    
    url(r'^(?P<pk>\d+)/edit/$', ArtistEditView.as_view(), name='alibrary-artist-edit'),

)