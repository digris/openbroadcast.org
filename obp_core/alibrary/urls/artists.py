from django.conf.urls import url
from alibrary import views


urlpatterns = [
    url(
        r"^$",
        views.ArtistListView.as_view(),
        name="artist-list",
    ),
    url(
        r"^(?P<uuid>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/(?:(?P<section>[-\w]+)/)?$",
        views.ArtistDetailView.as_view(),
        name="artist-detail",
    ),
    url(
        r"^(?P<pk>\d+)/edit/$",
        views.ArtistEditView.as_view(),
        name="artist-edit",
    ),
]
