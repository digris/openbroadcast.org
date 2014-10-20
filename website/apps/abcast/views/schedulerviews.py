from django.views.generic import DetailView, ListView
from django.shortcuts import render_to_response

from django.http import HttpResponse, Http404
from django.utils import simplejson as json
from django.conf import settings
from django.shortcuts import redirect
from django.utils.translation import ugettext as _

from django.template import RequestContext

from abcast.models import Emission, Channel
from actstream import action
from alibrary.models import Playlist

#from abcast.filters import EmissionFilter

import datetime

from jsonview.decorators import json_view

from django.db.models import Q
from lib.util import tagging_extra

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

OVERLAP_TOLERANCE = 2 # seconds

def schedule(request):
        
    log = logging.getLogger('abcast.schedulerviews.schedule')

    data = {}

    # pet all available channels
    data['channels'] = Channel.objects.filter(has_scheduler=True)


    data['list_style'] = request.GET.get('list_style', 's')
    data['days_offset'] = request.GET.get('days_offset', 0)
    data['get'] = request.GET
    
    num_days = request.GET.get('num_days', SCHEDULER_NUM_DAYS)
    num_days = int(num_days)
    if num_days < 7:
        num_days = 7
    if num_days > 14:
        num_days = 14

    data['num_days'] = num_days
    
    days = []
    today = datetime.datetime.now() 
    today = datetime.datetime(today.year, today.month, today.day)
    offset = datetime.timedelta(days=-today.weekday() + int(data['days_offset']))
    for day in range(int(num_days)):
        date = today + offset
        #date = date.strftime("%a, %d %b %Y %H:%M:%S +0000")
        days.append( date )
        offset += datetime.timedelta(days=1)
        
    
    data['today'] = today
    data['days'] = days
    
    data['pph'] = SCHEDULER_PPH
    data['ppd'] = (SCHEDULER_GRID_WIDTH - SCHEDULER_GRID_OFFSET) / int(num_days)
    data['offset'] = SCHEDULER_OFFSET
    
    # build a range-filter string for the API
    range_start = days[0] + datetime.timedelta(hours=SCHEDULER_OFFSET)
    range_end = days[-1] + datetime.timedelta(hours=SCHEDULER_OFFSET + 24)

    data['range_start'] = range_start
    data['range_end'] = range_end

    range_start_s = range_start.strftime("%Y-%m-%dT%H:%M:%S")
    range_end_s = range_end.strftime("%Y-%m-%dT%H:%M:%S")

    data['range_filter'] = '&time_start__gte=%s&time_end__lte=%s&' % (range_start_s, range_end_s)

    channel_id = request.GET.get('channel_id', SCHEDULER_DEFAULT_CHANNEL_ID)
    channel = Channel.objects.get(pk=int(channel_id))
    dayparts = channel.get_dayparts(days[0])
    data['dayparts'] = dayparts
    data['channel'] = channel


    data['station_time'] = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
        
    # look for a selected playlist in session
    playlist_id = request.session.get('scheduler_selected_playlist_id', None)
    if playlist_id:
        data['selected_playlist'] = Playlist.objects.get(pk=playlist_id)

    playlist_history = request.session.get('scheduler_selected_playlist_history', None)
    if playlist_history:
        from django.utils.safestring import mark_safe
        data['playlist_history'] = mark_safe(json.dumps(playlist_history))
        """
        history = [[playlist.get_api_url().replace("'", ''),
                                     1 if playlist.pk == playlist_id else 0] \
                                     for playlist in \
                                     Playlist.objects.filter(pk__in=playlist_history)]
        from django.utils.safestring import mark_safe

        data['playlist_history'] = mark_safe(json.dumps(history))
        """



    
    log.debug('schedule offset: %s' % offset)
    log.debug('schedule today: %s' % today)
    log.debug('schedule playlist_id: %s' % playlist_id)
    
    
    return render_to_response('abcast/schedule.html', data, context_instance=RequestContext(request))


class EmissionListView(ListView):
    
    model = Emission
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super(EmissionListView, self).get_context_data(**kwargs)
        
        self.extra_context['list_style'] = self.request.GET.get('list_style', 's')        
        self.extra_context['get'] = self.request.GET

        days = []
        today = datetime.datetime.now() 
        offset = datetime.timedelta(days=-today.weekday())
        for day in range(7):
            date = today + offset
            #date = date.strftime("%a, %d %b %Y %H:%M:%S +0000")
            days.append( date )
            offset += datetime.timedelta(days=1)
        
        self.extra_context['today'] = today
        self.extra_context['days'] = days
        
        context.update(self.extra_context)

        return context
    

    def get_queryset(self, **kwargs):

        kwargs = {}
        self.tagcloud = None
        q = self.request.GET.get('q', None)
        
        if q:
            qs = Emission.objects.filter(Q(name__istartswith=q))\
            .distinct()
        else:
            qs = Emission.objects.all()

        return qs

class EmissionDetailView(DetailView):

    # context_object_name = "emission"
    model = Emission
    extra_context = {}

    def render_to_response(self, context):
        return super(EmissionDetailView, self).render_to_response(context, mimetype="text/html")

    def get_context_data(self, **kwargs):
        
        obj = kwargs.get('object', None)
        context = super(EmissionDetailView, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context



"""
views for playlist / emission selection
"""
#@json_view
def select_playlist(request):
    
    log = logging.getLogger('abcast.schedulerviews.select_playlist')
    
    playlist_id = request.GET.get('playlist_id', None) 
    next = request.GET.get('next', None)

    if not playlist_id:
        request.session['scheduler_selected_playlist_id'] = None

    try:
        playlist = Playlist.objects.get(pk=playlist_id)
    except Playlist.DoesNotExist:
        log.warning('playlist does not exists. (id: %s)' % playlist_id)
        raise Http404   
    
    request.session['scheduler_selected_playlist_id'] = playlist.pk
    # try to build history
    history = request.session.get('scheduler_selected_playlist_history', [])
    if not playlist.pk in history:
        history.append(playlist.pk)
    request.session['scheduler_selected_playlist_history'] = history


    print 'HISTORY:'
    print history
    print '//////////////////////////////'


    log.debug('nex: %s' % next)
    log.debug('playlist_id: %s' % playlist_id)
    
    if next:
        return redirect(next)

    data = {
            'status': True,
            'playlist_id': playlist.id
            }
    #return data
    data = json.dumps(data)
    return HttpResponse(data, mimetype='application/json')



"""
put object to schedule
"""
@json_view
def schedule_object(request):
    
    log = logging.getLogger('abcast.schedulerviews.schedule_object')

    if not request.user.has_perm('abcast.schedule_emission'):
        log.warning('unauthorized attempt to schedule emission by: %s' % request.user)
        return { 'message': _('Sorry - you are not allowed to schedule an emission.') }
    
    ct = request.POST.get('ct', None) 
    obj_id = request.POST.get('obj_id', None)
    top = request.POST.get('top', None)
    left = request.POST.get('left', None)
    range_start = request.POST.get('range_start', None)
    range_end = request.POST.get('range_end', None)
    channel_id = request.POST.get('channel_id', SCHEDULER_DEFAULT_CHANNEL_ID)
    channel = Channel.objects.get(pk=channel_id)
    color = request.POST.get('color', 0)
    
    num_days = request.POST.get('num_days', SCHEDULER_NUM_DAYS)
    
    log.debug('content type: %s' % ct)
    
    if ct == 'playlist':
        obj = Playlist.objects.get(pk=int(obj_id))
        log.debug('object to schedule: %s' % obj.name)


        if not (obj.broadcast_status == 1 and obj.type == 'broadcast'):
            log.warning('attempt to shedule invalid playlist. pk: %s' % obj.pk)
            return { 'message': _('Sorry - this playlist does not meet all criterias to be scheduled.') }

    
    
    pph = SCHEDULER_PPH
    # ppd = SCHEDULER_PPD
    ppd = (SCHEDULER_GRID_WIDTH - SCHEDULER_GRID_OFFSET) / int(num_days)
    
    
    top = float(top) / pph * 60
    offset_min = int(15 * round(float(top)/15))
    
    left = float(left) / ppd
    offset_d = int(round(float(left)))
    
        
    log.debug('minutes (offset): %s' % offset_min)
    log.debug('days (offset): %s' % offset_d)
    
    # calculate actual date/time for position
    schedule_start = datetime.datetime.strptime('%s 00:00' % range_start, '%Y-%m-%d %H:%M')
    # add offsets
    time_start = schedule_start + datetime.timedelta(minutes=offset_min)
    time_start = time_start + datetime.timedelta(days=offset_d)
    
    time_start = time_start + datetime.timedelta(hours=SCHEDULER_OFFSET)
    
    # time_end = time_start + datetime.timedelta(milliseconds=obj.get_duration())
    # for duration calculation we use the 'target duration' (to avoid blocked slots)
    time_end = time_start + datetime.timedelta(seconds=(obj.target_duration))

    log.debug('time_start: %s' % time_start)
    log.debug('time_end: %s' % time_end)
    
    # check if in past
    now = datetime.datetime.now()
    lock_end = now + datetime.timedelta(seconds=SCHEDULER_LOCK_AHEAD)
    if lock_end > time_start:
        return { 'message': _('You cannot schedule things in the past!') }
    
    # check if slot is free
    # hm just allow some seconds of tolerance (in case of mini-overlaps)
    es = Emission.objects.filter(time_end__gt=time_start + datetime.timedelta(seconds=OVERLAP_TOLERANCE), time_start__lt=time_end + datetime.timedelta(seconds=OVERLAP_TOLERANCE), channel=channel)
    if es.count() > 0:
        for em in es:
            print 'Blocking emission: %s' % em.id
            print em.time_start
            print em.time_end
        return { 'message': _('Sorry, but the desired time does not seem to be available.') }
    
    
    # if no errors so far -> create emission and attach object
    e = Emission(content_object=obj, time_start=time_start, user=request.user, channel=channel, color=color)
    e.save()

    action.send(request.user, verb='scheduled', target=e.content_object)
    
    
    
    data = {
            'status': True,
            'obj_id': obj_id
            }
    
    return data
    #data = json.dumps(data)
    #return HttpResponse(data, mimetype='application/json')
 

"""
copy a day to another
"""
@json_view
def copy_paste_day(request):
    
    log = logging.getLogger('abcast.schedulerviews.copy_day')

    if not request.user.has_perm('abcast.schedule_emission'):
        log.warning('unauthorized attempt to copypast day by: %s' % request.user)
        return { 'message': _('Sorry - you are not allowed to edit emissions.') }
    
    source = request.POST.get('source', None) 
    target = request.POST.get('target', None)
    channel_id = request.POST.get('channel_id', SCHEDULER_DEFAULT_CHANNEL_ID)
    channel = Channel.objects.get(pk=channel_id)
    
    log.debug('copy from: %s to %s' % (source, target))
    
    if channel and source and target:
        source = datetime.datetime.strptime(source, '%Y-%m-%d')
        target = datetime.datetime.strptime(target, '%Y-%m-%d')
        
        offset = (target - source)
        
        source_start = source + datetime.timedelta(hours=SCHEDULER_OFFSET)
        source_end = source_start + datetime.timedelta(hours=24)

        log.debug('source: %s to %s' % (source_start, source_end))
        log.debug('offset: %s' % (offset))
        
        # get emissions
        es = Emission.objects.filter(time_start__gte=source_start, time_end__lte=source_end, channel=channel)
        for e in es:
            print e
            # check if slot is available
            slot_free = True

            # blocking before
            bloking_emissions = Emission.objects.filter(time_start__lte=e.time_start + offset, time_end__gte=e.time_start + offset + datetime.timedelta(seconds=OVERLAP_TOLERANCE), channel=channel)
            if bloking_emissions.count() > 0:
                slot_free = False

            # blocking after
            bloking_emissions = Emission.objects.filter(time_start__lte=e.time_end + offset - datetime.timedelta(seconds=OVERLAP_TOLERANCE), time_end__gte=e.time_end + offset, channel=channel)
            if bloking_emissions.count() > 0:
                slot_free = False

            if slot_free:
                e.pk = None
                e.uuid = None
                e.locked = False
                e.time_start = e.time_start + offset
                e.save()

                # action.send(request.user, verb='scheduled', target=e)

            else:
                print 'slot not free'

    
    now = datetime.datetime.now()

    
    data = {
            'status': True,
            }
    
    return data


"""
delete all emissions in given day
"""
@json_view
def delete_day(request):

    log = logging.getLogger('abcast.schedulerviews.delete_day')

    if not request.user.has_perm('abcast.schedule_emission'):
        log.warning('unauthorized attempt to delete day by: %s' % request.user)
        return { 'message': _('Sorry - you are not allowed to delete emissions.') }

    date = request.POST.get('date', None)
    channel_id = request.POST.get('channel_id', SCHEDULER_DEFAULT_CHANNEL_ID)
    channel = Channel.objects.get(pk=channel_id)

    log.debug('delete day %s on %s' % (date, channel.name))

    if channel and date:
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
        now = datetime.datetime.now()

        time_start = date + datetime.timedelta(hours=SCHEDULER_OFFSET)

        if time_start < now:
            time_start = now

        time_end = time_start + datetime.timedelta(hours=24)
        log.debug('range: %s to %s' % (time_start, time_end))

        # get emissions
        es = Emission.objects.filter(time_start__gte=time_start, time_end__lte=time_end, channel=channel)
        emission_count = es.count()

        for e in es:
            e.delete()

    data = {
            'status': True,
            'deleted': emission_count
            }

    return data

 
