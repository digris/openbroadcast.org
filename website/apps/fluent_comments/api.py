from tastypie import fields
from tastypie.authentication import *
from tastypie.authorization import *
from tastypie.resources import ModelResource
from django.contrib.comments.models import Comment
from django.contrib.sites.models import Site

from tastypie.contrib.contenttypes.fields import GenericForeignKeyField
from alibrary.models import Release
from alibrary.api import ReleaseResource
from abcast.models import Channel
from abcast.api import ChannelResource


"""
class ReleaseResource(ModelResource):
    class Meta:
        queryset = Release.objects.all()
"""

class SiteResource(ModelResource):
    class Meta:
        queryset = Site.objects.all()
     
class CommentResource(ModelResource):
    
    site = fields.ForeignKey('fluent_comments.api.SiteResource', 'site', null=False, full=False)

    
    
    co_to = {
             Release: ReleaseResource,
             Channel: ChannelResource,
             }
    
    content_object = GenericForeignKeyField(to=co_to, attribute='content_object', null=False, full=False)
    """
    curl --dump-header - -H "Content-Type: application/json" -X POST --data '{"comment":"sdfsdfsdf", "content_object": "/de/api/v1/library/release/1963/"}' http://localhost:8080/api/v1/comment/
    """
    
    class Meta:
        queryset = Comment.objects.all()
        list_allowed_methods = ['get','put','post']
        detail_allowed_methods = ['get',]
        resource_name = 'comment'
        excludes = ['ip_address', 'user_email', 'user_url', 'object_pk']
        #include_absolute_url = True
        authentication =  MultiAuthentication(ApiKeyAuthentication(), Authentication())
        authorization = Authorization()
        filtering = {
            #'channel': ALL_WITH_RELATIONS,
            'created': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
        }
        #cache = SimpleCache(timeout=120)
        
    def obj_create(self, bundle, request, **kwargs):
        
                 
        bundle.data['site'] = Site.objects.all()[0]
        
        
        print request.user
        
        bundle.data['user'] = request.user
        
        print Site.objects.all()[0]
        
        self.save_related(bundle)
        
        print bundle.data
        
        #print request
        

        
        
        
        bundle = super(CommentResource, self).obj_create(bundle, request)
  
        print "OBJ"
        print request.user
        print 'E OBJ'      
        
        
        from django.contrib.comments import signals
        
        """"""
        signals.comment_was_posted.send(
            sender  = bundle.obj.__class__,
            comment = bundle.obj,
            request = request,
        )
        
        
        
        return bundle
        
        # return super(CommentResource, self).obj_create(bundle, request, **kwargs)


    """
    def dehydrate(self, bundle):
        
        bundle.data['comment'] = 'session'
        return bundle
    """


    