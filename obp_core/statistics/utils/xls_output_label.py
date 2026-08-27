import logging
import calendar
import xlsxwriter

from django.utils import timezone
from django.conf import settings

SITE_URL = getattr(settings, "SITE_URL")
ISRC_HINT_TEXT = """Please be aware that collecting societies only will distribute the earnings properly if an ISRC code is present."""

log = logging.getLogger(__name__)


def label_statistics_as_xls(label, years, title=None, output=None):

    ROW_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXZY"

    title = title or "Airplay Statistics: open broadcast radio"
    output = output or f"Airplay statistics - {label.name}.xlsx"

    log.info(f"output to: {output}")

    ###################################################################
    # workbook preparation
    ###################################################################
    workbook = xlsxwriter.Workbook(output, {"in_memory": True})

    workbook.set_properties(
        {
            "title": title,
            "subject": title,
            "author": "digris AG",
            "company": "digris AG",
            "created": timezone.now(),
        }
    )

    ###################################################################
    # workbook style definitions
    ###################################################################
    bold = workbook.add_format({"bold": True})

    border_top = workbook.add_format({"bold": 1, "top": 1})

    border_bottom = workbook.add_format({"bold": 1, "bottom": 1})

    small = workbook.add_format({"font_size": 9, "italic": 1})

    isrc_hint = workbook.add_format({"color": "red"})

    ###################################################################
    # add statistics as sheet per year
    ###################################################################
    for year in years:

        start = year.get("start")
        end = year.get("end")
        objects = year.get("objects")

        first_row = 7
        last_row = len(objects) - 1 + first_row
        total_events = sum([i.num_events for i in objects])

        worksheet = workbook.add_worksheet(f"{start.year}")

        # Widen the first columns
        worksheet.set_column("A:C", 32)
        worksheet.set_column("D:D", 18)
        worksheet.set_row("1:1", 200)

        worksheet.merge_range(
            "A1:C1", f"{title} - {start:%Y-%m-%d} - {end:%Y-%m-%d}", bold
        )
        worksheet.merge_range("A2:C2", f"Label: {label.name}", bold)
        worksheet.merge_range("A3:C3", f"Total: {total_events}", bold)

        worksheet.merge_range("A4:C4", f"{ISRC_HINT_TEXT}", isrc_hint)

        worksheet.merge_range("A5:C5", f"File created: {timezone.now()}", small)

        worksheet.write(f"A{first_row}", "Title", border_bottom)
        worksheet.write(f"B{first_row}", "Artist", border_bottom)
        worksheet.write(f"C{first_row}", "Release", border_bottom)
        worksheet.write(f"D{first_row}", "ISRC", border_bottom)

        try:
            header = [
                calendar.month_name[dt.month]
                for dt in [i[0] for i in objects[0].time_series]
            ]
        except IndexError:
            header = []

        # write date (month) headers
        for index, item in enumerate(header, start=4):
            worksheet.write(first_row - 1, index, item, border_bottom)

            # set column width
            worksheet.set_column(index, index, 14)

        # write entries
        for index, item in enumerate(objects, start=first_row):
            worksheet.write(index, 0, item.name)
            worksheet.write(index, 1, item.artist.name)
            worksheet.write(index, 2, item.release.name)
            if item.isrc:
                worksheet.write(index, 3, item.isrc)
            else:
                worksheet.write_url(
                    index,
                    3,
                    f"{SITE_URL}{item.get_edit_url()}",
                    string="Add ISRC",
                )

            # add monthly numbers
            for ts_index, ts_item in enumerate(
                [ts[1] for ts in item.time_series], start=4
            ):
                worksheet.write(index, ts_index, ts_item)

        # add summs / formula
        worksheet.merge_range(
            f"A{last_row + 2}:D{last_row + 2}", "Total", border_top
        )

        for index, item in enumerate(header, start=4):
            letter = ROW_LETTERS[index]
            formula = "=SUM({}{}:{}{})".format(
                letter, first_row + 1, letter, last_row + 1
            )
            worksheet.write_formula(last_row + 1, index, formula, border_top)

        # worksheet.merge_range('A{}:C{}'.format(last_row + 4, last_row + 4), '{}'.format(timezone.now()), small)

    workbook.close()
