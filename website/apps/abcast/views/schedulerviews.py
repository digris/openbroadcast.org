import datetime
import json
import logging

from abcast.models import Emission, Channel
from actstream import action
from alibrary.models import Playlist
from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.views.generic import DetailView, ListView

log = logging.getLogger(__name__)


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


    data = {}

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
        try:
            data['selected_playlist'] = Playlist.objects.get(pk=playlist_id)
        except Playlist.DoesNotExist as e:
            data['selected_playlist'] = None


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


    # log.debug('schedule offset: %s' % offset)
    # log.debug('schedule today: %s' % today)
    # log.debug('schedule playlist_id: %s' % playlist_id)
    
    
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

    model = Emission
    extra_context = {}

    def render_to_response(self, context):
        return super(EmissionDetailView, self).render_to_response(context, content_type="text/html")

    def get_context_data(self, **kwargs):

        context = super(EmissionDetailView, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context



"""
views for playlist / emission selection
"""
def select_playlist(request):

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


    log.debug('nex: %s' % next)
    log.debug('playlist_id: %s' % playlist_id)
    
    if next:
        return redirect(next)

    data = {
            'status': True,
            'playlist_id': playlist.id
            }

    return HttpResponse(json.dumps(data), content_type='application/json')



"""
put object to schedule
"""
def schedule_object(request):

    if not request.user.has_perm('abcast.schedule_emission'):
        log.warning('unauthorized attempt to schedule emission by: %s' % request.user)
        return { 'message': _('Sorry - you are not allowed to schedule an emission.') }


    data = json.loads(request.body)
    
    ct = data.get('ct', None)
    obj_id = data.get('obj_id', None)
    top = data.get('top', None)
    left = data.get('left', None)
    range_start = data.get('range_start', None)
    range_end = data.get('range_end', None)
    channel_id = data.get('channel_id', SCHEDULER_DEFAULT_CHANNEL_ID)
    channel = Channel.objects.get(pk=channel_id)
    color = data.get('color', 0)
    
    num_days = data.get('num_days', SCHEDULER_NUM_DAYS)
    
    log.debug('content type: %s' % ct)
    
    if ct == 'playlist':
        obj = Playlist.objects.get(pk=int(obj_id))
        log.debug('object to schedule: %s' % obj.name)


        if not (obj.broadcast_status == 1 and obj.type == 'broadcast'):
            log.warning('attempt to shedule invalid playlist. pk: %s' % obj.pk)
            return { 'message': _('Sorry - this playlist does not meet all criterias to be scheduled.') }


    pph = SCHEDULER_PPH
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
    time_end = time_start + datetime.timedelta(seconds=obj.target_duration)

    log.debug('time_start: %s' % time_start)
    log.debug('time_end: %s' % time_end)
    
    # check if in past
    now = datetime.datetime.now()
    lock_end = now + datetime.timedelta(seconds=SCHEDULER_LOCK_AHEAD)
    if lock_end > time_start:
        return { 'message': _('You cannot schedule emissions in the past.') }
    
    # check if slot is free
    # hm just allow some seconds of tolerance (in case of mini-overlaps)
    es = Emission.objects.filter(
        time_end__gt=time_start + datetime.timedelta(seconds=OVERLAP_TOLERANCE),
        time_start__lt=time_end,
        channel=channel)
    if es.count() > 0:
        message = _('The desired time slot does not seem to be available.')
        try:
            message += u'<br>Emission schedule from %s to %s' % (time_start.time(), time_end.time())
            for conflicting_emission in es:
                message += u'<br> - overlaps "%s" - from %s to %s' % (conflicting_emission.name, conflicting_emission.time_start.time(), conflicting_emission.time_end.time())

        except:
            pass
        return { 'message': message }
    
    
    # if no errors so far -> create emission and attach object
    e = Emission(content_object=obj, time_start=time_start, user=request.user, channel=channel, color=color)
    e.save()

    action.send(request.user, verb='scheduled', target=e.content_object)
    

    data = {
            'status': True,
            'obj_id': obj_id
            }

    return HttpResponse(json.dumps(data), content_type='application/json')
 

"""
copy a day to another
"""
def copy_paste_day(request):

    if not request.user.has_perm('abcast.schedule_emission'):
        log.warning('unauthorized attempt to copypast day by: %s' % request.user)
        return { 'message': _('Sorry - you are not allowed to edit emissions.') }

    data = json.loads(request.body)

    source = data.get('source', None)
    target = data.get('target', None)
    channel_id = data.get('channel_id', SCHEDULER_DEFAULT_CHANNEL_ID)
    channel = Channel.objects.get(pk=channel_id)
    
    log.debug('copy from: %s to %s' % (source, target))
    
    if channel and source and target:
        source = datetime.datetime.strptime(source, '%Y-%m-%d')
        target = datetime.datetime.strptime(target, '%Y-%m-%d')
        
        offset = (target - source)
        
        source_start = source + datetime.timedelta(hours=SCHEDULER_OFFSET)
        source_end = source_start + datetime.timedelta(hours=24)

        log.debug('source: %s to %s' % (source_start, source_end))
        log.debug('offset: %s' % offset)
        
        # get emissions
        es = Emission.objects.filter(time_start__gte=source_start, time_end__lte=source_end, channel=channel)
        for e in es:
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

    data = {
            'status': True,
            }

    return HttpResponse(json.dumps(data), content_type='application/json')


"""
delete all emissions in given day
"""
def delete_day(request):

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

    return HttpResponse(json.dumps(data), content_type='application/json')

 
