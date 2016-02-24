from collections import namedtuple

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
    uuid = fields.CharField(attribute='uuid')
    name = fields.CharField(attribute='name')
    ct = fields.CharField(attribute='ct')
    detail_uri = fields.CharField(attribute='detail_uri')
    tags = fields.ListField(attribute='tags')
    meta = fields.ListField(attribute='meta')
    #created = fields.IntegerField(attribute='created')

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
            #return bundle_or_obj.obj.get_api_url()
        else:
            return ''

    def get_object_list(self, request, **kwargs):

        #sqs = SearchQuerySet().load_all().auto_query(request.GET.get('q', ''))
        sqs = SearchQuerySet().filter(text__startswith=request.GET.get('q', ''))


        search_models = []

        limit_models = request.GET.get('m', None)

        if limit_models:

            print '////////////////////'
            print limit_models

            for model in limit_models.split(' '):
                search_models.append(models.get_model(*model.split('.')))

            sqs = sqs.models(*search_models)



        results = []

        for result in sqs:
            new_obj = SearchObject(obj=result.object)
            results.append(new_obj)

        return results

    def obj_get_list(self, request=None, **kwargs):
        # Filtering disabled for brevity...
        return self.get_object_list(request)

    def obj_get(self, request=None, **kwargs):
        bucket = self._bucket()
        message = bucket.get(kwargs['pk'])
        return SearchObject(initial=message.get_data())
