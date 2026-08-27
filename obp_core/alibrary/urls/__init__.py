from django.conf.urls import include, url

from . import artists as urls_artist
from . import labels as urls_label
from . import media as urls_media
from . import playlists as urls_playlist
from . import releases as urls_release

app_name = "alibrary"
urlpatterns = [
    url(r"^releases/", include(urls_release)),
    url(r"^artists/", include(urls_artist)),
    url(r"^tracks/", include(urls_media)),
    url(r"^labels/", include(urls_label)),
    url(r"^playlists/", include(urls_playlist)),
]
