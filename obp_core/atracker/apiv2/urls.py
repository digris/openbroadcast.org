from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r"^event/(?P<obj_ct>[a-z-_\.]+):(?P<obj_uuid>[0-9A-Fa-f-]+)/$",
        views.ObjectEventView.as_view(),
        name="event-detail",
    )
]
