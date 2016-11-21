from collections import namedtuple

from django.core.paginator import Paginator, InvalidPage
from django.http import Http404
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.resources import Resource, Bundle
from haystack.query import SearchQuerySet
from easy_thumbnails.files import get_thumbnailer
from django.apps import apps



THUMBNAIL_OPT = dict(size=(240, 240), crop=True, bw=False, quality=80)


Metadata = namedtuple('Metadata', ['k', 'v'])

class SearchObject(object):

    def __init__(self, obj):

        self.app = obj._meta.app_label
        self.ct = obj.__class__.__name__.lower()
        self.resource_uri = obj.get_api_url()

        main_image = None
        if hasattr(obj, 'main_image') and obj.main_image:
            main_image = get_thumbnailer(obj.main_image).get_thumbnail(THUMBNAIL_OPT)

        data = {
            'uuid': obj.uuid,
            'name': obj.name,
            'description': obj.description,
            'tags': [t.name for t in obj.tags.all()],
            'ct': '{}.{}'.format(self.app, self.ct),
            'detail_uri': obj.get_absolute_url(),
            'image': main_image.url if main_image else None,
        }

        meta = []

        # if self.ct == 'media':
        #     meta = [
        #         ['Artist', obj.get_artist_display()],
        #         ['Duration', obj.master_duration]
        #     ]
        #
        # if self.ct == 'release':
        #     meta = [
        #         ['Label', obj.label.name if obj.label else ''],
        #     ]


        data['meta'] = meta


        self.__dict__['_data'] = data

    def __getattr__(self, name):
        return self._data.get(name, None)

    def to_dict(self):
        return self._data


class SearchResource(Resource):

    uuid = fields.CharField(attribute='uuid', null=True)
    name = fields.CharField(attribute='name', null=True)
    ct = fields.CharField(attribute='ct', null=True)
    detail_uri = fields.CharField(attribute='detail_uri', null=True)
    image = fields.CharField(attribute='image', null=True)
    description = fields.CharField(attribute='description', null=True)
    tags = fields.ListField(attribute='tags', null=True)
    meta = fields.ListField(attribute='meta', null=True)

    paginator_class = Paginator

    class Meta:
        resource_name = 'search'
        object_class = SearchObject
        authorization = Authorization()
        limit = 100

    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}

        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.pk
        else:
            kwargs['pk'] = bundle_or_obj.pk

        return kwargs


    def get_resource_uri(self, bundle_or_obj=None, url_name='api_dispatch_list'):

        if isinstance(bundle_or_obj, Bundle):
            return bundle_or_obj.obj.resource_uri

        return ''


    def get_object_list(self, request, **kwargs):

        #sqs = SearchQuerySet().load_all().auto_query(request.GET.get('q', ''))
        #sqs = SearchQuerySet().load_all().filter(text__startswith=request.GET.get('q', ''))
        sqs = SearchQuerySet().filter(content__contains=request.GET.get('q', ''))
        #sqs = SearchQuerySet().load_all().auto_query(request.GET.get('q', ''))


        search_models = []

        limit_models = request.GET.get('m', None)

        if limit_models:

            for model in limit_models.split(' '):
                try:
                    search_models.append(apps.get_model(*model.split('.')))
                except LookupError as e:
                    pass

            sqs = sqs.models(*search_models)

        paginator = Paginator(sqs, 100)

        try:
            page = paginator.page(int(request.GET.get('page', 1)))
        except InvalidPage:
            raise Http404("Sorry, no results on that page.")

        results = []
        for result in page.object_list:
            new_obj = SearchObject(obj=result.object)
            results.append(new_obj)

        return results


    def obj_get_list(self, request=None, **kwargs):

        return self.get_object_list(request)


    def get_list(self, request, **kwargs):

        objects = self.obj_get_list(request=request, **self.remove_api_resource_names(kwargs))
        sorted_objects = self.apply_sorting(objects, options=request.GET)

        paginator = self._meta.paginator_class(request.GET, sorted_objects, resource_uri=self.get_resource_uri(),
                                               limit=self._meta.limit, max_limit=self._meta.max_limit,
                                               collection_name=self._meta.collection_name)
        to_be_serialized = paginator.page()

        # Dehydrate the bundles in preparation for serialization.
        bundles = [self.build_bundle(obj=obj, request=request) for obj in to_be_serialized[self._meta.collection_name]]
        to_be_serialized[self._meta.collection_name] = [self.full_dehydrate(bundle) for bundle in bundles]
        to_be_serialized = self.alter_list_data_to_serialize(request, to_be_serialized)
        return self.create_response(request, to_be_serialized)
