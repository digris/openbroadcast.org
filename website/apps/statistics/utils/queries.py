# -*- coding: utf-8 -*-

import logging
import qsstats

from time import time
from django.db.models import Count, Prefetch
from alibrary.models import Media
from atracker.models import Event

log = logging.getLogger(__name__)


def get_events(obj, event_type_id, start, end):

    #######################################################################
    # attention! this takes ~1 second per item!
    #######################################################################

    # log.debug('get_events: {}'.format(obj))

    qs = obj.events.filter(
        event_type_id=event_type_id
    )

    # qs = obj.events

    qss = qsstats.QuerySetStats(qs, 'created')
    time_series = qss.time_series(start, end, 'months')

    return time_series


def get_media_for_label(label, start, end, event_type_id):

    log.debug('get_media_for_label: "{}" - range: {} - {}, type: {}'.format(label, start, end, event_type_id))

    qs = Media.objects.all()

    #######################################################################
    # get queryset for media objects containing events for a given
    # date range
    #######################################################################
    qs = qs.exclude(
        # release__in=Release.objects.filter(name__icontains='STATION-ID')
    ).filter(
        events__event_type_id=event_type_id,
        release__label=label,
        events__created__range=[
            start,
            end
        ]
    ).annotate(
        num_events=Count('events')
    ).select_related(
        'release',
        'release__label',
        'artist',
    ).prefetch_related(
        Prefetch(
            'events',
            queryset=Event.objects.filter(event_type__id=event_type_id)
        )
    ).order_by(
        'release__name',
        'name'
    )


    #######################################################################
    # 'annotate' the objects with time_series information
    #######################################################################
    objects = []
    for obj in qs:
        time_series = get_events(obj, event_type_id, start, end)
        obj.time_series = time_series

        objects.append(obj)


    return objects
