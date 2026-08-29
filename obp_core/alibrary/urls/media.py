from django.conf.urls import url
from alibrary import views


urlpatterns = [
    url(
        r"^$",
        views.MediaListView.as_view(),
        name="media-list",
    ),
    url(
        r"^(?P<uuid>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/(?:(?P<section>[-\w]+)/)?$",
        views.MediaDetailView.as_view(),
        name="media-detail",
    ),
    url(
        r"^(?P<pk>\d+)/edit/$",
        views.MediaEditView.as_view(),
        name="media-edit",
    ),
]
