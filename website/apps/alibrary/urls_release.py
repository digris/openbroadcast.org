from django.conf.urls.defaults import *

# app imports
from alibrary.views import *

urlpatterns = patterns('',
    
    url(r'^autocomplete/$', release_autocomplete, name='release_autocomplete'),
      
    url(r'^$', ReleaseListView.as_view(), dict(filters=[{'field':'account__username','relationship':'iexact'}], orders=[{'field':'foobar'}]), name='alibrary-release-list'),
    url(r'^(?P<slug>[-\w]+)/$', ReleaseDetailView.as_view(), name='alibrary-release-detail'),
    
    url(r'^(?P<pk>\d+)/edit/$', ReleaseEditView.as_view(), name='alibrary-release-edit'),

)