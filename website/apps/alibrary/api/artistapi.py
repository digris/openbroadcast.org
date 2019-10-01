# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

from alibrary.models import Artist
from django.conf.urls import url
from django.db.models import Q
from easy_thumbnails.files import get_thumbnailer
from tastypie.authentication import (
    MultiAuthentication,
    SessionAuthentication,
    ApiKeyAuthentication,
)
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash

THUMBNAIL_OPT = dict(size=(240, 240), crop=True, bw=False, quality=80)


class ArtistResource(ModelResource):
    class Meta:
        queryset = Artist.objects.all()
        list_allowed_methods = ["get"]
        detail_allowed_methods = ["get"]
        resource_name = "library/artist"
        excludes = ["updated"]
        include_absolute_url = True
        authentication = MultiAuthentication(
            SessionAuthentication(), ApiKeyAuthentication()
        )
        authorization = Authorization()
        filtering = {
            "created": ["exact", "range", "gt", "gte", "lt", "lte"],
            "id": ["exact", "in"],
        }

    def dehydrate(self, bundle):

        if bundle.obj.main_image:
            bundle.data["main_image"] = None
            try:
                opt = THUMBNAIL_OPT
                main_image = get_thumbnailer(bundle.obj.main_image).get_thumbnail(opt)
                bundle.data["main_image"] = main_image.url
            except:
                pass

        bundle.data["media_count"] = len(bundle.obj.get_media())

        if bundle.obj.country:
            bundle.data["country_name"] = bundle.obj.country.printable_name
        else:
            bundle.data["country_name"] = None

        bundle.data["tags"] = [tag.name for tag in bundle.obj.tags]

        return bundle

    def prepend_urls(self):

        return [
            url(
                r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/stats%s$"
                % (self._meta.resource_name, trailing_slash()),
                self.wrap_view("stats"),
                name="alibrary-artist_api-stats",
            )
        ]

    def stats(self, request, **kwargs):

        self.method_check(request, allowed=["get"])
        # self.is_authenticated(request)
        self.throttle_check(request)

        artist = Artist.objects.get(**self.remove_api_resource_names(kwargs))

        from statistics.utils.legacy import ObjectStatistics

        ostats = ObjectStatistics(artist=artist)
        stats = ostats.generate()

        self.log_throttled_access(request)
        return self.create_response(request, stats)
