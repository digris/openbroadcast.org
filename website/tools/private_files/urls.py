from django.conf.urls.defaults import *

urlpatterns = patterns('private_files.views',
    url(r'^(.+)/(.+)/(.+)/(.+)/(.+)$', 'get_file', name = 'private_files-file'),
)

