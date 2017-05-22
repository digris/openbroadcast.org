from alibrary.models import Release, Media
from django.conf.urls import url
from easy_thumbnails.files import get_thumbnailer
from tastypie import fields
from tastypie.authentication import MultiAuthentication, SessionAuthentication, ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.cache import SimpleCache
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash
from django.db.models import Q
from haystack.backends import SQ
from haystack.query import SearchQuerySet
from haystack.inputs import AutoQuery

THUMBNAIL_OPT = dict(size=(240, 240), crop=True, bw=False, quality=80)


class ReleaseResource(ModelResource):
    # media = fields.ToManyField('alibrary.api.MediaResource', 'media_release', null=True, full=True, max_depth=3)
    media = fields.ToManyField('alibrary.api.MediaResource', 'media_release', null=True, full=True, max_depth=2)

    label = fields.ForeignKey('alibrary.api.LabelResource', 'label', null=True, full=True, max_depth=2)

    class Meta:
        queryset = Release.objects.order_by('-created').all()
        list_allowed_methods = ['get', ]
        detail_allowed_methods = ['get', ]
        resource_name = 'library/release'
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

        bundle.data['artist'] = bundle.obj.get_artists()

        if bundle.obj.release_country:
            bundle.data['country'] = bundle.obj.release_country.printable_name
            bundle.data['country_code'] = bundle.obj.release_country.iso2_code
        else:
            bundle.data['country'] = None
            bundle.data['country_code'] = None

        bundle.data['tags'] = [tag.name for tag in bundle.obj.tags]

        return bundle

    def prepend_urls(self):

        return [
            url(r"^(?P<resource_name>%s)/autocomplete%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('autocomplete'), name="alibrary-release_api-autocomplete"),
            url(r"^(?P<resource_name>%s)/autocomplete-name%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('autocomplete_name'), name="alibrary-release_api-autocomplete_name"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/stats%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('stats'), name="alibrary-release_api-stats"),
        ]

    def autocomplete(self, request, **kwargs):

        self.method_check(request, allowed=['get'])
        # self.is_authenticated(request)
        self.throttle_check(request)

        q = request.GET.get('q', None)
        result = []
        object_list = []
        qs = None
        if q and len(q) > 2:

            # haystack version
            #sqs = SearchQuerySet().models(Release).filter(SQ(content__contains=q) | SQ(content_auto=q))
            sqs = SearchQuerySet().models(Release).filter(content=AutoQuery(q))
            qs = Release.objects.filter(id__in=[result.object.pk for result in sqs]).distinct()

            # ORM version
            # qs = Release.objects.filter(name__icontains=q)

        if qs:
            object_list = qs.distinct()[0:20]

        objects = []
        for result in object_list:
            bundle = self.build_bundle(obj=result, request=request)
            bundle = self.autocomplete_dehydrate(bundle, q)
            objects.append(bundle)

        if qs:
            meta = {
                'query': q,
                'total_count': qs.distinct().count()
            }

            data = {
                'meta': meta,
                'objects': objects,
            }
        else:
            meta = {
                'query': q,
                'total_count': 0
            }

            data = {
                'meta': meta,
                'objects': {},
            }

        self.log_throttled_access(request)
        return self.create_response(request, data)

    def autocomplete_dehydrate(self, bundle, q):
        bundle.data['name'] = bundle.obj.name
        bundle.data['id'] = bundle.obj.pk
        bundle.data['ct'] = 'release'
        bundle.data['releasedate'] = bundle.obj.releasedate
        bundle.data['artist'] = bundle.obj.get_artists()
        bundle.data['artist_display'] = bundle.obj.get_artist_display()
        bundle.data['media_count'] = bundle.obj.media_release.count()
        bundle.data['get_absolute_url'] = bundle.obj.get_absolute_url()
        bundle.data['resource_uri'] = bundle.obj.get_api_url()
        bundle.data['main_image'] = None
        try:
            opt = THUMBNAIL_OPT
            main_image = get_thumbnailer(bundle.obj.main_image).get_thumbnail(opt)
            bundle.data['main_image'] = main_image.url
        except:
            pass

        media_list = []
        # msqs = SearchQuerySet().models(Media).filter(SQ(content__contains=q) | SQ(content_auto=q))
        # for media in bundle.obj.media_release.filter(id__in=[result.object.pk for result in msqs]).distinct():
        #    media_list.append({'name': media.name, 'artist': media.artist.name, 'get_absolute_url': media.get_absolute_url()})

        bundle.data['media'] = media_list
        return bundle

    def autocomplete_name(self, request, **kwargs):

        self.method_check(request, allowed=['get'])
        # self.is_authenticated(request)
        self.throttle_check(request)

        q = request.GET.get('q', None)
        result = []
        object_list = []
        qs = None
        if q and len(q) > 1:
            qs = Release.objects.order_by('name').filter(name__istartswith=q)

        if qs:
            object_list = qs.distinct()[0:50]

        objects = []
        for result in object_list:
            bundle = self.build_bundle(obj=result, request=request)
            bundle = self.autocomplete_name_dehydrate(bundle, q)
            objects.append(bundle)

        if qs:
            meta = {
                'query': q,
                'total_count': qs.distinct().count()
            }

            data = {
                'meta': meta,
                'objects': objects,
            }
        else:
            meta = {
                'query': q,
                'total_count': 0
            }

            data = {
                'meta': meta,
                'objects': {},
            }

        self.log_throttled_access(request)
        return self.create_response(request, data)

    def autocomplete_name_dehydrate(self, bundle, q):
        bundle.data['name'] = bundle.obj.name
        bundle.data['id'] = bundle.obj.pk
        bundle.data['ct'] = 'release'
        bundle.data['releasedate'] = bundle.obj.releasedate
        bundle.data['artist'] = bundle.obj.get_artists()
        bundle.data['media_count'] = bundle.obj.media_release.count()
        bundle.data['get_absolute_url'] = bundle.obj.get_absolute_url()
        bundle.data['resource_uri'] = bundle.obj.get_api_url()
        bundle.data['main_image'] = None
        try:
            opt = THUMBNAIL_OPT
            main_image = get_thumbnailer(bundle.obj.main_image).get_thumbnail(opt)
            bundle.data['main_image'] = main_image.url
        except:
            pass

        return bundle

    def stats(self, request, **kwargs):

        self.method_check(request, allowed=['get'])
        # self.is_authenticated(request)
        self.throttle_check(request)

        release = Release.objects.get(**self.remove_api_resource_names(kwargs))

        from statistics.util import ObjectStatistics
        ostats = ObjectStatistics(release=release)
        stats = ostats.generate()

        self.log_throttled_access(request)
        return self.create_response(request, stats)


class SimpleReleaseResource(ModelResource):
    media = fields.ToManyField('alibrary.api.MediaResource', 'media_release', null=True, full=True, max_depth=2)

    class Meta:
        queryset = Release.objects.order_by('-created').all()
        list_allowed_methods = ['get', ]
        detail_allowed_methods = ['get', ]
        resource_name = 'library/simplerelease'
        excludes = ['updated', ]
        include_absolute_url = True
        authentication = MultiAuthentication(SessionAuthentication(), ApiKeyAuthentication())
        authorization = Authorization()
        filtering = {
            'created': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
            'id': ['exact', 'in'],
        }
        cache = SimpleCache(timeout=600)

    def dehydrate(self, bundle):
        return bundle
