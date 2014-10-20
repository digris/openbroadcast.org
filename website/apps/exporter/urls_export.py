from django.conf.urls import url, patterns

from exporter.views import ExportListView, ExportUpdateView, ExportDeleteAllView,\
    ExportDeleteView, export_download

urlpatterns = patterns('exporter.views',
                                               
    url(r'^$', ExportListView.as_view(), name='exporter-export-list'),
    url(r'^settings/$', ExportListView.as_view(), name='exporter-export-settings'),
    url(r'^(?P<pk>\d+)/$', ExportUpdateView.as_view(), name='exporter-export-update'),

    url(r'^delete-all/$', ExportDeleteAllView.as_view(), name='exporter-export-delete-all'),
    url(r'^delete/(?P<pk>\d+)/$', ExportDeleteView.as_view(), name='exporter-export-delete'),
    
    url(r'^download/(?P<uuid>[^//]+)/(?P<token>[^//]+)/$', export_download, name='exporter-export-download'),

)