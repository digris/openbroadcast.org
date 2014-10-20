import json

from tastypie import fields
from tastypie.authentication import *
from tastypie.authorization import *
from tastypie.resources import ModelResource, ALL_WITH_RELATIONS
from django.template import defaultfilters as dj_filters

from exporter.models import Export, ExportItem
from alibrary.api import ReleaseResource, ArtistResource, PlaylistResource, MediaResource
from alibrary.models import Release, Artist, Playlist, Media
from tastypie.contrib.contenttypes.fields import GenericForeignKeyField


class ExportItemResource(ModelResource):
    
    export_session = fields.ForeignKey('exporter.api.ExportResource', 'export_session', null=True, full=False)
    
    co_to = {
             Release: ReleaseResource,
             Artist: ArtistResource,
             Playlist: PlaylistResource,
             Media: MediaResource,
             }
    
    content_object = GenericForeignKeyField(to=co_to, attribute='content_object', null=False, full=False)

    class Meta:
        queryset = ExportItem.objects.all()
        list_allowed_methods = ['get', 'post',]
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        resource_name = 'exportitem'
        # excludes = ['type','results_musicbrainz']
        #excludes = ['id',]
        authentication =  MultiAuthentication(SessionAuthentication(), ApiKeyAuthentication())
        authorization = Authorization()
        always_return_data = True
        filtering = {
            'import_session': ALL_WITH_RELATIONS,
            'created': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
        }
        
    

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(export_session__user=request.user)

    def obj_create(self, bundle, request, **kwargs):


        item = bundle.data['item']
        print item
        print item['item_type']
        print item['item_id']

        try:
            # sorry for this, but else relations get blanked out???
            export_session_id = json.loads(request.body)['export_session_id']
        except Exception, e:
            export_session_id = None

        if export_session_id:
            export_session, created = Export.objects.get_or_create(pk=int(export_session_id))
            bundle.data['export_session'] = export_session


        # mapping
        co = None
        if item['item_type'] == 'release':
            co = Release.objects.get(pk=int(item['item_id']))

        if item['item_type'] == 'media':
            co = Media.objects.get(pk=int(item['item_id']))

        if item['item_type'] == 'playlist':
            co = Playlist.objects.get(pk=int(item['item_id']))
            print '###########################################'
            print co




        """
        sorry for this hack. verry strange - when crating object directly, for playlist models we always get:
        'ManyRelatedManager is not Callable'
        just temporary set co to arbitary media object
        """
        bundle.data['content_object'] = Media.objects.all()[1]

        res = super(ExportItemResource, self).obj_create(bundle, request, **kwargs)

        bundle.obj.content_object = co
        bundle.obj.save()

        return res



class ExportResource(ModelResource):
    
    items = fields.ToManyField('exporter.api.ExportItemResource', 'export_items', full=False, null=True)

    class Meta:
        queryset = Export.objects.all()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete', 'patch']
        #list_allowed_methods = ['get',]
        #detail_allowed_methods = ['get',]
        resource_name = 'export'
        excludes = ['updated',]
        include_absolute_url = True
        authentication =  MultiAuthentication(SessionAuthentication(), ApiKeyAuthentication())
        authorization = Authorization()
        always_return_data = True
        limit = 100
        max_limit = 200
        filtering = {
            #'channel': ALL_WITH_RELATIONS,
            'created': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
            'status': ['exact',],
        }
        
    def obj_create(self, bundle, request=None, **kwargs):
        return super(ExportResource, self).obj_create(bundle, request, user=request.user)
        

    def dehydrate(self, bundle):
        bundle.data['download_url'] = bundle.obj.get_download_url();
        bundle.data['formatted_filesize']  = dj_filters.filesizeformat(bundle.obj.filesize)
        return bundle

    """
    def save_related(self, obj):
        return True
    """

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(user=request.user)

        

    
    
    

    