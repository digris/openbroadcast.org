from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required

from spf.views import matches_csv


urlpatterns = patterns('importer.views',

    url(r'^csv/$', login_required(matches_csv), name='spf-matches-csv'),

)