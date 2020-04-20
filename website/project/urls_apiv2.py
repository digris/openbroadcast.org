# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.reverse import reverse
from rest_framework.authtoken import views as auth_views


@api_view(["GET"])
@permission_classes([AllowAny])
def api_root(request, format=None):
    return Response(
        {
            "version": '0.2.0',
            # "abcast/emission": reverse(
            #     "api:emission-list", request=request, format=format
            # ),
            # "alibrary/playlist": reverse(
            #     "api:playlist-list", request=request, format=format
            # ),
            # "alibrary/artist": reverse(
            #     "api:artist-list", request=request, format=format
            # ),
            # "alibrary/release": reverse(
            #     "api:release-list", request=request, format=format
            # ),
            # "alibrary/track": reverse("api:media-list", request=request, format=format),
            # "search": reverse("api:search-index", request=request, format=format),
            # "player": reverse("api:player-index", request=request, format=format),
            # "profiles": reverse("api:profile-list", request=request, format=format),
            # "auth-token": reverse(
            #     "api:obtain-auth-token", request=request, format=format
            # ),
        }
    )


urlpatterns = [
    url(r"^$", api_root),
    url(r"^api-token-auth/", auth_views.obtain_auth_token, name="obtain-auth-token"),
    url("^abcast/", include("abcast.apiv2.urls")),
    url("^alibrary/", include("alibrary.apiv2.urls")),
    url("^search/", include("search.apiv2.urls")),
    url("^tags/", include("tagging_extra.apiv2.urls")),
    url("^player/", include("player.apiv2.urls")),
    url("^profiles/", include("profiles.apiv2.urls")),
    url("^collector/", include("collector.apiv2.urls")),
    url("^media-preflight/", include("media_preflight.apiv2.urls")),
    url("^statistics/", include("statistics.apiv2.urls")),
    url("^exporter/", include("exporter.apiv2.urls")),
    # w.i.p.
    url("^atracker/", include("atracker.apiv2.urls")),
    url("^rating/", include("arating.apiv2.urls")),
]
