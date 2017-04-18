# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

from alibrary.models import Artist
from django.conf.urls import url
from django.db.models import Q
from easy_thumbnails.files import get_thumbnailer
from tastypie.authentication import MultiAuthentication, SessionAuthentication, ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash
from haystack.backends import SQ
from haystack.query import SearchQuerySet


THUMBNAIL_OPT = dict(size=(240, 240), crop=True, bw=False, quality=80)


class ArtistResource(ModelResource):
    class Meta:
        queryset = Artist.objects.all()
        list_allowed_methods = ['get', ]
        detail_allowed_methods = ['get', ]
        resource_name = 'library/artist'
        excludes = ['updated', ]
        include_absolute_url = True
        authentication = MultiAuthentication(SessionAuthentication(), ApiKeyAuthentication())
        authorization = Authorization()
        filtering = {
            'created': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
            'id': ['exact', 'in'],
        }

    def dehydrate(self, bundle):

        if (bundle.obj.main_image):
            bundle.data['main_image'] = None
            try:
                opt = THUMBNAIL_OPT
                main_image = get_thumbnailer(bundle.obj.main_image).get_thumbnail(opt)
                bundle.data['main_image'] = main_image.url
            except:
                pass

        bundle.data['media_count'] = len(bundle.obj.get_media())

        if bundle.obj.country:
            bundle.data['country_name'] = bundle.obj.country.printable_name
        else:
            bundle.data['country_name'] = None

        bundle.data['tags'] = [tag.name for tag in bundle.obj.tags]

        return bundle

    def prepend_urls(self):

        return [
            url(r"^(?P<resource_name>%s)/autocomplete%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('autocomplete'), name="alibrary-artist_api-autocomplete"),
            # for compatibility, remove later on
            url(r"^(?P<resource_name>%s)/autocomplete-name%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('autocomplete'), name="alibrary-artist_api-autocomplete"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/top-tracks%s$" % (
            self._meta.resource_name, trailing_slash()), self.wrap_view('top_tracks'),
                name="alibrary-artist_api-top_tracks"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/stats%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('stats'), name="alibrary-artist_api-stats"),
        ]

    def autocomplete(self, request, **kwargs):

        self.method_check(request, allowed=['get'])
        self.throttle_check(request)

        q = request.GET.get('q', None)
        result = []
        object_list = []
        objects = []
        object_count = 0

        qs = None

        if q and len(q) > 1:

            # haystack version
            sqs = SearchQuerySet().models(Artist).filter(SQ(content__contains=q) | SQ(content_auto=q))
            qs = Artist.objects.filter(id__in=[result.object.pk for result in sqs]).distinct()

            # ORM version
            # qs = Artist.objects.order_by('name').filter(Q(name__istartswith=q) | Q(namevariations__name__istartswith=q))

            object_list = qs.distinct()[0:50]
            object_count = qs.distinct().count()

            for result in object_list:
                bundle = self.build_bundle(obj=result, request=request)
                bundle = self.autocomplete_dehydrate(bundle, q)
                objects.append(bundle)

        data = {
            'meta': {
                'query': q,
                'total_count': object_count
            },
            'objects': objects,
        }

        self.log_throttled_access(request)
        return self.create_response(request, data)

    def autocomplete_dehydrate(self, bundle, q):

        bundle.data['name'] = bundle.obj.name
        bundle.data['type'] = bundle.obj.get_type_display()
        bundle.data['real_name'] = bundle.obj.real_name
        bundle.data['date_start'] = bundle.obj.date_start.year if bundle.obj.date_start else None
        bundle.data['date_end'] = bundle.obj.date_end.year if bundle.obj.date_end else None
        bundle.data['country'] = bundle.obj.country.iso2_code if bundle.obj.country else None
        bundle.data['id'] = bundle.obj.pk
        bundle.data['ct'] = 'artist'
        bundle.data['get_absolute_url'] = bundle.obj.get_absolute_url()
        bundle.data['resource_uri'] = bundle.obj.get_api_url()
        bundle.data['main_image'] = None
        try:
            opt = THUMBNAIL_OPT
            main_image = get_thumbnailer(bundle.obj.main_image).get_thumbnail(opt)
            bundle.data['main_image'] = main_image.url
        except:
            pass

        # namevariations
        bundle.data['namevariations'] = []
        for name in bundle.obj.namevariations.all():
            bundle.data['namevariations'].append(name.name)

        return bundle

    def stats(self, request, **kwargs):

        self.method_check(request, allowed=['get'])
        # self.is_authenticated(request)
        self.throttle_check(request)

        artist = Artist.objects.get(**self.remove_api_resource_names(kwargs))

        from statistics.util import ObjectStatistics
        ostats = ObjectStatistics(artist=artist)
        stats = ostats.generate()

        self.log_throttled_access(request)
        return self.create_response(request, stats)

    def top_tracks(self, request, **kwargs):

        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        artist = Artist.objects.get(**self.remove_api_resource_names(kwargs))
        objects = []
        from alibrary.models.mediamodels import Media
        from alibrary.api.mediaapi import MediaResource
        top_media = Media.objects.filter(artist=artist).order_by('?')[:6]

        for media in top_media:
            bundle = MediaResource().build_bundle(obj=media, request=request)
            data = MediaResource().full_dehydrate(bundle)
            objects.append(data)

        self.log_throttled_access(request)
        return self.create_response(request, objects)
