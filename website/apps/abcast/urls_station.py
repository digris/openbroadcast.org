from django.conf.urls import url
from abcast import views

app_name = "abcast"

urlpatterns = [
    url(r"^$", views.StationListView.as_view(), name="station-list"),
    url(
        r"^(?P<uuid>[0-9A-Fa-f-]+)/(?:(?P<section>[-\w]+)/)?$",
        views.StationDetailView.as_view(),
        name="station-detail",
    ),
]
