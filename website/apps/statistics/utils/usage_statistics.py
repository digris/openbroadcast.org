# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import qsstats
from django.contrib.contenttypes.models import ContentType
from atracker.models import Event
from alibrary.models import Media


logger = logging.getLogger(__name__)


def get_event_types(qs):
    return list(set(qs.values_list("event_type__title", flat=True)))


def get_months(qs):
    return list(set(qs.values_list("event_type__title", flat=True)))


def get_media_statistics(media_ids, start, end):
    ct = ContentType.objects.get(app_label="alibrary", model="media")
    qs = Event.objects.filter(
        object_id__in=media_ids,
        content_type=ct,
        created__gte=start,
        created__lte=end,
    )

    event_types = get_event_types(qs)

    labels = []
    datasets = []

    for event_type in event_types:
        qss = qsstats.QuerySetStats(qs.filter(event_type__title=event_type), "created")
        ts = qss.time_series(start, end, "months")
        if not labels:
            labels = [t[0].strftime("%b. %Y") for t in ts]
        datasets.append({"label": event_type, "data": [t[1] for t in ts]})

    return {
        "labels": labels,
        "datasets": datasets,
    }


def get_media_ids(obj):
    # TODO: implement this in a more modular way
    ct = obj.get_ct()
    if ct == "alibrary.label":
        return Media.objects.filter(release__label=obj).values_list('id', flat=True)
    return [m.id for m in obj.get_media()]


def get_usage_statistics(obj, start, end):
    logger.debug('usage statistics for "{}", {} - {}'.format(obj, start, end))

    # TODO: implement this in a more modular way
    media_ids = get_media_ids(obj)

    return get_media_statistics(media_ids, start, end)
