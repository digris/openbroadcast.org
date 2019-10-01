# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import djclick as click
from django.conf import settings

MEDIA_ASSET_KEEP_DAYS = getattr(settings, "MEDIA_ASSET_KEEP_DAYS", 60)


@click.group()
def cli():
    """Platform CLI"""
    pass


@cli.command()
def check():
    """Self-check (refactored to checks - not in use anymore)"""
    click.echo("depreciated. use './manage.py check base' instead")


@cli.command()
def delete_orphaned_tags():
    """Delete tags that are not assigned to any objects anymore (e.g. because they were 'merged')."""

    from tagging.models import TaggedItem

    to_delete = []
    tagged_items = TaggedItem.objects.all().nocache()

    with click.progressbar(
        tagged_items, label="Scanning {} tagged items".format(tagged_items.count())
    ) as bar:
        for ti in bar:
            if not ti.object:
                to_delete.append(ti.pk)

    click.echo("Total tagged items:    {}".format(tagged_items.count()))
    click.echo("Orphaned tagged items: {}".format(len(to_delete)))

    TaggedItem.objects.filter(pk__in=to_delete).delete()


@cli.command()
@click.option(
    "--age",
    "-a",
    type=int,
    default=MEDIA_ASSET_KEEP_DAYS,
    help="Clean media assets not accessed for the last {0} days".format(
        MEDIA_ASSET_KEEP_DAYS
    ),
)
def clean_assets(age):
    """Delete (cached) media assets (encoded versions, waveforms) that have nt been accessed for x days."""

    from media_asset.models import Format
    from media_asset.models import Waveform

    format_qs = Format.objects.filter(
        accessed__lte=datetime.now() - timedelta(days=age)
    ).nocache()

    waveform_qs = Waveform.objects.filter(
        accessed__lte=datetime.now() - timedelta(days=age)
    ).nocache()

    with click.progressbar(
        format_qs, label="Deleting {} media format versions".format(format_qs.count())
    ) as bar:
        for item in bar:
            item.delete()

    with click.progressbar(
        waveform_qs, label="Deleting {} waveforms".format(waveform_qs.count())
    ) as bar:
        for item in bar:
            item.delete()


@cli.command()
def reset():
    # TODO: implement reset command
    raise NotImplementedError("reset command not implemented yet")


@cli.command()
def crawl():
    # TODO: implement crawl command
    raise NotImplementedError("crawl command not implemented yet")


@cli.command()
@click.option("--ctype", "-t", "content_types", default=["all"], multiple=True)
def warm_cache(content_types):
    """Warm cache for given types."""
    click.secho("Warming cache for: {}".format(", ".join(content_types)))

    from alibrary.models import Artist

    if "artist" in content_types or "all" in content_types:
        artist_qs = Artist.objects.order_by("-updated").all()

        with click.progressbar(
            artist_qs, label="Warming cache for {} items".format(artist_qs.count())
        ) as bar:
            for item in bar:
                item.get_releases()
                item.get_media()
