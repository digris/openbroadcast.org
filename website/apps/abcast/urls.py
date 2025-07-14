from django.conf.urls import url
from abcast import views

app_name = "abcast"
urlpatterns = [
    url(r"^$", views.SchedulerIndex.as_view(), name="scheduler"),
    url(
        r"^emssion/(?P<pk>\d+)/$",
        views.EmissionDetailView.as_view(),
        name="emission-detail",
    ),
]
