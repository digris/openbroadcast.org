import logging

from django.apps import apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponseBadRequest

from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import MediaObjSerializer, ArtistObjSerializer, ProfileObjSerializer
from alibrary.apiv2.serializers import ReleaseSerializer, PlaylistSerializer

SITE_URL = getattr(settings, "SITE_URL")

SERIALIZER_MAP = {
    # library
    "alibrary.release": ReleaseSerializer,
    "alibrary.playlist": PlaylistSerializer,
    "alibrary.media": MediaObjSerializer,
    "alibrary.artist": ArtistObjSerializer,
    # user
    "profiles.profile": ProfileObjSerializer,
}

log = logging.getLogger(__name__)


@api_view(["PUT"])
def play(request, **kwargs):

    results = []
    items_to_play = request.data.get("items")

    if not items_to_play:
        return HttpResponseBadRequest("no items requested")

    for item in items_to_play:
        obj_ct = item.get("ct")
        obj_uuid = item.get("uuid")

        log.debug(f"item requested to play: {obj_ct} {obj_uuid}")

        serializer_class = SERIALIZER_MAP.get(obj_ct)
        if not serializer_class:
            log.warning(f"no serializer defined for {obj_ct}")
            return HttpResponseBadRequest(f"no serializer defined for {obj_ct}")

        try:
            obj = apps.get_model(*obj_ct.split(".")).objects.get(uuid=obj_uuid)
        except ObjectDoesNotExist:
            raise Http404

        serializer = serializer_class(obj, context={"request": request})
        results.append(serializer.data)

    return Response({"results": results})
