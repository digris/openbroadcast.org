import logging
import os
import re

from alibrary.models import Media
from django.core.exceptions import PermissionDenied
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    StreamingHttpResponse,
)
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.conf import settings
from django.views.generic import View

from .models import Waveform, Format

log = logging.getLogger(__name__)

WAVEFORM_TYPES = ["s", "w"]

NGINX_X_ACCEL_REDIRECT = getattr(settings, "NGINX_X_ACCEL_REDIRECT", True)

RANGE_RE = re.compile(r"bytes=(\d*)-(\d*)")


def ranged_file_response(request, path, content_type="application/octet-stream"):
    file_size = os.path.getsize(path)
    range_header = request.META.get("HTTP_RANGE")

    # No range requested: stream the complete file.
    if not range_header:
        response = StreamingHttpResponse(
            file_iterator(path),
            content_type=content_type,
        )
        response["Content-Length"] = file_size
        response["Accept-Ranges"] = "bytes"
        return response

    match = RANGE_RE.fullmatch(range_header.strip())
    if not match:
        response = HttpResponse(status=416)
        response["Content-Range"] = f"bytes */{file_size}"
        return response

    first, last = match.groups()

    # bytes=100-
    if first:
        start = int(first)
        end = int(last) if last else file_size - 1

    # bytes=-500  -> final 500 bytes
    else:
        suffix_length = int(last)
        start = max(file_size - suffix_length, 0)
        end = file_size - 1

    if start >= file_size or start > end:
        response = HttpResponse(status=416)
        response["Content-Range"] = f"bytes */{file_size}"
        return response

    end = min(end, file_size - 1)
    length = end - start + 1

    response = StreamingHttpResponse(
        file_iterator(path, offset=start, length=length),
        status=206,
        content_type=content_type,
    )
    response["Content-Length"] = length
    response["Content-Range"] = f"bytes {start}-{end}/{file_size}"
    response["Accept-Ranges"] = "bytes"

    return response


def file_iterator(path, offset=0, length=None, chunk_size=64 * 1024):
    with open(path, "rb") as f:
        f.seek(offset)

        remaining = length

        while remaining is None or remaining > 0:
            read_size = chunk_size if remaining is None else min(chunk_size, remaining)

            data = f.read(read_size)
            if not data:
                break

            yield data

            if remaining is not None:
                remaining -= len(data)


class WaveformView(View):
    """
    test with:
    http://obp-next.local:5000/media-asset/waveform/s/a9de1c5a-c1ca-4786-b5be-fdb5046ef212.png
    """

    def get(self, request, *args, **kwargs):

        media_uuid = kwargs.get("media_uuid")
        type = kwargs.get("type")
        media = get_object_or_404(Media, uuid=media_uuid)

        # request a default waveform  of the 'master'
        waveform = Waveform.objects.get_or_create_for_media(
            media=media, type=type, wait=True
        )

        # set access timestamp
        Waveform.objects.filter(pk=waveform.pk).update(accessed=timezone.now())

        try:
            with open(waveform.path, "rb") as waveform_file:
                waveform_data = waveform_file.read()
        except Exception as e:
            return HttpResponseBadRequest(f"{e}")
        return HttpResponse(waveform_data, content_type="image/png")


class FormatView(View):
    """
    test with:
    http://obp-next.local:5000/media-asset/format/10240118-cb99-40f6-92f9-e964dd3372e4/default.mp3
    http://obp-next.local:5000/media-asset/format/10240118-cb99-40f6-92f9-e964dd3372e4/lo.mp3
    """

    def get(self, request, *args, **kwargs):

        media_uuid = kwargs.get("media_uuid")
        quality = kwargs.get("quality")
        encoding = kwargs.get("encoding")
        media = get_object_or_404(Media, uuid=media_uuid)

        stream_permission = False

        # TODO: DISABLE DEFAULT PERMISSION!!!!!
        # stream_permission = True

        if request.user and request.user.has_perm("alibrary.play_media"):
            stream_permission = True

        if not stream_permission:
            log.warning(
                'unauthorized attempt by "%s" to download: %s - "%s"',
                request.user.username if request.user else "unknown",
                media.pk,
                media.name,
            )
            raise PermissionDenied

        # request a default encoded version of the 'master'
        media_format = Format.objects.get_or_create_for_media(
            media=media, quality=quality, encoding=encoding, wait=True
        )

        # set access timestamp
        Format.objects.filter(pk=media_format.pk).update(accessed=timezone.now())

        if NGINX_X_ACCEL_REDIRECT:
            x_path = f"/protected/{media_format.relative_path}"

            # TODO: improve handling of initial / range
            requested_range = self.request.META.get("HTTP_RANGE", None)
            if requested_range:
                requested_range = requested_range.split("=")[1].split("-")

                log.debug("requested range %s", requested_range)
                if requested_range and requested_range[0] == "0":
                    try:
                        from atracker.util import create_event

                        create_event(request.user, media, None, "stream")
                    except BaseException:
                        pass

                else:
                    log.debug("seek play")

            # serving through nginx
            response = HttpResponse(content_type="audio/mpeg")
            response["Content-Length"] = media_format.filesize
            response["X-Accel-Redirect"] = x_path

            return response

        # serving through django
        response = ranged_file_response(
            request,
            media_format.path,
            content_type="audio/mpeg",
        )

        # Only count initial playback, not every seek/range request.
        range_header = request.META.get("HTTP_RANGE")

        log.debug("range header: %s", range_header)

        if not range_header or range_header.startswith("bytes=0-"):
            try:
                from atracker.util import create_event

                create_event(request.user, media, None, "stream")
            except Exception:
                log.exception("Unable to create stream event")

        return response
