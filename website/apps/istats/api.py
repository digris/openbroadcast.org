from django.conf.urls.defaults import *
from django.contrib.sites.models import Site

from tastypie.authentication import *
from tastypie.authorization import *
from tastypie.resources import Resource
from tastypie.utils import trailing_slash

from .models import Stats



class StatsResource(Resource):
    
    base_url = Site.objects.get_current().domain

    class Meta:
        list_allowed_methods = ['get',]
        detail_allowed_methods = ['get',]
        resource_name = 'stats'
        authentication =  Authentication()
        authorization = Authorization()
        always_return_data = False


    def obj_get_list(self, request, *args, **kwargs):
        return []

    # additional methods
    def prepend_urls(self):
        
        return [
            url(r"^(?P<resource_name>%s)/server%s$" % (
                self._meta.resource_name, trailing_slash()),
                self.wrap_view('server_stats'),
                name="istats_api_server"),
        ]

    
    
    
    def server_stats(self, request, **kwargs):


        s = Stats()

        bundle = s.get_server_stats()


        self.log_throttled_access(request)
        return self.create_response(request, bundle)

    
    
    
    
    
    
    
    
    
    