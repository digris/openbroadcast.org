import os
import sys
import djclick as click

from ...radioplayer.generator import set_radioplayer_metadata


@click.group()
def cli():
    """Radioplayer CLI"""
    pass


@cli.command()
@click.option('media_id', '--media-id', '-m', type=int, required=True)
def now_playing(media_id):
    """
    local data example:
        ./manage.py radioplayer_cli now_playing -m 429607
    """

    from alibrary.models.mediamodels import Media

    content_object = Media.objects.get(pk=media_id)
    set_radioplayer_metadata(content_object)
