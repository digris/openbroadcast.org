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
    'title',
    'composer',
    'artist',
    'artist_info',
    'broadcaster',
    'broadcast_date',
    'time_of_broadcast',
    'duration',
    'works_index',
    'isrc',
    'label',
    'label_code',
    'catalog_number',
    'date_of_recording',
    'country_of_recording',
    'date_of_first_publication',
    'album_title',
    'track_number',
]


def parse_record(event, next_event=None):

    media = event.content_object

    if next_event:
        duration = next_event.created - event.created
    else:
        duration = media.duration

    record = {
        'title': '{}'.format(media.name),
        'broadcaster': event.event_content_object,
        'broadcast_date': event.created.date(),
        'time_of_broadcast': event.created.time(),
        'duration': duration,
        'artist': media.get_artist_display(),
        'isrc': media.isrc,
        'label': media.release.label.name if media.release and media.release.label else None,
        'label_code': media.release.label.labelcode if media.release and media.release.label else None,
        'catalog_number': media.release.catalognumber if media.release else None,
        'country_of_recording': media.release.release_country.iso2_code if media.release and media.release.release_country else None,
        'album_title': media.release.name if media.release else None,
        'track_number': media.tracknumber,
    }

    return record

def get_records(channel, start, end):

    qs = Event.objects.filter(
        created__range=(start, end),
        event_type_id=PLAYOUT_EVENT_TYPE_ID,
        event_object_id=channel.pk, # TODO: limit also to ct
    ).order_by(
        'created'
    )

    qs_as_list = list(qs)

    for index, event in enumerate(qs_as_list):
        try:
            next_event = qs_as_list[index + 1]
        except IndexError:
            next_event = None

        yield parse_record(event, next_event)


def statistics_as_csv(channel, start, end, output=None):

    ROW_LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXZY'

    # output = output or '{}_{}_{:02d}.csv'.format(channel.name, year, month)

    log.info('output to: {}'.format(output))

    with codecs.open(output, mode='wb', encoding='utf-8') as csv_file:

        writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)

        writer.writeheader()

        for record in get_records(channel, start, end):
            try:
                writer.writerow(record)
            except UnicodeEncodeError as e:
                pass






    # ###################################################################
    # # workbook preparation
    # ###################################################################
    # workbook = xlsxwriter.Workbook(
    #     output, {
    #         'in_memory': True
    #     }
    # )
    #
    # workbook.set_properties({
    #     'title': title,
    #     'subject': title,
    #     'author': 'digris AG',
    #     'company': 'digris AG',
    #     'created': timezone.now(),
    # })
    #
    # ###################################################################
    # # workbook style definitions
    # ###################################################################
    # bold = workbook.add_format({
    #     'bold': True
    # })
    #
    # border_top = workbook.add_format({
    #     'bold': 1,
    #     'top': 1,
    # })
    #
    # border_bottom = workbook.add_format({
    #     'bold': 1,
    #     'bottom': 1,
    # })
    #
    # small = workbook.add_format({
    #     'font_size': 9,
    #     'italic': 1,
    # })
    #
    # isrc_hint = workbook.add_format({
    #     'color': 'red',
    # })
    #
    #
    # ###################################################################
    # # add statistics as sheet per year
    # ###################################################################
    # for year in years:
    #
    #     start = year.get('start')
    #     end = year.get('end')
    #     objects = year.get('objects')
    #
    #     first_row = 7
    #     last_row = len(objects) - 1 + first_row
    #     total_events = sum([i.num_events for i in objects])
    #
    #     worksheet = workbook.add_worksheet('{}'.format(start.year))
    #
    #     # Widen the first columns
    #     worksheet.set_column('A:C', 32)
    #     worksheet.set_column('D:D', 18)
    #     worksheet.set_row('1:1', 200)
    #
    #     worksheet.merge_range('A1:C1', '{} - {:%Y-%m-%d} - {:%Y-%m-%d}'.format(title, start, end), bold)
    #     worksheet.merge_range('A2:C2', 'Label: {}'.format(label.name), bold)
    #     worksheet.merge_range('A3:C3', 'Total: {}'.format(total_events), bold)
    #
    #     worksheet.merge_range('A4:C4', '{}'.format(ISRC_HINT_TEXT), isrc_hint)
    #
    #     worksheet.merge_range('A5:C5', 'File created: {}'.format(timezone.now()), small)
    #
    #     worksheet.write('A{}'.format(first_row), 'Title', border_bottom)
    #     worksheet.write('B{}'.format(first_row), 'Artist', border_bottom)
    #     worksheet.write('C{}'.format(first_row), 'Release', border_bottom)
    #     worksheet.write('D{}'.format(first_row), 'ISRC', border_bottom)
    #
    #     try:
    #         header = [calendar.month_name[dt.month] for dt in [i[0] for i in objects[0].time_series]]
    #     except IndexError:
    #         header = []
    #
    #     # write date (month) headers
    #     for index, item in enumerate(header, start=4):
    #         worksheet.write(first_row - 1, index, item, border_bottom)
    #
    #         # set column width
    #         worksheet.set_column(index, index, 14)
    #
    #     # write entries
    #     for index, item in enumerate(objects, start=first_row):
    #         worksheet.write(index, 0, item.name)
    #         worksheet.write(index, 1, item.artist.name)
    #         worksheet.write(index, 2, item.release.name)
    #         if item.isrc:
    #             worksheet.write(index, 3, item.isrc)
    #         else:
    #             worksheet.write_url(index, 3, '{}{}'.format(SITE_URL, item.get_edit_url()), string='Add ISRC')
    #
    #         # add monthly numbers
    #         for ts_index, ts_item in enumerate([ts[1] for ts in item.time_series], start=4):
    #             worksheet.write(index, ts_index, ts_item)
    #
    #     # add summs / formula
    #     worksheet.merge_range('A{}:D{}'.format(last_row + 2, last_row + 2), 'Total', border_top)
    #
    #     for index, item in enumerate(header, start=4):
    #         letter = ROW_LETTERS[index]
    #         formula = '=SUM({}{}:{}{})'.format(letter, first_row + 1, letter, last_row + 1)
    #         worksheet.write_formula(last_row + 1, index, formula, border_top)
    #
    #
    #
    #     # worksheet.merge_range('A{}:C{}'.format(last_row + 4, last_row + 4), '{}'.format(timezone.now()), small)
    #
    #
    #
    #
    # workbook.close()
