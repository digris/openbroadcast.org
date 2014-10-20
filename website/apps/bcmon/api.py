from tastypie import fields
from tastypie.authentication import *
from tastypie.authorization import *
from tastypie.resources import ModelResource, Resource, ALL_WITH_RELATIONS

from bcmon.models import *
from alibrary.api import MediaResource

class ChannelResource(ModelResource):
    
    #playout = fields.ToOneField('PlayoutResource', 'playout')
    
    class Meta:
        queryset = Channel.objects.all()
        resource_name = 'channel'
        excludes = ['updated',]
        # excludes = ['email', 'password', 'is_superuser', 'is_active', 'is_staff', 'id']
        filtering = {
            'name': ['exact', ],
        }

class PlayoutResource(ModelResource):
    
    media = fields.ForeignKey(MediaResource, 'media', null=True, full=False)
    channel = fields.ForeignKey(ChannelResource, 'channel', null=True, full=True)

    class Meta:
        queryset = Playout.objects.all()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        resource_name = 'playout'
        excludes = ['updated',]
        authentication = BasicAuthentication()
        authorization = Authorization()
        filtering = {
            'channel': ALL_WITH_RELATIONS,
            'created': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
        }
        
    """"""
    def obj_create(self, bundle, request, **kwargs):
        
        print 'create'
        
        if 'channel' in bundle.data:            
            bundle.data['channel'] = {'pk': int(bundle.data['channel'])}

        return super(PlayoutResource, self).obj_create(bundle, request, **kwargs)
    
    
    def obj_update(self, bundle, request, **kwargs):

        return super(PlayoutResource, self).obj_update(bundle, request, **kwargs)
    
    
    
    
    
    
class FPObject(object):

    def __init__(self, initial=None):
        self.__dict__['_data'] = {}

        if hasattr(initial, 'items'):
            self.__dict__['_data'] = initial

    def __getattr__(self, name):
        return self._data.get(name, None)

    def __setattr__(self, name, value):
        self.__dict__['_data'][name] = value

    def to_dict(self):
        return self._data
    
    
    
class FPResource(Resource):
    
    uuid = fields.CharField(attribute='uuid', null=True)
    user_uuid = fields.CharField(attribute='user_uuid', null=True)
    
    class Meta:
        resource_name = 'identify'
        object_class = FPObject
        allowed_methods = ['get',]
        authentication = BasicAuthentication()
        authorization = Authorization()
        
    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}

        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.uuid
        else:
            kwargs['pk'] = bundle_or_obj.uuid

        return kwargs

    def get_object_list(self, request):

        results = []
        
        q = request.GET.get('q', None)
        
        if q:
            new_obj = FPObject()
            new_obj.uuid = 'UID-ID-IIIDDD'
            results.append(new_obj)

        
        return results

    def obj_get_list(self, request=None, **kwargs):
        # Filtering disabled for brevity...
        return self.get_object_list(request)
    