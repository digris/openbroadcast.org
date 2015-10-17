from django.conf.urls import *

# app imports
from alibrary.views import *

urlpatterns = patterns('',

    url(r'^licenses/(?P<slug>[-\w]+)/$', LicenseDetailView.as_view(), name='alibrary-license-detail'),

)