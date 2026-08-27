from django.conf.urls import url
from importer import views

app_name = "importer"
urlpatterns = [
    url(r"^$", views.ImportListView.as_view(), name="import-list"),
    url(r"^create/$", views.ImportCreateView.as_view(), name="import-create"),
    url(
        r"^(?P<pk>\d+)/$",
        views.ImportUpdateView.as_view(),
        name="import-update",
    ),
    url(
        r"^delete-all/$",
        views.ImportDeleteAllView.as_view(),
        name="import-delete-all",
    ),
    url(
        r"^delete/(?P<pk>\d+)/$",
        views.ImportDeleteView.as_view(),
        name="import-delete",
    ),
    url(
        r"^modify/(?P<pk>\d+)/$",
        views.ImportModifyView.as_view(),
        name="import-modify",
    ),
]
