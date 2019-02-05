# -*- coding: utf-8 -*-

import datetime

import djclick as click
from alibrary.models import Label
from ...utils.queries import get_media_for_label
from ...utils.output import airplays_for_label_as_xls

@click.group()
def cli():
    """Statistics CLI"""
    pass


@cli.command()
@click.argument('scope', nargs=1)
@click.option('-i', '--id', required=True)
@click.option('-y', '--year', type=int)
def generate(scope, id, year):

    print('generate statistics: {} - {} - {}'.format(scope, id, year))

    label = Label.objects.get(pk=id)

    start = datetime.datetime.combine(
        datetime.date(year, 1, 1),
        datetime.time.min
    )

    end = datetime.datetime.combine(
        datetime.date(year, 12, 31),
        datetime.time.max
    )

    objects = get_media_for_label(label, start, end, 3)

    for obj in objects:
        print(obj.time_series)

    tot = sum([i.num_airplays for i in objects])
    print(tot)


    f = airplays_for_label_as_xls(label, objects, year)
