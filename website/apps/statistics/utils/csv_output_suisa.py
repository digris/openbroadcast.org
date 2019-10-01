# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import logging
import codecs
import csv

from atracker.models import Event

from django.utils import timezone
from django.conf import settings

PLAYOUT_EVENT_TYPE_ID = 3

log = logging.getLogger(__name__)

FIELDNAMES = [
    "title",
    "composer",
    "artist",
    "artist_info",
    "broadcaster",
    "broadcast_date",
    "time_of_broadcast",
    "duration",
    "works_index",
    "isrc",
    "label",
    "label_code",
    "catalog_number",
    "date_of_recording",
    "country_of_recording",
    "date_of_first_publication",
    "album_title",
    "track_number",
]


def parse_record(event, next_event=None):

    media = event.content_object

    if next_event:
        duration = next_event.created - event.created
    else:
        duration = media.duration

    record = {
        "title": "{}".format(media.name),
        "broadcaster": event.event_content_object,
        "broadcast_date": event.created.date(),
        "time_of_broadcast": event.created.time(),
        "duration": duration,
        "artist": media.get_artist_display(),
        "isrc": media.isrc,
        "label": media.release.label.name
        if media.release and media.release.label
        else None,
        "label_code": media.release.label.labelcode
        if media.release and media.release.label
        else None,
        "catalog_number": media.release.catalognumber if media.release else None,
        "country_of_recording": media.release.release_country.iso2_code
        if media.release and media.release.release_country
        else None,
        "album_title": media.release.name if media.release else None,
        "track_number": media.tracknumber,
    }

    return record


def get_records(channel, start, end):

    qs = Event.objects.filter(
        created__range=(start, end),
        event_type_id=PLAYOUT_EVENT_TYPE_ID,
        event_object_id=channel.pk,  # TODO: limit also to ct
    ).order_by("created")

    qs_as_list = list(qs)

    for index, event in enumerate(qs_as_list):
        try:
            next_event = qs_as_list[index + 1]
        except IndexError:
            next_event = None

        yield parse_record(event, next_event)


def statistics_as_csv(channel, start, end, output=None):

    # output = output or '{}_{}_{:02d}.csv'.format(channel.name, year, month)

    log.info("output to: {}".format(output))

    with codecs.open(output, mode="wb", encoding="utf-8") as csv_file:

        writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)

        writer.writeheader()

        for record in get_records(channel, start, end):
            try:
                writer.writerow(record)
            except UnicodeEncodeError as e:
                pass
