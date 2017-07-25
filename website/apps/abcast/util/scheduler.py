import datetime
from django.contrib.sites.models import Site
from abcast.models import Emission

EXCHANGE = 'fs' # 'fs' or 'http'

def get_schedule_for_pypo(range_start, range_end, exclude=None, channel=None):

    es = Emission.objects.filter(time_end__gte=range_start, time_start__lte=range_end)
    if exclude:
        es = es.exclude(pk__in=exclude)

    base_url = Site.objects.get_current().domain

    media = {}

    """
    print
    print '--------------------------------------------------------------------'
    print '| getting schedule for PYPO                                        |'
    print '--------------------------------------------------------------------'
    print 'range start             : %s ' % range_start
    print 'range end               : %s ' % range_end
    print 'total emissions in range: %s' % es.count()
    print '--------------------------------------------------------------------'
    print
    """

    for e in es:

        e_start = e.time_start
        offset = 0
        items = e.content_object.get_items()
        for item in items:
            co = item.content_object
            if not co or not co.get_duration():
                return
            i_start = e_start + datetime.timedelta(milliseconds=offset)
            i_end = e_start + datetime.timedelta(milliseconds=offset + co.get_duration())


            # i_end needs cue / cross calculations
            # TODO: verify calculations!!!!
            # i_end = i_end - datetime.timedelta(milliseconds=( item.cue_in + item.cue_out + item.fade_cross ))
            i_end = i_end - datetime.timedelta(milliseconds=( item.cue_in + item.cue_out ))


            # map to ugly airtime format
            i_start_str = i_start.strftime('%Y-%m-%d-%H-%M-%S')
            i_end_str = i_end.strftime('%Y-%m-%d-%H-%M-%S')


            """
            compose media data
            """
            if i_end < range_start:
                pass
            else:

                uri = None

                if EXCHANGE == 'http':
                    raise NotImplemented('http transport not implemented anymore')

                if EXCHANGE == 'fs':
                    uri = co.get_playout_file(absolute=True)

                data = {

                        'id': str(co.uuid),
                        'cue_in': float(item.cue_in) / 1000,
                        'cue_out': float(co.get_duration() - item.cue_out) / 1000,
                        'fade_in': item.fade_in,
                        'fade_out': item.fade_out,
                        'fade_cross': item.fade_cross / 1000,
                        # TODO: just enabling crossfade to test new ls version
                        #'fade_cross': float(co.get_duration() - item.cue_out - item.fade_cross) / 1000,
                        #'fade_cross': 0,
                        'replay_gain': 0,
                        'independent_event': False,
                        'start': "%s" % i_start_str,
                        'end': "%s" % i_end_str,
                        'artist': 'artsi',
                        'title': 'fartsi',
                        'show_name': "%s" % e.name,
                        'uri': uri,
                        'row_id': str(co.uuid),
                        'type': "file",

                        }

                media['%s' % i_start_str] = data

            offset += ( co.get_duration() - (item.cue_in + item.cue_out + item.fade_cross ) )

    return media



def get_history(range, channel=None):

    now = datetime.datetime.now()
    range_start = now - datetime.timedelta(seconds=range)

    EMISSION_LIMIT = 4

    emissions = Emission.objects.filter(time_start__lte=now, channel=channel).order_by('-time_start')[0:EMISSION_LIMIT]
    base_url = Site.objects.get_current().domain

    objects = []

    """
    print
    print u'--------------------------------------------------------------------'
    print u'| getting schedule history                                        |'
    print u'--------------------------------------------------------------------'
    print u'channel                 : %s ' % channel.name
    print u'total emissions in range: %s' % emissions.count()
    print u'--------------------------------------------------------------------'
    print
    """

    for emission in emissions:

        print '*******************************'
        print 'range start: %s' % range_start
        print 'now: %s' % now

        for emission_item in emission.get_timestamped_media():
            emission_item.emission = emission

            if range_start < emission_item.timestamp < now:

                #print '////////////////////////////////'
                #print 'is %s > %s ?' % (emission_item.timestamp, range_start)
                #print 'is %s < %s ?' % (emission_item.timestamp, now)
                #print

                objects.append({
                    'emission': emission.get_api_url(),
                    'item': emission_item.content_object.get_api_url(),
                    'time_start': emission_item.timestamp,
                    'time_end': None,
                    'verbose_name': emission_item.content_object.name,
                })

    objects.reverse()

    return objects[1:]



def get_schedule(range_start=0, range_end=0, channel=None):
    """
    @range_start: seconds back or datetime
    @range_end: seconds forward or datetime
    """

    now = datetime.datetime.now()

    if not isinstance(range_start, datetime.datetime):
        range_start = now - datetime.timedelta(seconds=range_start)

    if not isinstance(range_end, datetime.datetime):
        range_end = now + datetime.timedelta(seconds=range_end)

    """
    print
    print u'--------------------------------------------------------------------'
    print u'| getting schedule history                                        |'
    print u'--------------------------------------------------------------------'
    print u'channel                 : %s ' % channel.name
    print u'range_start             : %s ' % range_start
    print u'range_end               : %s ' % range_end
    print
    """

    emissions = Emission.objects.filter(
        time_end__gte=range_start,
        time_start__lte=range_end,
        channel=channel).order_by('-time_start')

    objects = []

    """
    print u'total emissions in range: %s' % emissions.count()
    print u'--------------------------------------------------------------------'
    """

    for emission in emissions:

        for emission_item in emission.get_timestamped_media():

            # map timestamps
            emission_item.time_start = emission_item.timestamp
            emission_item.time_end = emission_item.timestamp + datetime.timedelta(milliseconds=emission_item.playout_duration)

            # check if ranges apply
            if emission_item.time_end >= range_start and emission_item.time_start <= range_end:

                objects.append({
                    'emission': emission.get_api_url(),
                    'item': emission_item.content_object.get_api_url(),
                    'time_start': emission_item.time_start,
                    'time_end': emission_item.time_end,
                    'verbose_name': emission_item.content_object.name,
                })

    objects.reverse()

    return objects

