# -*- coding: utf-8 -*-
import time
import datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Count
from django.utils.translation import ugettext as _
from atracker.models import Event

DEFAULT_ACTIONS = ["playout", "stream", "download"]


def last_day_of_month(date):
    if date.month == 12:
        return date.replace(day=31)
    return date.replace(month=date.month + 1, day=1) - datetime.timedelta(days=1)


class ObjectStatistics(object):
    def __init__(self, obj=None, user=None, artist=None, release=None):
        self.obj = obj
        self.user = user
        self.artist = artist
        self.release = release

    def generate(self, actions=DEFAULT_ACTIONS):

        stats = []
        # TODO: maybe modularize!
        for action in actions:

            if action == "playout":
                stats.append({"label": _("Airplays"), "data": self.get_stats(action)})

            if action == "stream":
                stats.append({"label": _("Plays"), "data": self.get_stats(action)})

            if action == "download":
                stats.append({"label": _("Downloads"), "data": self.get_stats(action)})

            if action == "update":
                stats.append({"label": _("Updates"), "data": self.get_stats(action)})

        return stats

    def get_stats(self, action):

        month_range = 12

        # calculate range
        now = datetime.date.today()
        range_start = (now - relativedelta(months=(month_range - 1))).replace(day=1)
        range_end = last_day_of_month(now)

        # generate month_map with zero-counts
        month_map = []
        for i in range(month_range):
            td = range_start + relativedelta(months=i)
            month_map.append({"id": td.month, "date": td, "count": 0})

        if self.obj:
            events = (
                Event.objects.by_obj(obj=self.obj)
                .filter(
                    event_type__title="%s" % action,
                    created__gte=range_start,
                    created__lte=range_end,
                )
                .extra(select={"month": "extract( month from created )"})
                .values("month")
                .annotate(dcount=Count("created"))
            )

        elif self.user:
            events = (
                Event.objects.filter(
                    user=self.user,
                    event_type__title="%s" % action,
                    created__gte=range_start,
                    created__lte=range_end,
                )
                .extra(select={"month": "extract( month from created )"})
                .values("month")
                .annotate(dcount=Count("created"))
            )
        elif self.artist:
            from django.contrib.contenttypes.models import ContentType

            ctype = ContentType.objects.get(app_label="alibrary", model="media")
            events = (
                Event.objects.filter(
                    object_id__in=self.artist.media_artist.values_list(
                        "pk", flat=True
                    ).distinct(),
                    content_type=ctype,
                    event_type__title="%s" % action,
                    created__gte=range_start,
                    created__lte=range_end,
                )
                .extra(select={"month": "extract( month from created )"})
                .values("month")
                .annotate(dcount=Count("created"))
            )
        elif self.release:
            from django.contrib.contenttypes.models import ContentType

            ctype = ContentType.objects.get(app_label="alibrary", model="media")
            events = (
                Event.objects.filter(
                    object_id__in=self.release.media_release.values_list(
                        "pk", flat=True
                    ).distinct(),
                    content_type=ctype,
                    event_type__title="%s" % action,
                    created__gte=range_start,
                    created__lte=range_end,
                )
                .extra(select={"month": "extract( month from created )"})
                .values("month")
                .annotate(dcount=Count("created"))
            )
        else:
            events = (
                Event.objects.filter(
                    event_type__title="%s" % action,
                    created__gte=range_start,
                    created__lte=range_end,
                )
                .extra(select={"month": "extract( month from created )"})
                .values("month")
                .annotate(dcount=Count("created"))
            )

        # map results to month_map (ugly, i know...)
        for item in events:
            for el in month_map:
                if el["id"] == item["month"]:
                    # el['count'] = item['dcount']
                    el["count"] += 1

        return self.serialize(month_map)

    def serialize(self, month_map):

        data = []
        for el in month_map:
            ts = int((time.mktime(el["date"].timetuple()))) * 1000
            data.append([ts, el["count"]])

        return data
