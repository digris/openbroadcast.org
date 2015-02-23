import datetime
from django.contrib.sites.models import Site
from abcast.models import Emission

EXCHANGE = 'fs' # 'fs' or 'http'


def get_schedule(range_start, range_end, exclude=None, channel=None):

    return


def get_schedule_for_pypo(range_start, range_end, exclude=None, channel=None):
    """

    :param range_start:
    :param range_end:
    :param exclude:
    :param channel:
    returns pypo readable schedule
    """


    es = Emission.objects.filter(time_end__gte=range_start, time_start__lte=range_end)
    if exclude:
        es = es.exclude(pk__in=exclude)

    base_url = Site.objects.get_current().domain


    # es = Emission.objects.future()
    media = {}
    print
    print '--------------------------------------------------------------------'
    print '| getting schedule for PYPO                                        |'
    print '--------------------------------------------------------------------'
    print 'range start             : %s ' % range_start
    print 'range end               : %s ' % range_end
    print 'total emissions in range: %s' % es.count()
    print '--------------------------------------------------------------------'
    print


    for e in es:
        try:
            print
            print 'emission: %s | %s - %s' % (e.name, e.pk, e.get_absolute_url())
            #print 'co      : %s | %s - %s' % (e.content_object.name, e.content_object.pk, e.content_object.get_absolute_url())
        except:
            pass

        e_start = e.time_start
        offset = 0
        items = e.content_object.get_items()
        for item in items:
            co = item.content_object
            i_start = e_start + datetime.timedelta(milliseconds=offset)
            i_end = e_start + datetime.timedelta(milliseconds=offset + co.get_duration())


            # i_end needs cue / cross calculations
            # TODO: verify calculations!!!!
            # i_end = i_end - datetime.timedelta(milliseconds=( item.cue_in + item.cue_out + item.fade_cross ))
            i_end = i_end - datetime.timedelta(milliseconds=( item.cue_in + item.cue_out ))


            # map to ugly airtime format
            i_start_str = i_start.strftime('%Y-%m-%d-%H-%M-%S')
            i_end_str = i_end.strftime('%Y-%m-%d-%H-%M-%S')

            #print 'cue_in  -  cue_out  -  fade_in  -  fade_out  -  fade_cross'
            #print '%06d     %06d      %06d      %06d       %06d' % (item.cue_in, item.cue_out, item.fade_in, item.fade_out, item.fade_cross)

            #print 'offset:     %s' % offset

            #print 'start:      %s' % i_start
            #print 'end:        %s' % i_end


            """
            compose media data
            """
            if i_end < range_start:
                pass
            else:
                if EXCHANGE == 'http':
                    try:
                        uri = "http://%s%s" % (base_url, co.get_stream_url())
                    except Exception, ex:
                        uri = None

                if EXCHANGE == 'fs':
                    uri = co.get_playout_file(absolute=False)

                data = {
                        #'id': co.pk,
                        'id': co.uuid,
                        'cue_in': float(item.cue_in) / 1000,
                        'cue_out': float(co.get_duration() - item.cue_out) / 1000,
                        'fade_in': item.fade_in,
                        'fade_out': item.fade_out,
                        'fade_cross': item.fade_cross / 1000,
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
                        'row_id': co.uuid,
                        'type': "file",

                        }

                media['%s' % i_start_str] = data

            #offset += ( co.get_duration() - (item.cue_in + item.cue_out) )
            offset += ( co.get_duration() - (item.cue_in + item.cue_out + item.fade_cross ) )


    #print media
    return media



def get_history(range, channel=None):

    now = datetime.datetime.now()
    range_start = now - datetime.timedelta(seconds=range)

    EMISSION_LIMIT = 4

    emissions = Emission.objects.filter(time_start__lte=now, channel=channel).order_by('-time_start')[0:EMISSION_LIMIT]
    base_url = Site.objects.get_current().domain

    objects = []

    print
    print u'--------------------------------------------------------------------'
    print u'| getting schedule history                                        |'
    print u'--------------------------------------------------------------------'
    print u'channel                 : %s ' % channel.name
    print u'total emissions in range: %s' % emissions.count()
    print u'--------------------------------------------------------------------'
    print


    for emission in emissions:

        print u'--------------------------------------------------------------------'
        print u'emission: %s | %s - %s' % (emission.name, emission.pk, emission.get_absolute_url())
        print u'%s - %s' % (emission.time_start, emission.time_end)

        for emission_item in  emission.get_timestamped_media():
            #print u'%s - %s' % (emission_item.timestamp, emission_item.content_object)
            emission_item.emission = emission
            if emission_item.timestamp > range_start and emission_item.timestamp < now:
                print '+ IN RANGE'
                objects.append({
                    'emission': emission.get_api_url(),
                    'item': emission_item.content_object.get_api_url(),
                    'time_start': emission_item.timestamp,
                    'time_end': None,
                    'verbose_name': emission_item.content_object.name,
                })
            else:
                print '- OUT OF RANGE'


        print


    objects.reverse()

    return objects

