#-*- coding: utf-8 -*-
from optparse import make_option
import logging
import datetime
import time
from django.core.management.base import BaseCommand, NoArgsCommand
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import translation
from abcast.util.calc import round_dt

log = logging.getLogger(__name__)

SCHEDULE_AHEAD = 1 # days to fill
SCHEDULER_DEFAULT_CHANNEL_ID = getattr(settings, 'SCHEDULER_DEFAULT_CHANNEL_ID', 1)
SCHEDULER_DEFAULT_USERNAME = getattr(settings, 'SCHEDULER_DEFAULT_USERNAME', 'autopilot')
SCHEDULER_DEFAULT_THEME = 3

class Autopilot(object):

    def __init__(self, * args, **kwargs):

        translation.activate('en')

        from abcast.models import Channel

        self.action = kwargs.get('action')
        self.schedule_ahead = int(kwargs.get('schedule_ahead', SCHEDULE_AHEAD))
        self.channel_id = int(kwargs.get('channel_id', SCHEDULER_DEFAULT_CHANNEL_ID))

        user_ids = kwargs.get('user_ids', None)
        self.user_ids = None
        if user_ids:
            self.user_ids = [int(id) for id in user_ids.split(',')]

        self.channel = Channel.objects.get(pk=self.channel_id)
        self.username = kwargs.get('username', SCHEDULER_DEFAULT_USERNAME)
        self.user = User.objects.get(username=self.username)
        self.verbosity = int(kwargs.get('verbosity', 1))

        self.used_playlist_ids = []

        from pushy.models import setup_signals
        setup_signals()

        
        
    def add_emissions(self, abs_start, abs_end):

        slot_duration = (abs_end - abs_start).seconds
        slot_time_left = slot_duration
        slot_time_offset = 0





        print 'adding emissions to slot: %s to %s' % (abs_start, abs_end)
        print 'weekday: %s' % abs_start.weekday()
        print 'slot_duration: %s' % slot_duration


        from abcast.models import Emission
        from alibrary.models import Playlist

        # look for playlists that match daypart criterias

        # pl_dayparts query
        from alibrary.models import Daypart as PlaylistDaypart

        pldps = PlaylistDaypart.objects.filter(
            day=abs_start.weekday(),
            time_start__lte=abs_start.time(),
            time_end__gte=abs_end.time()
        )

        # very ugly. but no beter quick idea on how to get these bits
        if abs_start.hour == 16:
            pldps = PlaylistDaypart.objects.filter(
                day=abs_start.weekday(),
                time_start__lte=datetime.time(17, 0),
                time_end__gte=datetime.time(20, 0),
            )

        # very ugly. but no beter quick idea on how to get these bits
        if abs_start.hour >= 20:
            pldps = PlaylistDaypart.objects.filter(
                day=abs_start.weekday(),
                time_start__gte=datetime.time(20, 0),
            )

        print 'matching dayparts:'
        for pldp in pldps:
            print pldp

        if slot_duration <= 3600:
            target_durations = [3600]
        else:
            target_durations = [3600, 7200]

        qs = Playlist.objects.filter(
            type='broadcast',
            broadcast_status=1,
            dayparts__in=pldps,
            target_duration__in=target_durations
        )

        if self.user_ids:
            qs = qs.filter(user__pk__in=self.user_ids)





        # filling in slots
        while slot_time_left > 0:

            if slot_time_left <= 3600:
                qs = qs.filter(target_duration__in=[3600])
            else:
                qs = qs.filter(target_duration__in=[3600, 7200])

            #print 'excludes: %s' % self.used_playlist_ids
            qs = qs.exclude(pk__in=self.used_playlist_ids)
            print 'adding emission, have %s options' % qs.count()


            playlist = qs.order_by('?')[0]


            print '// random pick:'
            print 'slot_time_left:   %s' % slot_time_left
            print 'slot_time_offset: %s' % slot_time_offset

            print playlist
            print playlist.target_duration
            print

            emission_start = (abs_start + datetime.timedelta(seconds=slot_time_offset))

            emission = Emission(
                content_object=playlist,
                time_start=emission_start,
                channel=self.channel,
                user=self.user,
                color=SCHEDULER_DEFAULT_THEME
            )

            emission.save()




            # mark as used
            self.used_playlist_ids.append(playlist.id)
            slot_time_left -= playlist.target_duration
            # a bit redundant, i see
            slot_time_offset += playlist.target_duration


        
    def run(self):

        log.debug('autopilot with action: %s' % self.action)

        from abcast.models import Channel, Emission, Daypart, DaypartSet
        
        
        if self.action == 'schedule':

            daypartset = DaypartSet.objects.get(channel=self.channel)
            dayparts = Daypart.objects.filter(daypartset=daypartset).order_by('time_start')

            
            log.debug('...')

            now = datetime.datetime.now()
            today = now.date()
            tomorrow = (now.date() + datetime.timedelta(hours=24))

            #print 'now: %s' % now
            #print 'today: %s' % today
            #print 'tomorrow: %s' % tomorrow

            print '/// dayparts on %s ///' % self.channel

            days_to_fill = [tomorrow,]


            for day_to_fill in days_to_fill:

                for daypart in dayparts:

                    rel_time_end = daypart.time_end

                    # shift 00:00:00 to 23:59:59:...
                    if rel_time_end.hour == 0:
                        rel_time_end = rel_time_end.max

                    abs_start = datetime.datetime.combine(day_to_fill, daypart.time_start)
                    abs_end = datetime.datetime.combine(day_to_fill, rel_time_end)

                    #print 'abs_start: %s' % abs_start
                    #print 'abs_end:   %s' % abs_end
                    #print 'duration:  %s' % (abs_end - abs_start)

                    # check if anything scheduled in daypart
                    emissions_in_daypart = Emission.objects.filter(
                        # start or end inside range
                        Q(time_start__gte=abs_start, time_end__lte=abs_end, channel=self.channel)|
                        # overlapping start or end
                        Q(time_start__lt=abs_start, time_end__gt=abs_start, channel=self.channel)|
                        Q(time_start__lt=abs_end, time_end__gt=abs_end, channel=self.channel)
                    )

                    # if no emissions ins slot > run autoscheduler for slot!
                    if not emissions_in_daypart.exists():
                        #print '*** empty daypart -> handle'
                        self.add_emissions(abs_start, abs_end)




                    #print 'emissions in slot: %s' % emissions_in_daypart.count()
                    #print '  |||  '.join([p.name for p in emissions_in_daypart])
                    #print '--------------------------------------------------'
                    print












class Command(NoArgsCommand):

    option_list = BaseCommand.option_list + (
        make_option('--action',
            action='store',
            dest='action',
            default='schedule',
            help='Action to do. (--action=schedule)'),
        make_option('--channel_id',
            action='store',
            dest='channel_id',
            default=SCHEDULER_DEFAULT_CHANNEL_ID,
            help='Specify the channel id'),
        make_option('--user_ids',
            action='store',
            dest='user_ids',
            default=None,
            help='Specify the user ids to filter on'),
        make_option('--username',
            action='store',
            dest='username',
            default=SCHEDULER_DEFAULT_USERNAME,
            help='Specify user to assign for autopilot scheduling'),
        make_option('--schedule_ahead',
            action='store',
            dest='schedule_ahead',
            default=SCHEDULE_AHEAD,
            help='Number of days to schedule ahead. Default 1'),
        )

    def handle_noargs(self, **options):
        ap = Autopilot(**options)
        ap.run()
