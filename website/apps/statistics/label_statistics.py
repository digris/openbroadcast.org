# -*- coding: utf-8 -*-
import datetime
import logging

from django.utils import timezone
from atracker.models import EventType

from .utils.queries import get_media_for_label
from .utils.output import label_statistics_as_xls

TITLE_MAP = {
    'playout': 'Airplay statistics',
    'download': 'Download statistics',
    'stream': 'Stream statistics',
}

log = logging.getLogger(__name__)

def yearly_summary_for_label_as_xls(year, label, event_type_id, output=None):

    log.debug('generating {} statistics for {} - {}'.format(
        event_type_id, label, year
    ))

    year = int(year)
    event_type = EventType.objects.get(
        pk=event_type_id
    )

    title = '{}: open broadcast radio'.format(
        TITLE_MAP.get(event_type.title)
    )

    start = datetime.datetime.combine(
        datetime.date(year, 1, 1),
        datetime.time.min
    )

    end = datetime.datetime.combine(
        datetime.date(year, 12, 31),
        datetime.time.max
    )

    objects = get_media_for_label(
        label=label,
        start=start,
        end=end,
        event_type_id=event_type_id
    )

    years = [{
        'start': start,
        'end': end,
        'objects': objects
    }]

    label_statistics_as_xls(
        label=label,
        years=years,
        title=title,
        output=output
    )

    return output


def summary_for_label_as_xls(label, event_type_id, output=None):

    log.debug('generating {} statistics for {} - since created'.format(
        event_type_id, label
    ))

    event_type = EventType.objects.get(
        pk=event_type_id
    )

    title = '{}: open broadcast radio'.format(
        TITLE_MAP.get(event_type.title)
    )

    years = []
    year_start = label.created.year if label.created.year >= 2014 else 2014
    year_end = timezone.now().year

    for year in range(year_end, year_start - 1, -1):

        start = datetime.datetime.combine(
            datetime.date(year, 1, 1),
            datetime.time.min
        )

        end = datetime.datetime.combine(
            datetime.date(year, 12, 31),
            datetime.time.max
        )

        objects = get_media_for_label(
            label=label,
            start=start,
            end=end,
            event_type_id=event_type_id
        )

        years.append({
            'start': start,
            'end': end,
            'objects': objects
        })

    label_statistics_as_xls(
        label=label,
        years=years,
        title=title,
        output=output
    )

    return output

