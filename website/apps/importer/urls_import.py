from django.conf.urls import url, patterns

from importer.views import ImportListView, ImportCreateView, ImportUpdateView, ImportDeleteView, ImportModifyView, ImportDeleteAllView, multiuploader

urlpatterns = patterns('',
                                               
    url(r'^$', ImportListView.as_view(), name='importer-import-list'),
    url(r'^create/$', ImportCreateView.as_view(), name='importer-import-create'),
    url(r'^(?P<pk>\d+)/$', ImportUpdateView.as_view(), name='importer-import-update'),
    
    url(r'^delete-all/$', ImportDeleteAllView.as_view(), name='importer-import-delete-all'),
    url(r'^delete/(?P<pk>\d+)/$', ImportDeleteView.as_view(), name='importer-import-delete'),
    url(r'^modify/(?P<pk>\d+)/$', ImportModifyView.as_view(), name='importer-import-modify'),
    
    # upload handler
    url(r'^multi/(?P<import_id>\d+)/$', multiuploader, name='importer-upload-multi'),

)