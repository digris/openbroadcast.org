from alibrary.models import Release
from django.conf.urls import url
from easy_thumbnails.files import get_thumbnailer
from tastypie import fields
from tastypie.authentication import MultiAuthentication, SessionAuthentication, ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.cache import SimpleCache
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash


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
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/stats%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('stats'), name="alibrary-release_api-stats"),
        ]


    def stats(self, request, **kwargs):

        self.method_check(request, allowed=['get'])
        # self.is_authenticated(request)
        self.throttle_check(request)

        release = Release.objects.get(**self.remove_api_resource_names(kwargs))

        from statistics.utils.legacy import ObjectStatistics
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
