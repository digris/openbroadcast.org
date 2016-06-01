from django.conf.urls import patterns, url
from alibrary.views import LicenseDetailView

urlpatterns = patterns('',
    url(r'^licenses/(?P<slug>[-\w]+)/$', LicenseDetailView.as_view(), name='alibrary-license-detail'),
)
