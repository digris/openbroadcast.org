from collections import namedtuple

from django.core.paginator import Paginator, InvalidPage
from django.http import Http404
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.resources import Resource, Bundle
from haystack.query import SearchQuerySet
from django.db import models

Metadata = namedtuple('Metadata', ['k', 'v'])

class SearchObject(object):

    def __init__(self, obj):

        ct = obj.__class__.__name__.lower()

        data = {
            'uuid': obj.uuid,
            'name': obj.name,
            'tags': [t.name for t in obj.tags.all()],
            'ct': 'alibrary.{}'.format(ct),
            'detail_uri': obj.get_absolute_url(),
            # 'image': obj.main_image,
        }

        meta = []

        if ct == 'media':
            meta = [
                ['Artist', obj.get_artist_display()],
                ['Duration', obj.master_duration]
            ]

        if ct == 'release':
            meta = [
                ['Label', obj.label.name if obj.label else ''],
            ]


        data['meta'] = meta


        self.__dict__['_data'] = data

    def __getattr__(self, name):
        return self._data.get(name, None)

    def to_dict(self):
        return self._data


class SearchResource(Resource):
    # Just like a Django ``Form`` or ``Model``, we're defining all the
    # fields we're going to handle with the API here.
    uuid = fields.CharField(attribute='uuid', null=True)
    name = fields.CharField(attribute='name', null=True)
    ct = fields.CharField(attribute='ct', null=True)
    detail_uri = fields.CharField(attribute='detail_uri', null=True)
    tags = fields.ListField(attribute='tags', null=True)
    meta = fields.ListField(attribute='meta', null=True)


    paginator_class = Paginator

    class Meta:
        resource_name = 'search'
        object_class = SearchObject
        authorization = Authorization()

    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}

        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.pk
        else:
            kwargs['pk'] = bundle_or_obj.pk

        return kwargs

    def get_resource_uri(self, bundle_or_obj=None, url_name='api_dispatch_list'):

        if isinstance(bundle_or_obj, Bundle):
            return ''
        else:
            return ''

    def get_object_list(self, request, **kwargs):

        #sqs = SearchQuerySet().load_all().auto_query(request.GET.get('q', ''))
        sqs = SearchQuerySet().load_all().filter(text__startswith=request.GET.get('q', ''))
        #sqs = SearchQuerySet().load_all().auto_query(request.GET.get('q', ''))


        search_models = []

        limit_models = request.GET.get('m', None)

        if limit_models:

            for model in limit_models.split(' '):
                search_models.append(models.get_model(*model.split('.')))

            sqs = sqs.models(*search_models)


        #return sqs

        paginator = Paginator(sqs, 20)

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
        # Filtering disabled for brevity...
        return self.get_object_list(request)


    def get_list(self, request, **kwargs):
        """
        Returns a serialized list of resources.

        Calls ``obj_get_list`` to provide the data, then handles that result
        set and serializes it.

        Should return a HttpResponse (200 OK).
        """
        # TODO: Uncached for now. Invalidation that works for everyone may be
        #       impossible.
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



    def __get_list(self, request, **kwargs):
        """
        Returns a serialized list of resources.

        Calls ``obj_get_list`` to provide the data, then handles that result
        set and serializes it.

        Should return a HttpResponse (200 OK).
        """

        print '*** get_list ***'

        objects = self.obj_get_list(request=request, **self.remove_api_resource_names(kwargs))
        sorted_objects = self.apply_sorting(objects, options=request.GET)

        paginator = self._meta.paginator_class(request.GET, sorted_objects, resource_uri=self.get_resource_uri(),
                                               limit=self._meta.limit, max_limit=self._meta.max_limit,
                                               collection_name=self._meta.collection_name)
        to_be_serialized = paginator.page()

        # Dehydrate the bundles in preparation for serialization.
        # bundles = [self.build_bundle(obj=obj, request=request) for obj in
        #            to_be_serialized[self._meta.collection_name]]

        bundles = []
        for result in to_be_serialized[self._meta.collection_name]:
            new_obj = SearchObject(obj=result.object)

            #bundle = self.full_dehydrate(new_obj)
            bundle = new_obj.to_dict()

            print bundle

            bundles.append(bundle)

        to_be_serialized = self.alter_list_data_to_serialize(request, to_be_serialized)

        return self.create_response(request, to_be_serialized)

