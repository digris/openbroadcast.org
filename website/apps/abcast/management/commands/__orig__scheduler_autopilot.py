#-*- coding: utf-8 -*-
from optparse import make_option
import datetime

from django.core.management.base import BaseCommand, NoArgsCommand
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import translation


from abcast.util.calc import round_dt



# logging
import logging
logger = logging.getLogger(__name__)

START_OFFSET = -1 # hours to look ahead
SCHEDULE_AHEAD = 4 # hours to fill

SCHEDULER_DEFAULT_CHANNEL_ID = getattr(settings, 'SCHEDULER_DEFAULT_CHANNEL_ID', 1)
SCHEDULER_DEFAULT_USERNAME = 'root'

SCHEDULER_DEFAULT_THEME = 3

class Autopilot(object):

    def __init__(self, * args, **kwargs):

        translation.activate('en')

        from abcast.models import Channel

        self.action = kwargs.get('action')
        self.schedule_ahead = int(kwargs.get('schedule_ahead', SCHEDULE_AHEAD))
        self.channel_id = int(kwargs.get('channel_id', SCHEDULER_DEFAULT_CHANNEL_ID))
        self.channel = Channel.objects.get(pk=self.channel_id)
        self.username = kwargs.get('username', SCHEDULER_DEFAULT_USERNAME)
        self.user = User.objects.get(username=self.username)
        self.verbosity = int(kwargs.get('verbosity', 1))

        from pushy.models import setup_signals
        setup_signals()

        
        
    def add_emission(self, slot_start):

        from abcast.models import Channel, Emission
        from alibrary.models import Playlist
        
        log = logging.getLogger('abcast.autopilot.add_emission')
        log.debug('auto-adding emission, slot start: %s' % slot_start)

        # check if overlapping emission exists
        ces = Emission.objects.filter(time_start__lt=slot_start, time_end__gt=slot_start, channel=self.channel)
        print 'coliding emissions'
        print ces
        if ces.count() > 0:
            next_start = ces[0].time_end
        else:
            next_start = slot_start
            
        print 'next_start: %s' % next_start
        next_start = round_dt(next_start, 300) # round to 5 minutes
        print 'next_start rounded: %s' % next_start
            
        # check how much time is available until next emission
        fes = Emission.objects.filter(time_start__gte=next_start, channel=self.channel).order_by('time_start')
        print fes
        free_slot = 14400
        if fes.count() > 0:
            log.debug('got %s emissions scheduled in future' % fes.count())
            diff = fes[0].time_start - next_start
            free_slot = int(diff.total_seconds())


        log.debug('length of free slot is: %s seconds' % free_slot)
        log.debug('length of free slot is: %s hours' % (int(free_slot) / 60 / 60))
            
        if free_slot == 0 or free_slot < 60:
            print 'FREE SLOT IS %s. ENDS AT:' % free_slot
            print fes[0].time_end
            return fes[0].time_end
            
        """
        look for possible playlists to schedule
        """
        ps = Playlist.objects.filter(target_duration__lte=free_slot, rotation=True, status=1, type="broadcast", duration__gte=29*60*1000).order_by('?')
        
        if ps.count() > 0:
            p = ps[0]
        else:
            p = None
        
        print 'The random selection i!!'
        print p
        
        # create the scheduler entry
        if p:
            e = Emission(content_object=p, time_start=next_start, channel=self.channel, user=self.user, color=SCHEDULER_DEFAULT_THEME)
            e.save()
            # e, c = Emission.objects.get_or_create(content_object=p, time_start=next_start, channel=self.channel, user=self.user, color=SCHEDULER_DEFAULT_THEME)
            
            print 'Created emission, will run until: %s' % e.time_end
            
            return e.time_end
        

    def free_time_in_range(self, range_start, range_end):

        from abcast.models import Channel, Emission
        
        log = logging.getLogger('abcast.autopilot.free_time_in_range')
        log.debug('range_start: %s' % range_start)
        log.debug('range_end: %s' % range_end)
        

        range_seconds = int((range_end - range_start).total_seconds())
        #print 'range_seconds %s' % range_seconds
        
        emissions_total = 0
        es = Emission.objects.filter(time_end__gte=range_start, time_start__lte=range_end, channel=self.channel)
        for e in es:
            print e
            emissions_total += int(e.content_object.get_duration())
        
            
        #print 'range_seconds:   %s' % range_seconds
        #print 'emissions_total: %s' % (int(emissions_total) / 1000)
            
        free_time = range_seconds - (int(emissions_total) / 1000)
        
        return free_time
        
        
    def run(self):
        
        log = logging.getLogger('abcast.autopilot.run')
        
        log.debug('running autopilot, action: %s' % self.action)

        from abcast.models import Channel, Emission
        
        
        if self.action == 'schedule':
            
            log.debug('try to fill up the schedule')
            
            now = datetime.datetime.now()
            range_start = now.replace(minute=0, second=0, microsecond=0) + datetime.timedelta(hours=1 + START_OFFSET)
            range_end = range_start + datetime.timedelta(hours=self.schedule_ahead)
            
            log.debug('range_start: %s' % range_start)
            log.debug('range_end:   %s' % range_end)
            
            slot_start = range_start

            print
            print 'free time in range:'
            print self.free_time_in_range(range_start, range_end)


            """"""
            while self.free_time_in_range(range_start, range_end) > 120:
                slot_start = self.add_emission(slot_start)


            





class Command(NoArgsCommand):

    option_list = BaseCommand.option_list + (
        make_option('--action',
            action='store',
            dest='action',
            default=False,
            help='Action to do. (--action=schedule)'),
        make_option('--channel_id',
            action='store',
            dest='channel_id',
            default=SCHEDULER_DEFAULT_CHANNEL_ID,
            help='Specify the channel id'),
        make_option('--username',
            action='store',
            dest='username',
            default='autopilot',
            help='Specify user to assign for autopilot scheduling'),
        make_option('--schedule_ahead',
            action='store',
            dest='schedule_ahead',
            default=SCHEDULE_AHEAD,
            help='Number of hours to schedule ahead. Default 12'),
        )

    def handle_noargs(self, **options):
        ap = Autopilot(**options)
        ap.run()
