from django.conf.urls.defaults import *

# app imports
from alibrary.views import LabelDetailView, LabelListView, LabelEditView, label_autocomplete

urlpatterns = patterns('',
                       
    url(r'^autocomplete/$', label_autocomplete, name='alibrary-label-autocomplete'),
      
    url(r'^$', LabelListView.as_view(), name='alibrary-label-list'),              
    url(r'^(?P<slug>[-\w]+)/$', LabelDetailView.as_view(), name='alibrary-label-detail'),
    
    url(r'^(?P<pk>\d+)/edit/$', LabelEditView.as_view(), name='alibrary-label-edit'),

)