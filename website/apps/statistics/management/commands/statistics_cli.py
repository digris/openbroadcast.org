# -*- coding: utf-8 -*-

import datetime

import djclick as click
from alibrary.models import Label
from atracker.models import EventType
from ...label_statistics import yearly_summary_for_label_as_xls, summary_for_label_as_xls


@click.group()
def cli():
    """Statistics CLI"""
    pass


@cli.command()
@click.argument('scope', nargs=1)
@click.option('-i', '--id', required=True)
@click.option('-y', '--year', type=int, required=False)
@click.option('-p', '--path', type=click.Path(), required=False)
def generate(scope, id, year, path):

    print('generate statistics: {} - {} - {} - {}'.format(scope, id, year, path))

    event_type_id = EventType.objects.get(title=scope).pk

    label = Label.objects.get(pk=id)

    if year:

        yearly_summary_for_label_as_xls(
            year=year,
            label=label,
            event_type_id=event_type_id,
            output=path
        )

    else:
        summary_for_label_as_xls(
            label=label,
            event_type_id=event_type_id,
            output=path
        )
