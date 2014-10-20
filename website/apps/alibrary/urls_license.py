from django.conf.urls.defaults import *

# app imports
from alibrary.views import *

urlpatterns = patterns('',

    url(r'^license/(?P<slug>[-\w]+)/$', LicenseDetailView.as_view(), name='alibrary-license-detail'),

)