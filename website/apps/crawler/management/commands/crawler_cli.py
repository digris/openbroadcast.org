#-*- coding: utf-8 -*-

import os
import requests
import djclick as click
from django.db.models import Q
from django.contrib.auth.models import User
from django.conf import settings
from django.core.cache import caches
from django.contrib.contenttypes.models import ContentType

from alibrary.models import Release, Media, Artist, Label, Relation

from ...workflows.musicbrainz import (
    release_fetch_media_mb_ids,
    # metadata crawlers
    artist_crawl_musicbrainz, label_crawl_musicbrainz, release_crawl_musicbrainz,
    media_crawl_musicbrainz,
)

from ...workflows.artwork import obj_crawl_artwork

DEFAULT_LIMIT = 100
MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT', None)


cache = caches['crawler']

@click.group()
def cli():
    """Crawler CLI"""
    pass

@cli.command()
@click.option('id', '--id', type=int, required=False)
def crawl_releases_for_media_mbid(id):
    """Loop through all releases with mb_id - tries to find ids for tracks"""

    qs = Release.objects.filter(relations__service='musicbrainz')

    if id:
        # case if explicit id given
        qs = qs.filter(pk__in=[id])
    else:
        # narrow queryset
        # we have to get the objects *with* relations first and then exclude them from the qs.
        # (other way round is too inefficient)
        _m_qs = Media.objects.all()
        _m_qs_with_mb = Media.objects.filter(relations__service='musicbrainz')
        _m_ids = _m_qs.exclude(pk__in=_m_qs_with_mb).values_list('id', flat=True)

        qs = qs.filter(media_release__pk__in=_m_ids).distinct()


    click.secho('Num. objects to process: {}'.format(qs.count()), fg='green')

    total_mb_ids_added = []
    for obj in qs:
        mb_ids_added = release_fetch_media_mb_ids(obj=obj)
        if mb_ids_added:
            total_mb_ids_added += mb_ids_added

    click.secho('Total mb ids added:    {}'.format(
        len(total_mb_ids_added)
    ), fg='green')


@cli.command()
@click.argument('ct', type=str, nargs=1, required=False)
@click.option('id', '--id', type=int, required=False)
@click.option('cache_for', '--cache', type=int, required=False, default=60 * 10 * 24)
def crawl_musicbrainz(ct, id, cache_for):
    """
    crawls for (secondary) identifiers.
    give content type(s) as argument(s):
    track, artist, release, label
    """

    changes = []

    if ct == 'artist':
        qs = Artist.objects.filter(relations__service='musicbrainz').distinct()
        _crawl_func = artist_crawl_musicbrainz

    if ct == 'label':
        qs = Label.objects.filter(relations__service='musicbrainz').distinct()
        _crawl_func = label_crawl_musicbrainz

    if ct == 'release':
        qs = Release.objects.filter(relations__service='musicbrainz').distinct()
        _crawl_func = release_crawl_musicbrainz

    if ct == 'media':
        qs = Media.objects.filter(relations__service='musicbrainz').distinct()
        _crawl_func = media_crawl_musicbrainz


    click.secho('Num. {} objects to process: {}'.format(ct, qs.count()), fg='green')

    for obj in qs:
        cache_key = 'musicbrainz-{}-{}'.format(ct, obj.pk)
        if cache.get(cache_key):
            click.secho('object recently crawled: {}'.format(obj), bg='yellow', fg='black')
        else:
            _changes = _crawl_func(obj=obj)
            if _changes:
                changes.append(_changes)
            cache.set(cache_key, 1, cache_for)


    ###################################################################
    # summary display
    ###################################################################
    click.secho('#' * 72, fg='green')

    click.secho('Total updated objects:    {}'.format(
        len(changes)
    ), fg='green')

    click.secho('Total updated properties: {}'.format(
        sum([len(c) for c in changes])
    ), fg='green')




@cli.command()
@click.argument('ct', type=str, nargs=1, required=False)
@click.option('id', '--id', type=int, required=False)
@click.option('cache_for', '--cache', type=int, required=False, default=60 * 10 * 24)
def crawl_artwork(ct, id, cache_for):
    """
    crawls for artwork.
    give content type(s) as argument(s):
    track, artist, release, label
    """


    images_added = []

    if ct == 'artist':

        services = [
            'wikidata',
            'discogs',
        ]

        qs = Artist.objects.filter(
            Q(main_image__isnull=True) | Q(main_image=''),
            relations__service__in=services
        ).distinct()

    if ct == 'release':

        services = [
            'musicbrainz',
            'wikidata',
            'discogs',
            'wikipedia',
        ]

        qs = Release.objects.filter(
            #Q(main_image__isnull=True) | Q(main_image=''),
            relations__service__in=services
        ).distinct()

    if ct == 'label':

        services = [
            'wikidata',
            'discogs',
        ]

        qs = Label.objects.filter(
            Q(main_image__isnull=True) | Q(main_image=''),
            relations__service__in=services
        ).distinct()




    click.secho('Num. {} objects to process: {}'.format(ct, qs.count()), fg='green')
    for obj in qs:
        cache_key = 'artwork-{}-{}'.format(ct, obj.pk)
        if cache.get(cache_key):
            click.secho('object recently crawled: {}'.format(obj), bg='yellow', fg='black')
        else:
            image = obj_crawl_artwork(obj=obj, services=services, save=True)
            if image:
                images_added.append(image)
            cache.set(cache_key, 1, cache_for)





    click.secho('#' * 72, fg='green')

    click.secho('Total images added:    {}'.format(
        len(images_added)
    ), fg='green')



























@cli.command()
@click.option('cache_for', '--cache', type=int, required=False, default=60 * 10 * 24)
def crawl_viaf_isni(cache_for):
    """
    crawls viaf database for artist ISNI codes
    """

    qs = Artist.objects.filter(
        Q(isni_code__isnull=True) | Q(isni_code=''),
        relations__service='viaf'
    ).distinct()

    for obj in qs:

        cache_key = 'viaf-isni-{}-{}'.format('artist', obj.pk)

        if cache.get(cache_key):
            click.secho('object recently crawled: {}'.format(obj), bg='yellow', fg='black')

        else:

            url = obj.relations.filter(service='viaf').first().url + '/justlinks.json'
            r = requests.get(url)
            if r.status_code == 200:
                try:
                    data = r.json()
                    isni = data['ISNI'][0]
                    click.secho('got ISNI {} for {}'.format(isni, obj), fg='green')
                    type(obj).objects.filter(pk=obj.pk).update(isni_code=isni)
                except Exception as e:
                    click.secho('unable to get ISNI for {}'.format(obj), fg='red')
                    pass

        cache.set(cache_key, 1, cache_for)
