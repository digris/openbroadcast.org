from django.conf.urls import url, include
from actstream.views import ActionListView

app_name = "actstream"

urlpatterns = [
    url(r"^$", ActionListView.as_view(), name="action-list"),
    url(r"^", include("actstream.urls_orig")),
]
