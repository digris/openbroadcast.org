#-*- coding: utf-8 -*-
from __future__ import unicode_literals

import djclick as click

from tagging.models import Tag, TaggedItem

@click.group()
def cli():
    """Tagging-extra CLI"""
    pass


@cli.command()
def clean_orphaned_tagged_items():

    click.echo('cleaning orphaned tag assignments')

    qs = TaggedItem.objects.all().prefetch_related(
        'object'
    )

    to_be_deleted = []

    with click.progressbar(qs) as bar:
        for item in bar:
            if not item.object:
                to_be_deleted.append(item.pk)

    # print(to_be_deleted)
    click.echo('{} assignments marked for deletion'.format(len(to_be_deleted)))

    TaggedItem.objects.filter(pk__in=to_be_deleted).delete()
