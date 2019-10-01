# -*- coding: utf-8 -*-

import djclick as click

from tagging.models import Tag, TaggedItem


@click.group()
def cli():
    """Tagging-extra CLI"""
    pass


@cli.command()
def clean_orphaned_tagged_items():
    """
    usage:

        ./manage.py tagging_extra_cli clean_orphaned_tagged_items
    """

    click.echo(u"cleaning orphaned tag assignments")

    qs = TaggedItem.objects.all().prefetch_related("object")

    to_be_deleted = []

    with click.progressbar(qs) as bar:
        for item in bar:
            if not item.object:
                to_be_deleted.append(item.pk)

    # print(to_be_deleted)
    click.echo(u"{} assignments marked for deletion".format(len(to_be_deleted)))

    TaggedItem.objects.filter(pk__in=to_be_deleted).delete()
