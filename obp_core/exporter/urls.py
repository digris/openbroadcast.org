from django.conf.urls import url
from exporter import views
from exporter import views_ng

app_name = "exporter"
urlpatterns = [
    url(r"^$", views_ng.ExporterIndexView.as_view(), name="export-index"),
    url(r"^legacy/$", views.ExportListView.as_view(), name="export-list-legacy"),
    url(
        r"^delete-all/$",
        views.ExportDeleteAllView.as_view(),
        name="export-delete-all",
    ),
    url(
        r"^delete/(?P<pk>\d+)/$",
        views.ExportDeleteView.as_view(),
        name="export-delete",
    ),
    url(
        r"^download/(?P<uuid>[^//]+)/(?P<token>[^//]+)/$",
        views.export_download,
        name="export-download",
    ),
]
