# -*- coding: utf-8 -*-
import calendar
import datetime
import logging

from django.utils import timezone
from atracker.models import EventType

from .utils.queries import get_media_for_label
from .utils.csv_output_suisa import statistics_as_csv

# TITLE_MAP = {
#     'playout': 'Airplay statistics',
#     'download': 'Download statistics',
#     'stream': 'Stream statistics',
# }

log = logging.getLogger(__name__)

def monthly_for_channel_as_xls(channel, year, month, output=None):

    log.debug('generating statistics for "{}" - year: {} - month: {}'.format(
        channel, year, month
    ))

    start = datetime.datetime.combine(
        datetime.date(year, month, 1),
        datetime.time.min
    )

    end = datetime.datetime.combine(
        datetime.date(year, month, calendar.monthrange(year, month)[1]),
        datetime.time.max
    )

    statistics_as_csv(
        channel=channel,
        start=start,
        end=end,
        output=output
    )

    return output
