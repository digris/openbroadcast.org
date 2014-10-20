import json
import datetime

from django.conf import settings
from django.conf.urls.defaults import *
from django.http import HttpResponse
from tastypie.authentication import *
from tastypie.authorization import *
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash
from tastypie.http import HttpUnauthorized
from tastypie.contrib.contenttypes.fields import GenericForeignKeyField
from actstream import action
from alibrary.models import Playlist
from abcast.models import Emission, Channel

# logging
import logging
logger = logging.getLogger(__name__)


SCHEDULER_GRID_WIDTH = getattr(settings, 'SCHEDULER_GRID_WIDTH', 830)
SCHEDULER_GRID_OFFSET = getattr(settings, 'SCHEDULER_GRID_OFFSET', 60)
SCHEDULER_PPH = getattr(settings, 'SCHEDULER_PPH', 42)
SCHEDULER_PPD = getattr(settings, 'SCHEDULER_PPD', 110) # actually should be calculated
# how long ahead should the schedule be locked
SCHEDULER_LOCK_AHEAD = getattr(settings, 'SCHEDULER_LOCK_AHEAD', -60*60) # 1 minute, to allow caching of files
SCHEDULER_NUM_DAYS = 7
# hours to offset the schedule
# 6: day starts at 6:00 and goes until 6:00
SCHEDULER_OFFSET = getattr(settings, 'SCHEDULER_OFFSET', 6)
SCHEDULER_DEFAULT_CHANNEL_ID = getattr(settings, 'SCHEDULER_DEFAULT_CHANNEL_ID', 1)

"""
scheduler specific resources, using custom hydration
"""

class PlaylistResource(ModelResource):

    class Meta:
        queryset = Playlist.objects.order_by('-created').all()
        list_allowed_methods = ['get',]
        detail_allowed_methods = ['get',]
        resource_name = 'simpleplaylist'
        #excludes = ['updated',]
        include_absolute_url = True
        
        always_return_data = True
        
        authentication =  MultiAuthentication(SessionAuthentication(), ApiKeyAuthentication())
        authorization = Authorization()
        filtering = {
        }

    def dehydrate(self, bundle):
        bundle.data['item_count'] = bundle.obj.items.count();
        return bundle



class EmissionResource(ModelResource):

    co_to = {
             Playlist: PlaylistResource,
             }
    
    content_object = GenericForeignKeyField(to=co_to, attribute='content_object', null=False, full=True)

    class Meta:
        queryset = Emission.objects.order_by('name').all()
        list_allowed_methods = ['get',]
        detail_allowed_methods = ['get', 'post', 'delete',]
        resource_name = 'abcast/emission'
        excludes = ['locked', ]
        include_absolute_url = True
        authentication =  Authentication()
        authorization = Authorization()
        filtering = {
            #'channel': ALL_WITH_RELATIONS,
            'created': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
            'channel': ['exact',],
            'time_start': ['gte', 'lte'],
            'time_end': ['gte', 'lte'],
            'updated': ['gte', 'lte'],
        }
        max_limit = 100000
        #cache = SimpleCache(timeout=120)


    def alter_list_data_to_serialize(self, request, data):
        # add current time to meta, to enable to just call api for changes
        data['meta']['time'] = datetime.datetime.now()
        return data


    def apply_filters(self, request, applicable_filters):
        base_object_list = super(EmissionResource, self).apply_filters(request, applicable_filters)

        channel_id = request.GET.get('channel_id', None)
        if channel_id:
            base_object_list = base_object_list.filter(channel_id=int(channel_id)).distinct()

        return base_object_list



    def dehydrate(self, bundle):
        
        obj = bundle.obj
        
        bundle.data['locked'] = obj.has_lock
        bundle.data['playing'] = obj.is_playing
        bundle.data['type_display'] = obj.get_type_display()
        
        bundle.data['overlap'] = False
        if obj.time_start.hour < SCHEDULER_OFFSET:
                tt = obj.time_start + datetime.timedelta(days=-1)
                bundle.data['day_id'] = tt.strftime("%Y-%m-%d")
                bundle.data['overlap'] = True
        else:
            bundle.data['day_id'] = obj.time_start.strftime("%Y-%m-%d")
        
        if obj.user:
            bundle.data['user'] = {
                                    'username': obj.user.username,
                                    'absolute_url': obj.user.get_absolute_url(),
                                    'full_name': obj.user.get_full_name()
                                   }

        if obj.content_object and obj.content_object.user:
            bundle.data['user_co'] = {
                                    'username': obj.content_object.user.username,
                                    'absolute_url': obj.content_object.user.get_absolute_url(),
                                    'full_name': obj.content_object.user.get_full_name()
                                   }

        return bundle
    
    
    

    
    # additional methods
    def prepend_urls(self):
        
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/reschedule%s$" % (
                self._meta.resource_name, trailing_slash()),
                self.wrap_view('reschedule'),
                name="scheduler_api_reschedule"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/update%s$" % (
                self._meta.resource_name, trailing_slash()),
                self.wrap_view('emission_update'),
                name="scheduler_api_emission_update"),
        ]

    def emission_update(self, request, **kwargs):

        # TODO: check for scheduler permissions
        if not request.user.is_authenticated():
            return HttpUnauthorized()


        e = Emission.objects.get(**self.remove_api_resource_names(kwargs))

        locked = request.POST.get('locked', 0)
        color = request.POST.get('color', 0)

        if int(locked) == 1:
            e.locked = True
        else:
            e.locked = False
            
        e.color = int(color)
        data = {}
        
        e.save()

        #action.send(request.user, verb='updated', target=e.content_object)
        
        return self.json_response(request, data)

    def reschedule(self, request, **kwargs):

        # TODO: check for scheduler permissions
        if not request.user.is_authenticated():
            return HttpUnauthorized()

        log = logging.getLogger('abcast.schedulerapi.reschedule')

        top = request.POST.get('top', None)
        left = request.POST.get('left', None)
        
        num_days = request.POST.get('num_days', SCHEDULER_NUM_DAYS)
        channel_id = request.POST.get('channel_id', SCHEDULER_DEFAULT_CHANNEL_ID)

        channel = Channel.objects.get(pk=int(channel_id))

        e = Emission.objects.get(**self.remove_api_resource_names(kwargs))

        data = {"version":"2.4.1"}
    
    
        pph = SCHEDULER_PPH
        # ppd = SCHEDULER_PPD
        ppd = (SCHEDULER_GRID_WIDTH - SCHEDULER_GRID_OFFSET) / int(num_days)
        
        top = float(top) / pph * 60
        #offset_min = int(15 * round(float(top)/15))
        offset_min = int(5 * round(float(top)/5))
    
        left = float(left) / ppd
        offset_d = int(round(float(left)))
    
        
        log.debug('minutes (offset): %s' % offset_min)
        log.debug('days (offset): %s' % offset_d)


        # add offsets
        time_start = datetime.datetime.combine(e.time_start.date(), datetime.time(0))
        time_start = time_start + datetime.timedelta(minutes=offset_min, days=offset_d)
        
        time_start = time_start + datetime.timedelta(hours=SCHEDULER_OFFSET)
        
        # time_end = time_start + datetime.timedelta(milliseconds=e.content_object.get_duration())
        # for duration calculation we use the 'target duration' (to avoid blocked slots)
        time_end = time_start + datetime.timedelta(seconds=e.content_object.target_duration)
    
        log.debug('time_start: %s' % time_start)
        log.debug('time_end: %s' % time_end)
    
        success = True
    
        # check if in past
        now = datetime.datetime.now()
        lock_end = now + datetime.timedelta(seconds=SCHEDULER_LOCK_AHEAD)
        if lock_end > time_start:
            data = { 'message': _('You cannot schedule things in the past!') }
            success = False
        
        # check if slot is free
        es = Emission.objects.filter(time_end__gt=time_start + datetime.timedelta(seconds=2), time_start__lt=time_end, channel=channel).exclude(pk=e.pk)
        if es.count() > 0:
            data = { 'message': _('Sorry, but the desired time does not seem to be available.') }
            success = False

        if success:
            e.time_start = time_start
            data['status'] = True

            action.send(request.user, verb='rescheduled', target=e.content_object)
        
        
        # always save to trigger push-update
        e.save()
        
        
        
        return self.json_response(request, data)




    def json_response(self, request, data):
        
        self.method_check(request, allowed=['get', 'post'])
        self.is_authenticated(request)
        self.throttle_check(request)
        self.log_throttled_access(request)
        
        return HttpResponse(json.dumps(data), content_type = 'application/json; charset=utf8')
    
    
    
    
    
    
    
    
    