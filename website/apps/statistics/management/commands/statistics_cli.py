# -*- coding: utf-8 -*-

import djclick as click
from datetime import datetime
from alibrary.models import Label
from abcast.models import Channel
from atracker.models import EventType
from ...label_statistics import (
    yearly_summary_for_label_as_xls,
    summary_for_label_as_xls,
)

# from ...suisa_statistics import monthly_for_channel_as_xls
from ...suisa_statistics import monthly_statistics_as_email


@click.group()
def cli():
    """Statistics CLI"""
    pass


@cli.command()
@click.argument("scope", nargs=1)
@click.option("-i", "--id", required=True)
@click.option("-y", "--year", type=int, required=False)
@click.option("-p", "--path", type=click.Path(), required=False)
def label_statistics(scope, id, year, path):

    print(
        "generate label statistics: scope: {} - id: {} - year: {} - output: {}".format(
            scope, id, year, path
        )
    )

    event_type_id = EventType.objects.get(title=scope).pk

    label = Label.objects.get(pk=id)

    if year:
        yearly_summary_for_label_as_xls(
            year=year, label=label, event_type_id=event_type_id, output=path
        )

    else:
        summary_for_label_as_xls(label=label, event_type_id=event_type_id, output=path)


@cli.command()
@click.option("-i", "--channel-id", "channel_id", required=True)
@click.option("-y", "--year", type=int, required=False)
@click.option("-m", "--month", type=int, required=False)
@click.option("-e", "--email", "email_addresses", multiple=True, required=True)
def suisa_statistics(channel_id, year, month, email_addresses):
    """
    usage:

        ./manage.py statistics_cli suisa_statistics -i 1 -y 2019 -m 03 -e foo@example.org

    If not both 'year' and 'month' are specified the last completed month will be used.
    """

    if not (year and month):
        now = datetime.now()
        print(now.year)
        print(now.month)

        if now.month == 1:
            year = now.year - 1
            month = 12
        else:
            year = now.year
            month = now.month - 1

    click.echo(
        "generate suisa report: channel: {} - year: {} - month: {} - to: {}".format(
            channel_id, year, month, ", ".join(email_addresses)
        )
    )

    channel = Channel.objects.get(pk=channel_id)

    monthly_statistics_as_email(
        channel=channel, year=year, month=month, email_addresses=email_addresses
    )
