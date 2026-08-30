from django.conf.urls import url, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register(r"artist", views.ArtistViewSet)
router.register(r"label", views.LabelViewSet)
router.register(r"release", views.ReleaseViewSet)
router.register(r"media", views.MediaViewSet)

# app_name = "alibrary"
urlpatterns = [
    url(r"^playlist/$", views.playlist_list, name="playlist-list"),
    url(
        r"^playlist/collect/$",
        views.playlist_list_collect,
        name="playlist-list-collect",
    ),
    url(
        r"^playlist/(?P<uuid>[0-9A-Fa-f-]+)/$",
        views.playlist_detail,
        name="playlist-detail",
    ),
    url(
        r"^media/(?P<uuid>[0-9A-Fa-f-]+)/download-master/$",
        views.media_download_master,
        name="media-download-master",
    ),
    url(
        r"^media/(?P<uuid>[0-9A-Fa-f-]+)/appearances/$",
        views.MediaAppearances.as_view(),
        name="media-appearances",
    ),
    # utilities
    url(
        r"^utils/merge-objects/$",
        views.ObjectMergeView.as_view(),
        name="utils-merge-objects",
    ),
    url(
        r"^utils/re-assign-objects/$",
        views.ObjectReassignView.as_view(),
        name="utils-re-assign-objects",
    ),
    # router
    url(r"^", include(router.urls)),
]
