from django.conf.urls import include, url

from alibrary.views.releaseviews import ReleaseListView, ReleaseDetailView, ReleaseEditView

from alibrary import urls_release, urls_artist, urls_label, urls_media, urls_playlist

app_name = "alibrary"
urlpatterns = [
    # url(
    #     r"^releases/",
    #     ReleaseListView.as_view(),
    #     name="release-list"
    # ),
    url(
        r"^releases/",
        include(urls_release)
    ),
    url(
        r"^artists/",
        include(urls_artist)
    ),
    url(
        r"^tracks/",
        include(urls_media)
    ),
    url(
        r"^labels/",
        include(urls_label)
    ),
    url(
        r"^playlists/",
        include(urls_playlist)
    ),
]
