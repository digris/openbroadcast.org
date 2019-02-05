# -*- coding: utf-8 -*-

import logging
import xlsxwriter

from django.utils import timezone



log = logging.getLogger(__name__)


def airplays_for_label_as_xls(label, objects, year, filename=None):
    ROW_LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXZY'

    first_row = 5
    last_row = len(objects) - 1 + first_row
    title = 'Airplay Statistics: open broadcast radio'
    filename = '{} Airplay statistics - {}.xlsx'.format(year, label.name)
    total_airplays = sum([i.num_airplays for i in objects])

    workbook = xlsxwriter.Workbook(
        filename, {
            'in_memory': True
        }
    )

    workbook.set_properties({
        'title': title,
        'subject': title,
        'author': 'digris AG',
        'company': 'digris AG',
        'created': timezone.now(),
    })

    # worksheet = workbook.add_worksheet('{}'.format(year))
    worksheet = workbook.add_worksheet()

    # Widen the first columns
    worksheet.set_column('A:C', 32)
    worksheet.set_column('D:D', 18)
    worksheet.set_row('1:1', 200)

    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({
        'bold': True
    })

    border_top = workbook.add_format({
        'bold': 1,
        'top': 1,
    })

    border_bottom = workbook.add_format({
        'bold': 1,
        'bottom': 1,
    })
