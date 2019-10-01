# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging

from alibrary.models import Media
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.conf import settings
from django.views.generic import View

from .models import Waveform, Format

log = logging.getLogger(__name__)

WAVEFORM_TYPES = ["s", "w"]

NGINX_X_ACCEL_REDIRECT = getattr(settings, "NGINX_X_ACCEL_REDIRECT", True)


class WaveformView(View):
    """
    test with:
    http://local.openbroadcast.org:8080/media-asset/waveform/s/a9de1c5a-c1ca-4786-b5be-fdb5046ef212.png
    """

    def get(self, request, *args, **kwargs):

        media_uuid = kwargs.get("media_uuid", None)
        type = kwargs.get("type", None)
        media = get_object_or_404(Media, uuid=media_uuid)

        # request a default waveform  of the 'master'
        waveform = Waveform.objects.get_or_create_for_media(
            media=media, type=type, wait=True
        )

        # set access timestamp
        Waveform.objects.filter(pk=waveform.pk).update(accessed=timezone.now())

        try:
            waveform_data = open(waveform.path, "rb").read()
        except Exception as e:
            return HttpResponseBadRequest("{}".format(e))
        return HttpResponse(waveform_data, content_type="image/png")


class FormatView(View):
    """
    test with:
    http://local.openbroadcast.org:8080/media-asset/format/10240118-cb99-40f6-92f9-e964dd3372e4/default.mp3
    http://local.openbroadcast.org:8080/media-asset/format/10240118-cb99-40f6-92f9-e964dd3372e4/lo.mp3
    """

    def get(self, request, *args, **kwargs):

        media_uuid = kwargs.get("media_uuid", None)
        quality = kwargs.get("quality", None)
        encoding = kwargs.get("encoding", None)
        media = get_object_or_404(Media, uuid=media_uuid)

        stream_permission = False

        # TODO: DISABLE DEFAULT PERMISSION!!!!!
        # stream_permission = True

        if request.user and request.user.has_perm("alibrary.play_media"):
            stream_permission = True

        if not stream_permission:
            log.warning(
                'unauthorized attempt by "%s" to download: %s - "%s"'
                % (
                    request.user.username if request.user else "unknown",
                    media.pk,
                    media.name,
                )
            )
            raise PermissionDenied

        # request a default encoded version of the 'master'
        format = Format.objects.get_or_create_for_media(
            media=media, quality=quality, encoding=encoding, wait=True
        )

        # set access timestamp
        Format.objects.filter(pk=format.pk).update(accessed=timezone.now())

        if NGINX_X_ACCEL_REDIRECT:

            x_path = "/protected/{}".format(format.relative_path)

            # TODO: improve handling of initial / range
            requested_range = self.request.META.get("HTTP_RANGE", None)
            if requested_range:
                requested_range = requested_range.split("=")[1].split("-")

                log.debug(u"requested range %s" % (requested_range))
                if requested_range and requested_range[0] == "0":
                    try:
                        from atracker.util import create_event

                        create_event(request.user, media, None, "stream")
                    except:
                        pass

                else:
                    log.debug(u"seek play")

            # serving through nginx
            response = HttpResponse(content_type="audio/mpeg")
            response["Content-Length"] = format.filesize
            response["X-Accel-Redirect"] = x_path
            return response

        else:
            # # original part - serving through django
            data = open(format.path, "rb").read()
            response = HttpResponse(data, content_type="audio/mpeg")
            response["Content-Length"] = format.filesize

            try:
                from atracker.util import create_event

                create_event(request.user, media, None, "stream")
            except:
                pass

            return response
