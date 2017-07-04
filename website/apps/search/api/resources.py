from collections import namedtuple

from haystack.inputs import AutoQuery, Exact, Clean
from tastypie.paginator import Paginator
from django.http import Http404
from django.template.defaultfilters import truncatechars
from django.template.loader import get_template
from django.db.models import Q
from tastypie import fields
from django.utils.translation import ugettext as _
from tastypie.authorization import Authorization
from tastypie.resources import Resource, Bundle
from haystack.query import SearchQuerySet, EmptySearchQuerySet, SQ
from easy_thumbnails.files import get_thumbnailer
from django.apps import apps

THUMBNAIL_OPT = dict(size=(197, 197), crop=True, upscale=True)




class ResultObject(object):

    def __init__(self, result):

        obj = result.object

        self.ct = '{}.{}'.format(obj._meta.app_label, obj.__class__.__name__.lower())
        self.ct_display = '{}'.format(obj._meta.verbose_name.title())
        self.resource_uri = obj.get_api_url()
        self.obj = obj


        main_image = None
        if hasattr(obj, 'main_image') and obj.main_image:
            try:
                main_image = get_thumbnailer(obj.main_image).get_thumbnail(THUMBNAIL_OPT)
            except:
                pass

        data = {
            'uuid': obj.uuid,
            'id': obj.id,
            'name': obj.name,
            'ct': '',
            'ct_display': '',
            'representation': self.representation,
            'tags': [t.name for t in obj.tags.all()],
            'detail_uri': obj.get_absolute_url(),
            'edit_uri': obj.get_edit_url(),
            'image': main_image.url if main_image else None,
            'text': result.text,
            #'name_auto': result.name_auto,
        }

        meta = []

        data['meta'] = meta

        self.__dict__['_data'] = data

    def __getattr__(self, name):
        return self._data.get(name, None)

    def to_dict(self):
        return self._data

    @property
    def representation(self):
        """html formatted human readable representation for object"""
        tpl = get_template('search/representation/{}.html'.format(self.ct.replace('.', '/')))
        return tpl.render(context={'object': self.obj})




class GlobalSearchResource(Resource):

    uuid = fields.CharField(attribute='uuid', null=True)
    id = fields.IntegerField(attribute='id', null=True)
    name = fields.CharField(attribute='name', null=True)
    representation = fields.CharField(attribute='representation', null=True)
    text = fields.CharField(attribute='text', null=True)
    #name_auto = fields.CharField(attribute='name_auto', null=True)
    image = fields.CharField(attribute='image', null=True)
    detail_uri = fields.CharField(attribute='detail_uri', null=True)
    edit_uri = fields.CharField(attribute='edit_uri', null=True)
    tags = fields.ListField(attribute='tags', null=True)
    ct = fields.CharField(attribute='ct', null=True)
    ct_display = fields.CharField(attribute='ct_display', null=True)

    paginator_class = Paginator

    class Meta:
        resource_name = 'search'
        authorization = Authorization()
        paginator_class = Paginator
        limit = 5

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

        q = kwargs.get('query', '')

        # sqs = SearchQuerySet().filter(SQ(content__contains=q) | SQ(name=q))
        # sqs = SearchQuerySet().filter(SQ(content__contains=q) | SQ(content_auto=q))
        #sqs = SearchQuerySet().filter(SQ(content=AutoQuery(q)) | SQ(name=AutoQuery(q)))
        #sqs = SearchQuerySet().filter(content=AutoQuery(q))
        sqs = SearchQuerySet().filter(text_auto=AutoQuery(q))


        search_models = []
        limit_models = request.GET.get('ct', None)
        if limit_models:
            for model in limit_models.split(':'):
                try:
                    search_models.append(apps.get_model(*model.split('.')))
                except LookupError as e:
                    pass

            sqs = sqs.models(*search_models)


        # TODO: nasty hack here. filter out 'basket' playlists that do not belong to the authenticated user
        if request.user.is_authenticated():
            sqs = sqs.exclude(Q(type='basket') | ~Q(user_pk=request.user.pk))
        else:
            sqs = sqs.exclude(type='basket')


        sqs = sqs.highlight().load_all()

        return sqs


    def obj_get_list(self, request=None, **kwargs):

        return self.get_object_list(request, **kwargs)


    def get_list(self, request, **kwargs):

        query = request.GET.get('q', None)

        results = self.obj_get_list(request, **{'query': query})
        if not results:
            results = EmptySearchQuerySet()

        paginator = Paginator(request.GET, results, resource_uri='/api/v1/search/', max_limit=10)

        bundles = []
        for result in paginator.page()['objects']:

            result_obj = ResultObject(result)

            bundle = self.build_bundle(
                obj=result_obj,
                request=request
            )
            bundles.append(self.full_dehydrate(bundle))

        object_list = {
            'meta': paginator.page()['meta'],
            'objects': bundles
        }
        object_list['meta']['search_query'] = query

        return self.create_response(request, object_list)
