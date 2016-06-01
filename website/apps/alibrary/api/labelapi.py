from alibrary.models import Label
from django.conf.urls import url
from easy_thumbnails.files import get_thumbnailer
from tastypie.authentication import MultiAuthentication, SessionAuthentication, ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.cache import SimpleCache
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash

THUMBNAIL_OPT = dict(size=(70, 70), crop=True, bw=False, quality=80)


class LabelResource(ModelResource):
    class Meta:
        queryset = Label.objects.all()
        list_allowed_methods = ['get', ]
        detail_allowed_methods = ['get', ]
        resource_name = 'library/label'
        excludes = ['updated', ]
        include_absolute_url = True
        authentication = MultiAuthentication(SessionAuthentication(), ApiKeyAuthentication())
        authorization = Authorization()
        filtering = {
            'created': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
            'id': ['exact', 'in'],
        }
        cache = SimpleCache(timeout=120)

    def dehydrate(self, bundle):

        if (bundle.obj.main_image):
            bundle.data['main_image'] = None
            try:
                opt = THUMBNAIL_OPT
                main_image = get_thumbnailer(bundle.obj.main_image).get_thumbnail(opt)
                bundle.data['main_image'] = main_image.url
            except:
                pass

        bundle.data['release_count'] = bundle.obj.release_label.count()
        bundle.data['type_display'] = bundle.obj.get_type_display()

        bundle.data['tags'] = [tag.name for tag in bundle.obj.tags]

        return bundle

    # additional methods
    def prepend_urls(self):

        return [
            url(r"^(?P<resource_name>%s)/autocomplete%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('autocomplete'), name="alibrary-label_api-autocomplete"),
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

            if q.startswith("*"):
                q = q[1:]  # remap q
                qs = Label.objects.order_by('name').filter(name__icontains=q)
            else:
                qs = Label.objects.order_by('name').filter(name__istartswith=q)

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
        bundle.data['id'] = bundle.obj.pk
        bundle.data['ct'] = 'label'
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
