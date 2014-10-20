import json

from django.conf.urls.defaults import *
from tastypie.authentication import *
from tastypie.authorization import *
from tastypie.resources import Resource, ALL_WITH_RELATIONS
from tastypie.utils import trailing_slash
from django.http import HttpResponse


class BaseResource(Resource):

    class Meta:
        #queryset = ImportFile.objects.all()
        list_allowed_methods = ['get',]
        detail_allowed_methods = ['get',]
        resource_name = 'base'
        # excludes = ['type','results_musicbrainz']
        excludes = ['type',]
        authentication = Authentication()
        authorization = Authorization()
        always_return_data = True
        filtering = {
            'import_session': ALL_WITH_RELATIONS,
            'created': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
        }
        

    def dehydrate(self, bundle):
        bundle.data['status'] = bundle.obj.get_status_display().lower();
        # offload json parsing to the backend
        # TODO: remove in js, enable here
        """
        bundle.data['import_tag'] = json.loads(bundle.data['import_tag'])
        bundle.data['results_acoustid'] = json.loads(bundle.data['results_acoustid'])
        bundle.data['results_musicbrainz'] = json.loads(bundle.data['results_musicbrainz'])
        bundle.data['results_discogs'] = json.loads(bundle.data['results_discogs'])
        bundle.data['results_tag'] = json.loads(bundle.data['results_tag'])
        """
        return bundle
    
    # additional methods
    def prepend_urls(self):
        
        return [
            url(r"^(?P<resource_name>%s)/version%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('api_version'), name="base_api_version"),
            url(r"^(?P<resource_name>%s)/register-component%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('register_component'), name="base_api_register_component"),
            url(r"^(?P<resource_name>%s)/get-stream-parameters%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_stream_parameters'), name="base_api_get_stream_parameters"),
        ]



    def api_version(self, request, **kwargs):
        
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        data = {"version":"2.4.1"}
        
        return HttpResponse(
                            json.dumps(data),
                            content_type = 'application/json; charset=utf8'
                            )
        
        bundle = self.build_bundle(obj=data, request=request)
        bundle = self.dehydrate(bundle)

        self.log_throttled_access(request)
        return self.create_response(request, bundle)

    def register_component(self, request, **kwargs):
        
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        data = {"status": True}
        
        return HttpResponse(
                            json.dumps(data),
                            content_type = 'application/json; charset=utf8'
                            )

    def get_stream_parameters(self, request, **kwargs):
        
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        data = {"stream_params":{"s1":{"enable":"true","output":"icecast","type":"ogg","bitrate":"128","host":"ubuntu","port":"8000","user":"","pass":"donthackme","admin_user":"admin","admin_pass":"donthackme","mount":"airtime_128","url":"http:\/\/airtime.sourcefabric.org","description":"Airtime Radio! Stream #1","genre":"genre","name":"Airtime!","channels":"stereo","liquidsoap_error":"OK"},"s2":{"enable":"false","output":"icecast","type":"","bitrate":"","host":"","port":"","user":"","pass":"","admin_user":"","admin_pass":"","mount":"","url":"","description":"","genre":"","name":"","channels":"stereo"},"s3":{"enable":"false","output":"icecast","type":"","bitrate":"","host":"","port":"","user":"","pass":"","admin_user":"","admin_pass":"","mount":"","url":"","description":"","genre":"","name":"","channels":"stereo"}}}
        
        return HttpResponse(
                            json.dumps(data),
                            content_type = 'application/json; charset=utf8'
                            )

        

    