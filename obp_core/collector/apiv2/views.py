import logging

from django.conf import settings
from django.db.models import Q


from rest_framework.decorators import api_view
from rest_framework.response import Response

# from .serializers import ReleaseSerializer
from alibrary.apiv2.serializers import PlaylistSerializer
from alibrary.models.playlistmodels import Playlist

SITE_URL = settings.SITE_URL

SERIALIZER_MAP = {"alibrary.playlist": PlaylistSerializer}

log = logging.getLogger(__name__)


@api_view(["GET"])
def playlist_list(request, **kwargs):

    results = []

    q = request.GET.get("q", "").strip()

    qs = Playlist.objects.filter(
        user=request.user, type__in=["basket", "playlist"]
    ).order_by("-updated")

    if q != "":
        qs = qs.filter(Q(name__istartswith=q) | Q(series__name__istartswith=q))

    serializer = PlaylistSerializer(qs[0:100], many=True, context={"request": request})

    return Response({"results": serializer.data})
