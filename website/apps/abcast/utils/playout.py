# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import datetime
import logging

from ..models import Emission

log = logging.getLogger(__name__)


def map_item(item, uuid, duration, time_start, time_end):

    uri = item.content_object.get_playout_file(absolute=False)
    uri_abs = item.content_object.get_playout_file(absolute=True)

    return {
        "uuid": str(uuid),
        "duration": duration / 1000.0,
        "cue_in": float(item.cue_in) / 1000.0,
        "cue_out": float(duration - item.cue_out) / 1000.0,
        "fade_in": item.fade_in,
        "fade_out": item.fade_out,
        "fade_cross": item.fade_cross / 1000.0,
        # TODO: just enabling crossfade to test new ls version
        # 'fade_cross': float(co.get_duration() - item.cue_out - item.fade_cross) / 1000,
        # 'fade_cross': 0,
        "start": "%s" % time_start,
        "end": "%s" % time_end,
        "uri": uri,
        "uri_abs": uri_abs,
        "type": "file",
    }


def map_emission(emission, time_start):

    emission_start = emission.time_start
    offset = 0

    for item in emission.content_object.get_items():
        co = item.content_object

        try:
            total_duration = co.get_duration()
            playout_duration = total_duration - (
                item.cue_in + item.cue_out + item.fade_cross
            )
        except Exception as e:
            log.warning("unable to get duration {}".format(e))
            continue

        # get absolute times
        item_start = emission_start + datetime.timedelta(milliseconds=offset)
        item_end = item_start + datetime.timedelta(milliseconds=playout_duration)

        if item_end < time_start:
            print(item_end, "<", time_start)
            continue

        offset += playout_duration

        yield map_item(
            item,
            co.uuid,
            duration=total_duration,
            time_start=item_start,
            time_end=item_end,
        )


def get_playout_schedule(time_start, time_end):

    log.info("get schedule for {} {}".format(time_start, time_end))

    qs = Emission.objects.filter(time_end__gte=time_start, time_start__lte=time_end)

    schedule = []

    for emission in qs:
        schedule += map_emission(emission, time_start)

    return schedule
