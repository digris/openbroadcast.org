from django.conf.urls import url

from . import views

app_name = "collection"
urlpatterns = [
    url(r"^$", views.CollectionListView.as_view(), name="collection-list"),
    url(
        r"^(?P<slug>[0-9a-z-\_]+)/$",
        views.CollectionDetailView.as_view(),
        name="collection-detail",
    ),
]
