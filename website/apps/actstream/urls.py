from django.conf.urls import url, include
from actstream.views import ActionListView

urlpatterns = [
    url(r"^$", ActionListView.as_view(), name="actstream-action-list"),
    url(r"^", include("actstream.urls")),
]
