import calendar
import datetime
import logging
import tempfile
from django.core.mail import EmailMessage
from django.template.loader import get_template

from .utils.csv_output_suisa import statistics_as_csv

log = logging.getLogger(__name__)


def monthly_statistics_as_email(channel, year, month, email_addresses):

    log.info(
        'generating statistics for "%s" - year: %s - month: %s - to: %s',
        channel,
        year,
        month,
        ", ".join(email_addresses),
    )

    start = datetime.datetime.combine(datetime.date(year, month, 1), datetime.time.min)

    end = datetime.datetime.combine(
        datetime.date(year, month, calendar.monthrange(year, month)[1]),
        datetime.time.max,
    )

    with tempfile.NamedTemporaryFile() as f:
        statistics_as_csv(channel=channel, start=start, end=end, output=f.name)
        f.seek(0)

        tpl = get_template("statistics/email/_report_suisa.txt")
        channel_slug = channel.name.replace(" ", "-").lower()
        filename = f"{year}-{month}-{channel_slug}.csv"
        subject = f"Playout report {channel.name} | {month}-{year}"
        body = tpl.render(
            {"channel": channel, "month": month, "year": year, "filename": filename}
        )

        for email_address in email_addresses:
            email = EmailMessage(
                subject,
                body,
                "no-reply@openbroadcast.org",
                [email_address],
            )
            email.attach(filename, f.read(), "text/csv")
            email.send(fail_silently=False)
