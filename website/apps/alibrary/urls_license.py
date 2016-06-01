from django.conf.urls import patterns, url
from .views import LicenseDetailView

urlpatterns = patterns('',
    url(r'^license/(?P<slug>[-\w]+)/$', LicenseDetailView.as_view(), name='alibrary-license-detail'),
)
