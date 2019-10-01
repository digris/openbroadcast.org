# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import re

import actstream
from django.db import transaction
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from dajaxice.decorators import dajaxice_register
from django.contrib.auth.decorators import permission_required
import requests
from stdnum import ean
from django.utils.translation import ugettext as _
import urllib
from alibrary.models import Release, Relation, Label, Artist, Media
from base.models.utils.merge import (
    merge_objects,
    merge_votes,
    merge_relations,
    merge_tags,
)
from base.utils.AsciiDammit import asciiDammit

from alibrary.util.api_compare import get_from_provider
from alibrary.util.api_search import discogs_ordered_search


import logging

log = logging.getLogger(__name__)

MUSICBRAINZ_HOST = getattr(settings, "MUSICBRAINZ_HOST", None)
DISCOGS_HOST = getattr(settings, "DISCOGS_HOST", None)


@dajaxice_register
def api_lookup(request, *args, **kwargs):

    # compose lookup by known objects
    item_type = kwargs.get("item_type", None)
    item_id = kwargs.get("item_id", None)
    provider = kwargs.get("provider", None)

    # alternatively, in case we already know the uri, this value is used for the query
    api_url = kwargs.get("api_url", None)

    log.debug("api_lookup: %s - id: %s - provider: %s" % (item_type, item_id, provider))

    try:
        log.debug(provider)
        data = get_from_provider(item_type, item_id, provider, api_url)
        return json.dumps(data, encoding="utf-8")
    except Exception as e:
        log.warning("api_lookup error: %s", e)
        error_message = "Unable to process search request. \r\nPlease check again if the provided URLs are correct."
        return json.dumps({"error": "%s" % error_message}, encoding="utf-8")


@dajaxice_register
def provider_search_query(request, *args, **kwargs):

    item_type = kwargs.get("item_type", None)
    item_id = kwargs.get("item_id", None)
    provider = kwargs.get("provider", None)

    log.debug("type: %s - id: %s - provider: %s" % (item_type, item_id, provider))

    data = {}
    try:
        if item_type == "release" and provider == "discogs":
            item = Release.objects.get(pk=item_id)
            artist_display = item.get_artist_display()
            if artist_display == "Various Artists":
                artist_display = "Various"

            data = {"query": "%s - %s" % (artist_display, item.name)}

        if item_type == "release" and provider == "musicbrainz":
            item = Release.objects.get(pk=item_id)
            data = {
                "query": "%s AND artist:%s" % (item.name, item.get_artist_display())
            }
            # TODO: reason? https://lab.hazelfire.com/issues/1791
            # data = {'query': '%s artist:%s' % (item.name, item.get_artist_display())}

        if item_type == "artist" and provider == "discogs":
            item = Artist.objects.get(pk=item_id)
            data = {"query": "%s" % (item.name)}

        if item_type == "artist" and provider == "musicbrainz":
            item = Artist.objects.get(pk=item_id)
            data = {"query": "%s" % (item.name)}

        if item_type == "media" and provider == "discogs":
            item = Media.objects.get(pk=item_id)
            data = {"query": "%s" % (item.name)}

        if item_type == "media" and provider == "musicbrainz":
            item = Media.objects.get(pk=item_id)
            data = {"query": "%s AND artist:%s" % (item.name, item.artist.name)}

        if item_type == "label" and provider == "discogs":
            item = Label.objects.get(pk=item_id)
            if " " in item.name:
                data = {"query": '"%s"' % (item.name)}
            else:
                data = {"query": "%s" % (item.name)}

        if item_type == "label" and provider == "musicbrainz":
            item = Label.objects.get(pk=item_id)
            data = {"query": "%s" % (item.name)}

        return json.dumps(data)

    except Exception as e:
        log.warning("%s" % e)
        return None


@dajaxice_register
def provider_search(request, *args, **kwargs):

    item_type = kwargs.get("item_type", None)
    item_id = kwargs.get("item_id", None)
    provider = kwargs.get("provider", None)
    query = kwargs.get("query", None)

    # log.debug('query: %s' % (query))

    results = []
    error = None

    if provider == "discogs":

        # query = re.sub('[^A-Za-z0-9 :]+', '', query)
        query = query.replace("(", "")
        query = query.replace(")", "")

        results = discogs_ordered_search(query, item_type)

        query = query.replace('"', "&quot;")

    if provider == "musicbrainz":

        _type = item_type
        if item_type == "media":
            _type = "recording"

        if ean.is_valid(query):
            log.debug("ean barcode detected. switching url composition")
            t_query = query.replace("-", "")
            url = "http://%s/ws/2/%s?query=barcode:%s&fmt=json" % (
                MUSICBRAINZ_HOST,
                _type,
                t_query,
            )
        else:
            # query = re.sub('[^A-Za-z0-9 :]+', '', query)
            t_query = asciiDammit(query)

            """
            escape lucene special characters:
            https://lucene.apache.org/core/4_3_0/queryparser/org/apache/lucene/queryparser/classic/package-summary.html#package_description
            """
            t_query = (
                t_query.replace("!", "\!")
                .replace("+", "\+")
                .replace("-", "\-")
                .replace("~", "\~")
                .replace("*", "\*")
                .replace("?", "\?")
                .replace('"', '\\"')
                .replace("/", "\/")
                .replace("(", "\(")
                .replace(")", "\)")
                .replace("[", "\[")
                .replace("]", "\]")
                .replace(":", "\:")
                .replace("artist\:", "artist:")
            )

            t_query = urllib.quote(t_query)

            url = "http://%s/ws/2/%s?query=%s&fmt=json" % (
                MUSICBRAINZ_HOST,
                _type,
                t_query,
            )

            query = urllib.unquote(t_query)
            query = (
                query.replace("\!", "!")
                .replace("\+", "+")
                .replace("\-", "-")
                .replace("\~", "~")
                .replace("\*", "*")
                .replace("\?", "?")
                .replace('\\"', "")
                .replace("\/", "/")
                .replace("\(", "(")
                .replace("\)", ")")
                .replace("\[", "[")
                .replace("\]", "]")
                .replace("\:", ":")
            )

        log.debug("query url: %s" % (url))
        r = requests.get(url)

        if item_type == "release":
            results = json.loads(r.text)["releases"]
            for result in results:
                result["uri"] = "http://musicbrainz.org/release/%s" % result["id"]
                result["thumb"] = "http://coverartarchive.org/%s/%s" % (
                    item_type,
                    result["id"],
                )

        if item_type == "artist":
            results = json.loads(r.text)["artists"]
            for result in results:
                result["uri"] = "http://musicbrainz.org/artist/%s" % result["id"]
                result["thumb"] = "http://coverartarchive.org/%s/%s" % (
                    item_type,
                    result["id"],
                )

        if item_type == "label":
            results = json.loads(r.text)["labels"]
            for result in results:
                result["uri"] = "http://musicbrainz.org/label/%s" % result["id"]
                result["thumb"] = "http://coverartarchive.org/%s/%s" % (
                    item_type,
                    result["id"],
                )

        if item_type == "media":
            results = json.loads(r.text)["recordings"]
            for result in results:
                result["uri"] = "http://musicbrainz.org/recording/%s" % result["id"]

    return json.dumps({"query": query, "results": results, "error": error})


@dajaxice_register
def provider_update(request, *args, **kwargs):

    item_type = kwargs.get("item_type", None)
    item_id = kwargs.get("item_id", None)
    provider = kwargs.get("provider", None)
    uri = kwargs.get("uri", None)

    log.debug("uri: %s" % (uri))

    item = None
    data = {}
    try:
        if item_type == "release":
            item = Release.objects.get(pk=item_id)

        if item_type == "artist":
            item = Artist.objects.get(pk=item_id)

        if item_type == "label":
            item = Label.objects.get(pk=item_id)

        if item_type == "media":
            item = Media.objects.get(pk=item_id)

        if item and uri:
            rel = Relation(content_object=item, url=uri)
            # disabled save, as this involves heavy issues!
            # rel.save()

        data = {"service": "%s" % rel.service, "url": "%s" % rel.url}

    except Exception as e:
        log.warning("%s" % e)

    return json.dumps(data)


@dajaxice_register
@permission_required("alibrary.merge_media")
def merge_items(request, *args, **kwargs):

    item_type = kwargs.get("item_type", None)
    item_ids = kwargs.get("item_ids", [])
    master_id = kwargs.get("master_id", None)

    slave_items = []
    master_item = None
    data = {"status": None, "error": None}

    if item_type and item_ids and master_id:
        log.debug(
            "merge items - type: %s - ids: %s - master: %s"
            % (item_type, ", ".join(item_ids), master_id)
        )
        try:

            if item_type == "release":

                items = Release.objects.filter(pk__in=item_ids).exclude(
                    pk=int(master_id)
                )
                for item in items:
                    item.album_artists.clear()
                    slave_items.append(item)

                master_item = Release.objects.get(pk=int(master_id))
                if slave_items and master_item:
                    merge_votes(master_item, slave_items)
                    merge_relations(master_item, slave_items)
                    merge_tags(master_item, slave_items)
                    master_item = merge_objects(master_item, slave_items)
                    # needed to clear cache
                    for media in master_item.media_release.all():
                        media.save()
                    data["status"] = True
                else:
                    data["status"] = False
                    data["error"] = "No selection"

            if item_type == "media":

                from alibrary.models import MediaExtraartists

                items = Media.objects.filter(pk__in=item_ids).exclude(pk=int(master_id))

                extra_artists = []

                for item in items:
                    item.waveforms.all().delete()
                    item.formats.all().delete()

                    # store extra artists before deleting assignment
                    # we need to extract artist and profession to a separate dict, as the 'MediaExtraartists'
                    # instances will be deleted in the next step
                    extra_artists += [
                        {"artist": ea.artist, "profession": ea.profession}
                        for ea in MediaExtraartists.objects.filter(media=item)
                    ]

                    # delete media- and extra artist assignments
                    item.media_artists.clear()
                    item.extra_artists.clear()

                    slave_items.append(item)

                master_item = Media.objects.get(pk=int(master_id))
                if slave_items and master_item:
                    merge_votes(master_item, slave_items)
                    merge_relations(master_item, slave_items)
                    merge_tags(master_item, slave_items)
                    merge_objects(master_item, slave_items)

                    # re-attach stored extra artists to master
                    if extra_artists:
                        for extra_artist in extra_artists:
                            MediaExtraartists.objects.get_or_create(
                                artist=extra_artist["artist"],
                                profession=extra_artist["profession"],
                                media=master_item,
                            )

                    master_item.save()
                    data["status"] = True
                else:
                    data["status"] = False
                    data["error"] = "No selection"

            if item_type == "artist":
                items = Artist.objects.filter(pk__in=item_ids).exclude(
                    pk=int(master_id)
                )
                for item in items:
                    slave_items.append(item)

                master_item = Artist.objects.get(pk=int(master_id))
                if slave_items and master_item:
                    merge_votes(master_item, slave_items)
                    merge_relations(master_item, slave_items)
                    merge_tags(master_item, slave_items)
                    merge_objects(master_item, slave_items)
                    master_item.save()
                    # needed to clear cache
                    for media in master_item.media_artist.all():
                        media.save()

                    data["status"] = True
                else:
                    data["status"] = False
                    data["error"] = "No selection"

            if item_type == "label":
                items = Label.objects.filter(pk__in=item_ids).exclude(pk=int(master_id))
                for item in items:
                    slave_items.append(item)

                master_item = Label.objects.get(pk=int(master_id))
                if slave_items and master_item:
                    merge_votes(master_item, slave_items)
                    merge_relations(master_item, slave_items)
                    merge_tags(master_item, slave_items)
                    merge_objects(master_item, slave_items)
                    master_item.save()
                    # needed to clear cache?
                    """
                    for media in master_item.media_release.all():
                        media.save()
                    """
                    data["status"] = True
                else:
                    data["status"] = False
                    data["error"] = "No selection"

            if master_item and data["status"]:
                actstream.action.send(
                    request.user, verb=_("merged to"), target=master_item
                )
                pass

        except Exception as e:
            log.warning("%s" % e)
            data["status"] = False
            data["error"] = "%s" % e

    return json.dumps(data)


@dajaxice_register
@permission_required("alibrary.reassign_media")
def reassign_items(request, *args, **kwargs):

    media_ids = kwargs.get("media_ids", [])
    name = kwargs.get("name", None)
    release_id = kwargs.get("release_id", None)

    if media_ids and (release_id or name):

        log.debug("reassigning items: %s to %s" % ((",").join(media_ids), release_id))

        if release_id:
            r = Release.objects.get(pk=int(release_id))
        else:
            r = Release(name=name.strip())
            r.creator = r.last_editor = request.user
            r.save()

        for id in media_ids:
            m = Media.objects.get(pk=int(id))
            m.release = r
            m.save()

        data = {"status": True, "error": None, "next": r.get_absolute_url()}

    else:

        data = {"status": False, "error": "missing data"}

    return json.dumps(data)
