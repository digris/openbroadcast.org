#-*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
import logging
import time
from django.db.models import Count, Sum, Q, Max, Min
from django.contrib.auth.models import User
from random import shuffle
from abcast.models import Channel, Emission
from abcast.models import Daypart as BroadcastDaypart
from abcast.models import DaypartSet as BroadcastDaypartSet
from alibrary.models import Playlist
from alibrary.models import Daypart as PlaylistDaypart

log = logging.getLogger(__name__)


OVERLAP_TOLERANCE = 5 # tolerance in seconds. keep low! (1-5 seconds)
SLOT_MIN_DURATION = 15 * 60

class Autopilot(object):

    def __init__(self, channel_id, username):

        self.channel = Channel.objects.get(pk=channel_id)
        self.user = User.objects.get(username=username)
        self.dayparts = BroadcastDaypart.objects.filter(
            daypartset__channel=self.channel,
            enable_autopilot=True
        ).order_by('time_start')

        self.scheduled_emissions = []
        self.playlist_ids_to_exclude = []



    def schedule(self, *args, **kwargs):

        days_offset = kwargs.get('days_offset', 0)
        days_fill = kwargs.get('days_fill', 1)

        log.info('Scheduling: {:} days with offset {:} - on behalf of "{:}" on channel "{:}"'.format(
                days_fill,
                days_offset,
                self.user,
                self.channel
        ))

        now = datetime.datetime.now()
        day_start = now.date() + datetime.timedelta(days=days_offset)

        # populating excludes
        range_start = day_start - datetime.timedelta(days=5)
        range_end = day_start + datetime.timedelta(days=days_fill)

        exclude_qs = Emission.objects.filter(
            time_start__gt=range_start,
            time_end__lt=range_end,
            channel=self.channel,
        )

        for item in exclude_qs:

            if item.content_type.model == 'playlist':
                self.add_playlist_exclude(item.object_id)

        days_to_fill = []
        for i in range(days_fill):
            days_to_fill.append(
                day_start + datetime.timedelta(days=i)
            )

        for day_to_fill in days_to_fill:
            self.schedule_day(day=day_to_fill)


    def schedule_day(self, day):

        log.info('Scheduling day: {:}"'.format(day))

        dayparts_to_fill = []

        for daypart in self.dayparts:

            rel_time_start = daypart.time_start
            rel_time_end = daypart.time_end.max if daypart.time_end.hour == 0 else daypart.time_end

            abs_time_start = datetime.datetime.combine(day, rel_time_start)
            abs_time_end = datetime.datetime.combine(day, rel_time_end)

            slot = {
                'daypart': daypart,
                'weekday': day.weekday(),
                'rel_time_start': rel_time_start,
                'rel_time_end': rel_time_end,
                'abs_time_start': abs_time_start,
                'abs_time_end': abs_time_end,
            }

            if abs_time_end > datetime.datetime.now():
                dayparts_to_fill.append(slot)

        for dp in dayparts_to_fill:

            self.schedule_daypart(daypart=dp)

            # try:
            #     self.schedule_daypart(daypart=dp)
            # except Exception as e:
            #     print '*** %s ***' % e


        log.info('Added {:} emissions to scheduler on {:}'.format(len(self.scheduled_emissions), self.channel.name))


    def schedule_daypart(self, daypart):

        log.info('Scheduling daypart: {abs_time_start}-{abs_time_end} - Weekday: {weekday}"'.format(**daypart))

        daypart_duration = (daypart['abs_time_end'] - daypart['abs_time_start'])
        log.debug('Slot duration: {:} seconds'.format(daypart_duration.seconds))


        theme = 3

        if daypart['abs_time_start'].hour in [7, 19]:
            theme = 1

        if daypart['abs_time_start'].hour == 12:
            theme = 2

        if daypart['abs_time_start'].hour == 0:
            theme = 0

        # get applying dayparts & playlists for current slot
        daypart_qs = self.get_daypart_qs(
            weekday=daypart['weekday'],
            time_start=daypart['abs_time_start'],
            time_end=daypart['abs_time_end'],
        )


        next_start = daypart['abs_time_start']
        num_tries = 0
        while next_start and next_start < daypart['abs_time_end']:

            if num_tries > 20:
                raise IOError('io 10??')

            # needs to be re-fetched in every loop
            playlists_qs = self.get_playlist_qs(dayparts=daypart_qs)

            if not playlists_qs.exists():
                next_start = None

            else:

                max_min_durations = playlists_qs.values("target_duration").aggregate(
                        max=Max('target_duration'),
                        min=Min('target_duration')
                )

                next_start, next_end, min_duration, slot_duration = self.get_next_slot(
                        time_start=daypart['abs_time_start'],
                        time_end=daypart['abs_time_end'],
                        min_duration=max_min_durations.get('min', 0)
                )

            if next_start:
                qs = playlists_qs.filter(target_duration__lte=slot_duration)

                if qs.exists():

                    playlists = list(qs.order_by('?'))
                    shuffle(playlists)

                    playlist = playlists[0]
                    #playlist = qs.order_by('?')[0]



                    log.info('Scheduling at {:} - pk: {:} "{:}"'.format(next_start, playlist.pk, playlist.name))

                    emission = Emission(
                        content_object=playlist,
                        time_start=next_start,
                        channel=self.channel,
                        user=self.user,
                        color=theme
                    )

                    emission.save()

                    self.add_playlist_exclude(playlist.pk)

                    self.add_scheduled_emission(emission)



                    time.sleep(1)

            num_tries += 1



        # summary
        # durations = playlists_qs.values("target_duration").order_by('target_duration').distinct().annotate(number=Count("pk"))



    def get_next_slot(self, time_start, time_end, min_duration=None, max_duration=None):

        log.debug('Look for slot: {:} - {:} with durations min: {:} max: {:}'.format(
            time_start.time(), time_end.time(), min_duration, max_duration
        ))


        if (time_end - time_start).seconds < min_duration:
            return None, None, None, None


        next_start = None
        next_end = None

        # get last ending emission in slot
        ending_emissions = Emission.objects.filter(
            time_start__lte=time_start + datetime.timedelta(seconds=OVERLAP_TOLERANCE),
            time_end__gt=time_start + datetime.timedelta(seconds=OVERLAP_TOLERANCE),
            channel=self.channel
        ).order_by('-time_end')

        if ending_emissions.exists():
            #print 'NEXT: %s' % ending_emissions[0].time_end

            ending_emission = ending_emissions[0]

            next_start = ending_emission.time_end.replace(second=0)

            #print ending_emissions[0].pk

            log.debug('ending emission "{:}" in range {:}-{:}, next start: {:}'.format(
                ending_emission.name,
                ending_emission.time_start.time(),
                ending_emission.time_end.time(),
                next_start,
            ))

        else:
            #print 'NEXT: %s' % time_start
            next_start = time_start
            log.debug('no ending emission in range, next start: {:}'.format(next_start))


        # get next starting emission in slot
        starting_emissions = Emission.objects.filter(
            Q(time_start__gte=next_start - datetime.timedelta(seconds=OVERLAP_TOLERANCE)) &
            Q(time_start__lt=time_end),
            channel=self.channel,
        ).exclude(pk__in=[e.pk for e in ending_emissions]).order_by('time_start')

        if starting_emissions.exists():
            starting_emission = starting_emissions[0]



            if (starting_emission.time_start - next_start).seconds < min_duration + OVERLAP_TOLERANCE:
                next_start = starting_emission.time_end
                next_end = time_end
                slot_duration = 0

            else:
                print 'SLOT OK'
                next_end = starting_emission.time_start.replace(second=0)
                slot_duration = (next_end - next_start).seconds

            log.debug('starting emission "{:}" in range {:}-{:}, next end: {:}'.format(
                starting_emission.name,
                starting_emission.time_start.time(),
                starting_emission.time_end.time(),
                next_end,
            ))


        else:
            #print 'NEXT: %s' % time_start
            next_end = time_end
            log.debug('no starting emission in range, next end: {:}'.format(next_end))

            slot_duration = (next_end - next_start).seconds


        while next_start and not slot_duration >= min_duration:
            log.debug('slot duration of {:} is too short - requested: {:}'.format(
                    slot_duration, min_duration
            ))

            if not starting_emissions.exists():
                return None, next_end, min_duration, slot_duration

            next_start, next_end, min_duration, slot_duration = self.get_next_slot(
                time_start=starting_emissions[0].time_end.replace(second=0),
                time_end=time_end,
                min_duration=min_duration,
            )

        if next_start and next_start > time_end:
            return None, None, None, None

        if next_start:
            next_start = round_time(next_start, 300)


        return next_start, next_end, min_duration, slot_duration



    def add_scheduled_emission(self, emission):
        self.scheduled_emissions.append(emission)
        return self.scheduled_emissions


    def add_playlist_exclude(self, id):

        if not id in self.playlist_ids_to_exclude:
            self.playlist_ids_to_exclude.append(id)
        return self.playlist_ids_to_exclude


    def get_daypart_qs(self, weekday, time_start, time_end):

        daypart_qs = PlaylistDaypart.objects.filter(
            day=weekday,
            time_start__lte=time_start.time(),
            time_end__gte=time_end.time()
        )

        # very ugly. but no beter quick idea on how to get these bits
        if time_start.hour == 16:
            daypart_qs = PlaylistDaypart.objects.filter(
                day=weekday,
                time_start__lte=datetime.time(17, 0),
                time_end__gte=datetime.time(20, 0),
            )

        # very ugly. but no beter quick idea on how to get these bits
        if time_start.hour >= 20:
            daypart_qs = PlaylistDaypart.objects.filter(
                day=weekday,
                time_start__gte=datetime.time(20, 0),
            )

        return daypart_qs


    def get_playlist_qs(self, dayparts=None):

        duration_filter = 900
        type_filter = 'broadcast'
        broadcast_status_filter = 1
        rotation_filter = True

        playlists_qs = Playlist.objects.filter(
            target_duration__gte=duration_filter,
            type=type_filter,
            broadcast_status=broadcast_status_filter,
            rotation=rotation_filter,
            dayparts__in=dayparts
        ).exclude(
            pk__in=self.playlist_ids_to_exclude
        ).nocache()

        # try again without filtering duplicates
        if not playlists_qs.exists():
            playlists_qs = Playlist.objects.filter(
                target_duration__gte=duration_filter,
                type=type_filter,
                broadcast_status=broadcast_status_filter,
                rotation=rotation_filter,
                dayparts__in=dayparts
            ).nocache()

        # try again without looking at dayparts
        if not playlists_qs.exists():
            playlists_qs = Playlist.objects.filter(
                target_duration__gte=duration_filter,
                type=type_filter,
                broadcast_status=broadcast_status_filter,
                rotation=rotation_filter,
            ).exclude(
                pk__in=self.playlist_ids_to_exclude
            ).nocache()

        return playlists_qs


    def reset(self, *args, **kwargs):

        log.info('Resetting: user "{:}" for channel "{:}"'.format(
                self.user,
                self.channel
        ))

        # TODO: don't affect past
        delete_qs = Emission.objects.filter(
                channel=self.channel
        )

        if self.user:
            delete_qs = delete_qs.filter(
                    user=self.user
            )

        if kwargs.get('force'):
            delete_qs.delete()

        print 'Got %s entries marked for deletion' % delete_qs.count()

        if raw_input('are you sure? [y/N]: ').lower() == 'y':
            delete_qs.delete()







"""
http://stackoverflow.com/questions/3463930/how-to-round-the-minute-of-a-datetime-object-python
"""
def round_time(dt=None, round_to=60):
    if dt == None : dt = datetime.datetime.now()
    seconds = (dt - dt.min).seconds
    rounding = (seconds + round_to / 2) // round_to * round_to
    return dt + datetime.timedelta(0, rounding-seconds, -dt.microsecond)





