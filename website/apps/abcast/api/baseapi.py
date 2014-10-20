import datetime
import json

from django.conf.urls.defaults import *
from django.http import HttpResponse
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from tastypie import fields
from tastypie.authentication import *
from tastypie.authorization import *
from tastypie.resources import ModelResource, Resource, ALL_WITH_RELATIONS
from tastypie.utils import trailing_slash
from easy_thumbnails.files import get_thumbnailer

from abcast.models import Station, Channel, Emission
from abcast.util import scheduler
from lib.pypo_gateway import send as pypo_send


SCHEDULE_AHEAD = 60 * 60 * 6 # seconds

class StationResource(ModelResource):
    
    # label = fields.ForeignKey('alibrary.api.LabelResource', 'label', null=True, full=True, max_depth=2)

    class Meta:
        queryset = Station.objects.order_by('name').all()
        list_allowed_methods = ['get',]
        detail_allowed_methods = ['get',]
        resource_name = 'abcast/station'
        excludes = ['updated',]
        #include_absolute_url = True
        authentication =  MultiAuthentication(SessionAuthentication(), ApiKeyAuthentication(), Authentication())
        authorization = Authorization()
        filtering = {
            #'channel': ALL_WITH_RELATIONS,
            'created': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
        }
        #cache = SimpleCache(timeout=120)
        

    def dehydrate(self, bundle):
        
        if(bundle.obj.main_image):
            opt = dict(size=(70, 70), crop=True, bw=False, quality=80)
            try:
                main_image = get_thumbnailer(bundle.obj.main_image).get_thumbnail(opt)
                bundle.data['main_image'] = main_image.url
            except:
                pass

        return bundle

class ChannelResource(ModelResource):
    
    station = fields.ForeignKey('abcast.api.StationResource', 'station', null=True, full=True, max_depth=2)

    class Meta:
        queryset = Channel.objects.order_by('name').all()
        list_allowed_methods = ['get',]
        detail_allowed_methods = ['get',]
        resource_name = 'abcast/channel'
        excludes = ['on_air_id',]
        #include_absolute_url = True
        authentication =  Authentication()
        authorization = Authorization()
        filtering = {
            #'channel': ALL_WITH_RELATIONS,
            'created': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
        }
        #cache = SimpleCache(timeout=120)
        

    """ stream:
    file: "private/8acfe075/bcb7/11e2/a24c/b8f6b11a3aed/master.mp3"
    rtmp_app: "alibrary"
    rtmp_host: "rtmp://localhost:1935/"
    uri: "/content/library/tracks/tracks/8acfe075-bcb7-11e2-a24c-b8f6b11a3aed/stream_html5/base.mp3"
    uuid: "8acfe075-bcb7-11e2-a24c-b8f6b11a3aed"
    """

    def dehydrate(self, bundle):
        
        if(bundle.obj.station and bundle.obj.station.main_image):
            opt = dict(size=(70, 70), crop=True, bw=False, quality=80)
            try:
                main_image = get_thumbnailer(bundle.obj.station.main_image).get_thumbnail(opt)
                bundle.data['main_image'] = main_image.url
            except:
                bundle.data['main_image'] = None
        else:
            bundle.data['main_image'] = None


        """
        generate on-air
        """
        on_air = bundle.obj.get_on_air()

        bundle.data['on_air'] = on_air

        """
        generate stream settings
        """
        if (bundle.obj.rtmp_app and bundle.obj.rtmp_path) or bundle.obj.get_stream_url():
            stream = {
                      'file': '%s.stream' % bundle.obj.rtmp_path,
                     'rtmp_app': '%s' % bundle.obj.rtmp_app,
                     'rtmp_host': 'rtmp://%s:%s/' % (settings.RTMP_HOST, settings.RTMP_PORT),
                      #'uri': 'http://pypo:8000/obp-dev-256.mp3',
                      'uri': bundle.obj.get_stream_url(),
                      'uuid': bundle.obj.uuid,
                      }
        else:
            stream = {
                'error': _('stream data not defined')
            }

        bundle.data['stream'] = stream
        bundle.data['stream_url'] = bundle.obj.get_stream_url()
        bundle.data['images'] = []
        bundle.data['media'] = None

        return bundle
    
    # additional methods
    def prepend_urls(self):
        
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/on-air%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_now_playing'), name="playlist_api_get_now_playing"),
        ]



    def get_now_playing(self, request, **kwargs):
        
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        c = Channel.objects.get(**self.remove_api_resource_names(kwargs))

        bundle = self.build_bundle(obj=c, request=request)
        bundle = self.full_dehydrate(bundle)
        

        """
        search for current emission & map item times
        """
        now = datetime.datetime.now()
        
        es = Emission.objects.filter(time_start__lte=now, time_end__gte=now)
        print
        print 'get_now_playing:'
        print es


        # check if in cache
        cached_item = cache.get('abcast_on_air_%s' % c.pk)
        print 'ITEM FROM CACHE:'
        print cached_item

        now_playing = []
        start_next = False
        items = []
        
        
        
        if es.count() == 1:
            e = es[0]
            print e
            print 'Got scheduled emission!'
            

            e_start = e.time_start
            offset = 0
            items = e.content_object.get_items()
            for item in items:
                co = item.content_object
                item.time_start = e_start + datetime.timedelta(milliseconds=offset)
                item.time_end = e_start + datetime.timedelta(milliseconds=offset + co.get_duration() - (item.cue_in + item.cue_out + item.fade_cross))
                
                # check if playing
                if item.time_start < now and item.time_end > now:
                    item.is_playing = True
                    # map item for quick access

                    # ugly
                    if cached_item:
                        item_url = cached_item.get_api_url()
                    else:
                        item_url = item.content_object.get_api_url()

                    now_playing = {
                                   'emission': e.get_api_url(),
                                   'item': item_url,
                                   'time_start': item.time_start,
                                   'time_end': item.time_end,
                                   }
                    
                    start_next = (item.time_end - now).total_seconds()
                    
                    print (item.time_end - now).total_seconds()
                    
                else:
                    item.is_playing = False
                
                print '## item'
                print 
                print 'start:      %s' % item.time_start
                print 'end:        %s' % item.time_end
                print 'is playing: %s' % item.is_playing
                # print item.content_object
                
                """
                compose media data
                """


                
                offset += ( co.get_duration() - (item.cue_in + item.cue_out) )
                
        else:
            # no emission in timeframe
            es = Emission.objects.filter(time_start__gte=now).order_by('time_start')
            print 'Nothing playing right now... future:'
            if es.count() > 0:
                e = es[0]
                start_next = (e.time_start - now).total_seconds()
            
            
            

        bundle = {
                  'start_next': start_next,
                  'playing': now_playing,
                  }

        self.log_throttled_access(request)
        return self.create_response(request, bundle)
        

"""
api mapping for airtime / pypo

required resources are:
 - 
 
"""



class BaseResource(Resource):
    
    base_url = Site.objects.get_current().domain

    class Meta:
        #queryset = ImportFile.objects.all()
        list_allowed_methods = ['get',]
        detail_allowed_methods = ['get',]
        resource_name = 'abcast/base'
        # excludes = ['type','results_musicbrainz']
        excludes = ['type',]
        authentication =  MultiAuthentication(ApiKeyAuthentication(), SessionAuthentication(), Authentication())
        authorization = Authorization()
        always_return_data = True
        filtering = {
            'import_session': ALL_WITH_RELATIONS,
            'created': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
        }

    
    # additional methods
    def prepend_urls(self):
        
        return [
            url(r"^(?P<resource_name>%s)/version%s$" % (
                self._meta.resource_name, trailing_slash()),
                self.wrap_view('api_version'),
                name="base_api_version"),
            
            url(r"^(?P<resource_name>%s)/register-component%s$" % (
                self._meta.resource_name, trailing_slash()),
                self.wrap_view('register_component'),
                name="base_api_register_component"),
            
            url(r"^(?P<resource_name>%s)/get-stream-parameters%s$" % (
                self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_stream_parameters'),
                name="base_api_get_stream_parameters"),

            url(r"^(?P<resource_name>%s)/rabbitmq-do-push%s$" % (
                self._meta.resource_name, trailing_slash()),
                self.wrap_view('rabbitmq_do_push'),
                name="base_api_rabbitmq_do_push"),
            
            url(r"^(?P<resource_name>%s)/get-stream-settings%s$" % (
                self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_stream_settings'),
                name="base_api_get_stream_settings"),
                
            url(r"^(?P<resource_name>%s)/update-stream-settings%s$" % (
                self._meta.resource_name, trailing_slash()),
                self.wrap_view('update_stream_settings'),
                name="base_api_update_stream_settings"),
                
            url(r"^(?P<resource_name>%s)/update-liquidsoap-status%s$" % (
                self._meta.resource_name, trailing_slash()),
                self.wrap_view('update_liquidsoap_status'),
                name="base_api_update_liquidsoap_status"),
                
            url(r"^(?P<resource_name>%s)/notify-media-item-start-play%s$" % (
                self._meta.resource_name, trailing_slash()),
                self.wrap_view('notify_start_play'),
                name="base_api_notify_start_play"),
                
            url(r"^(?P<resource_name>%s)/get-bootstrap-info%s$" % (
                self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_bootstrap_info'),
                name="base_api_get_bootstrap_info"),
                
            url(r"^(?P<resource_name>%s)/recorded-shows%s$" % (
                self._meta.resource_name, trailing_slash()),
                self.wrap_view('recorded_shows'),
                name="base_api_recorded_shows"),
                
            url(r"^(?P<resource_name>%s)/get-schedule%s$" % (
                self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_schedule'),
                name="base_api_get_schedule"),
                
            url(r"^(?P<resource_name>%s)/on-air%s$" % (
                self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_now_playing'),
                name="base_api_get_now_playing'"),
        ]
        
        

    def api_version(self, request, **kwargs):

        data = {"version":"2.4.1"}
        return self.json_response(request, data)
    

    def register_component(self, request, **kwargs):

        data = {"status": True}
        return self.json_response(request, data)

    def get_stream_parameters(self, request, **kwargs):

        data = {"stream_params":{"s1":{"enable":"true","output":"icecast","type":"mp3","bitrate":"256","host":"ubuntu","port":"8000","user":"","pass":"donthackme","admin_user":"admin","admin_pass":"donthackme","mount":"airtime_128","url":"http:\/\/airtime.sourcefabric.org","description":"Airtime Radio! Stream #1","genre":"genre","name":"Airtime!","channels":"stereo","liquidsoap_error":"OK"},"s2":{"enable":"false","output":"icecast","type":"","bitrate":"","host":"","port":"","user":"","pass":"","admin_user":"","admin_pass":"","mount":"","url":"","description":"","genre":"","name":"","channels":"stereo"},"s3":{"enable":"false","output":"icecast","type":"","bitrate":"","host":"","port":"","user":"","pass":"","admin_user":"","admin_pass":"","mount":"","url":"","description":"","genre":"","name":"","channels":"stereo"}}}
        return self.json_response(request, data)

    def rabbitmq_do_push(self, request, **kwargs):

        """ airtime
        /* This action is for use by our dev scripts, that make
         * a change to the database and we want rabbitmq to send
         * out a message to pypo that a potential change has been made. */
        public function rabbitmqDoPushAction()
        {
            Logging::info("Notifying RabbitMQ to send message to pypo");

            Application_Model_RabbitMq::SendMessageToPypo("reset_liquidsoap_bootstrap", array());
            Application_Model_RabbitMq::PushSchedule();
        }
        """

        pypo_send({'event_type': 'reset_liquidsoap_bootstrap'})

        data = {}
        return self.json_response(request, data)

    def update_stream_settings(self, request, **kwargs):
        
        print '** update_stream_settings **'
        print request.POST

        data = {"stream_params":{"s1":{"enable":"true","output":"icecast","type":"ogg","bitrate":"128","host":"ubuntu","port":"8000","user":"","pass":"donthackme","admin_user":"admin","admin_pass":"donthackme","mount":"airtime_128","url":"http:\/\/airtime.sourcefabric.org","description":"Airtime Radio! Stream #1","genre":"genre","name":"Airtime!","channels":"stereo","liquidsoap_error":"OK"},"s2":{"enable":"false","output":"icecast","type":"","bitrate":"","host":"","port":"","user":"","pass":"","admin_user":"","admin_pass":"","mount":"","url":"","description":"","genre":"","name":"","channels":"stereo"},"s3":{"enable":"false","output":"icecast","type":"","bitrate":"","host":"","port":"","user":"","pass":"","admin_user":"","admin_pass":"","mount":"","url":"","description":"","genre":"","name":"","channels":"stereo"}}}
        return self.json_response(request, data)

    def get_stream_settings(self, request, **kwargs):
        
        print '** get_stream_settings **'
        print request.GET
        channel_uuid = request.GET.get('channel_id', None)

        try:
            channel = Channel.objects.get(uuid=channel_uuid)
        except Exception, e:
            print e
            channel = None
            
        settings = []
        if channel:
            from abcast.util.liquidsoap import generate_settings
            settings = generate_settings(channel)

        data = {'settings': settings}
        return self.json_response(request, data)

    def update_liquidsoap_status(self, request, **kwargs):
        
        print '** update_liquidsoap_status **'
        print request.POST
        
        data = {'status': True}
        return self.json_response(request, data)




    def notify_start_play(self, request, **kwargs):
        
        print '** notify_start_play **'
        media_uuid = request.GET.get('media_id', None)
        channel_uuid = request.GET.get('channel_id', None)

        if media_uuid and channel_uuid:
            print 'media_uuid  : %s' % media_uuid
            print 'channel_uuid: %s' % channel_uuid
            
            from alibrary.models import Media 
            
            item = Media.objects.get(uuid=media_uuid)
            try:
                channel = Channel.objects.get(uuid=channel_uuid)
            except:
                channel = None

            if channel:
                channel.on_air = item
                channel.save()

            
            #print 'item: %s' % item.name
            #print 'channel: %s' % channel.name
            
        data = {
            'status': True,
            'item': '%s' % item.name,
            'channel': '%s' % channel.name,
        }
        return self.json_response(request, data)

    def get_bootstrap_info(self, request, **kwargs):

        print '** get_bootstrap_info **'
        channel_uuid = request.GET.get('channel_id', None)

        if channel_uuid:
            channel = get_object_or_404(Channel, uuid=channel_uuid)

        data = {"switch_status":
                    {"live_dj": "off",
                     "master_dj": "off",
                     "scheduled_play": "on"
                    },
                    "station_name": u'%s' % channel.name,
                    "stream_label": u'%s' % channel.teaser,
                    "transition_fade": "00.000000"
        }
        return self.json_response(request, data)

    def recorded_shows(self, request, **kwargs):

        data = {"shows":[],"is_recording":False,"server_timezone":"America\/Los_Angeles"}
        return self.json_response(request, data)
    

    def recorded_shows(self, request, **kwargs):

        data = {"shows":[],"is_recording":False,"server_timezone":"America\/Los_Angeles"}
        return self.json_response(request, data)
    

    def get_schedule(self, request, **kwargs):

        print '** get_schedule **'
        channel_uuid = request.GET.get('channel_id', None)

        if channel_uuid:
            channel = get_object_or_404(Channel, uuid=channel_uuid)
        else:
            channel = None

        range_start = datetime.datetime.now()
        range_end = datetime.datetime.now() + datetime.timedelta(seconds=SCHEDULE_AHEAD)

        # TODO: it would be possible to implement multi-channel way here
        media = scheduler.get_schedule_for_pypo(range_start, range_end, channel=channel)
        # map
        data = {'media': media}

        return self.json_response(request, data)

    
    def get_now_playing(self, request, **kwargs):
        """
        search for current emission & map item times
        """
        now = datetime.datetime.now()
        
        es = Emission.objects.filter(time_start__lte=now, time_end__gte=now)
        print
        print 'get_now_playing:'
        print es
        
        now_playing = []
        start_next = False
        items = []
        
        
        
        if es.count() == 1:
            e = es[0]
            print e
            print 'Got scheduled emission!'
            

            e_start = e.time_start
            offset = 0
            items = e.content_object.get_items()
            for item in items:
                co = item.content_object
                item.time_start = e_start + datetime.timedelta(milliseconds=offset)
                item.time_end = e_start + datetime.timedelta(milliseconds=offset + co.get_duration() - (item.cue_in + item.cue_out + item.fade_cross))
                
                # check if playing
                if item.time_start < now and item.time_end > now:
                    item.is_playing = True
                    # map item for quick access
                    now_playing = {
                                   'emission': e.get_api_url(),
                                   'item': item.content_object.get_api_url(),
                                   'time_start': item.time_start,
                                   'time_end': item.time_end,
                                   }
                    
                    start_next = (item.time_end - now).total_seconds()
                    
                    print (item.time_end - now).total_seconds()
                    
                else:
                    item.is_playing = False
                
                print '## item'
                print 
                print 'start:      %s' % item.time_start
                print 'end:        %s' % item.time_end
                print 'is playing: %s' % item.is_playing
                # print item.content_object
                
                """
                compose media data
                """


                
                offset += ( co.get_duration() - (item.cue_in + item.cue_out) )
                
        else:
            # no emission in timeframe
            es = Emission.objects.filter(time_start__gte=now).order_by('time_start')
            print 'Nothing playing right now... future:'
            if es.count() > 0:
                e = es[0]
                start_next = (e.time_start - now).total_seconds()
            
            
            

        bundle = {
                  'start_next': start_next,
                  'playing': now_playing,
                  }

        self.log_throttled_access(request)
        return self.create_response(request, bundle)
        
        """
        data = {"now_playing": now_playing,"items": []}
        return self.json_response(request, data)
        """


    """
    response wrappers
    """
    def base_response(self, request, bundle):
        
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)
        self.log_throttled_access(request)
        
        return self.create_response(request, bundle)

    def json_response(self, request, data):
        
        self.method_check(request, allowed=['get', 'post'])
        self.is_authenticated(request)
        self.throttle_check(request)
        self.log_throttled_access(request)
        
        return HttpResponse(json.dumps(data),
                            content_type = 'application/json; charset=utf8')
    
    
    
    
    
    
    
"""
kind of hackish - function is here to hav access via api and other places
"""
    
    
    
    
    