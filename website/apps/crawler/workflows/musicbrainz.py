# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import re
import requests
from django.conf import settings

from l10n.models import Country
from alibrary.models import Relation
from alibrary.util.relations import uuid_by_url, uuid_by_object, get_service_by_url

log = logging.getLogger(__name__)

MUSICBRAINZ_HOST = getattr(settings, "MUSICBRAINZ_HOST")


MB_RELATION_USE_SERVICES = [
    "IMDb",
    "VIAF",
    "official homepage",
    "discogs",
    "social network",
    "wikipedia",
    "youtube",
    "wikidata",
]


def unify_name(text):
    """
    unify strings for matching - as different conventions/styles exist
    """
    _map = (("’", "'"),)

    for c in _map:
        text = text.replace(c[0], c[1])

    return text


def strip_http(url):

    _map = (("https://", ""), ("http://", ""), ("//", ""))

    for c in _map:
        url = url.replace(c[0], c[1])

    return url


def format_approx_date(approx_date):

    if len(approx_date) == 4:
        approx_date = "{}-00-00".format(approx_date)
    elif len(approx_date) == 7:
        approx_date = "{}-00".format(approx_date)
    elif len(approx_date) == 10:
        approx_date = "{}".format(approx_date)

    re_date_start = re.compile("^\d{4}-\d{2}-\d{2}$")

    if re_date_start.match(approx_date) and approx_date != "0000-00-00":
        return "{}".format(approx_date)


def release_fetch_media_mb_ids(obj):
    """
    We have the situation that often *Releases* have an `mb_id` assigned (through manual editing process
    or when assigned during import) - but not the containing Media items.
     - selects all Releases with a `mb_id` containing Tracks without `mb_id`.
     - for every track - if `tracknumber` and `name` are equal - the `mb_id` is added as a Relation
    """

    mb_id = uuid_by_object(obj, service="musicbrainz")

    mb_ids_added = []

    log.debug("processing: {} - id:{} - mb_id:{}".format(obj, obj.pk, mb_id))

    # get media objects without musicbrainz relation
    qs_media = obj.media_release.exclude(relations__service="musicbrainz")

    if not qs_media.exists():
        log.debug("no media objects without mb relation")
        return
    else:
        log.debug("{} media objects without mb relation".format(qs_media.count()))

        # load release + relations from mb api
        url = "http://{host}/ws/2/release/{mb_id}/?fmt=json&inc=recordings".format(
            host=MUSICBRAINZ_HOST, mb_id=mb_id
        )

        try:
            r = requests.get(url)
            _data = r.json()
            log.debug("successfully loaded data from {}".format(url))
        except Exception as e:
            log.warning("unable to load data from {}".format(url))
            return

        if not "media" in _data:
            log.warning("unable to load media {}".format(url))
            return

        # map tracknumbers from lp format A1, A2, B1, B2 etc to 1, 2, 3, 4 ...
        try:
            if _data["media"][0]["tracks"][0]["number"][0:1] == "A":
                for media in _data["media"]:
                    _track_number = 1
                    for track in media["tracks"]:
                        track["number"] = _track_number
                        _track_number += 1
        except (IndexError, KeyError):
            pass

        # map tracknumbers for multi-disc releases
        _tracks = {}
        for m in _data["media"]:
            for t in m["tracks"]:
                try:
                    t_no = int(t["number"]) + m["track-offset"]
                    _tracks[t_no] = t
                except ValueError as e:
                    log.warning(
                        'unable to map tracknumber "{}" - {}'.format(t["number"], e)
                    )

        for m in qs_media:

            log.debug("looking up results for #{} - {}".format(m.tracknumber, m))

            try:
                _track = _tracks[m.tracknumber]
            except KeyError as e:
                return

            log.debug(
                "track from results #{} - {}".format(m.tracknumber, _track["title"])
            )

            # check if titles match
            if unify_name(m.name).lower() == unify_name(_track["title"]).lower():
                log.info("got id for match: {}".format(_track["recording"]["id"]))
                mb_recording_id = _track["recording"]["id"]
                # add mb relation
                if mb_recording_id:
                    mb_url = "http://musicbrainz.org/recording/{mb_id}".format(
                        mb_id=mb_recording_id
                    )
                    try:
                        rel = Relation.objects.get(object_id=m.pk, url=mb_url)
                    except Relation.DoesNotExist as e:
                        log.debug("relation not here yet, so add it: {}".format(mb_url))
                        rel = Relation(content_object=m, url=mb_url)
                        rel.save()

                    mb_ids_added.append(mb_recording_id)

            else:
                log.info('no match: "{}" <> "{}"'.format(m.name, _track["title"]))

    return mb_ids_added


#######################################################################
# musicbrainz crawling
#######################################################################


class MBCrawler(object):
    """
    generic musicbrainz crawler
     - implements loading data from api
     - implements crawling of relations a.k.a. urls
     - implements flow
    """

    mb_api_inc = []
    mb_ctype = None

    def __init__(self, obj):
        self.obj = obj
        self.mb_id = uuid_by_object(obj, service="musicbrainz")

        log.debug(
            "crawling metadata: {} - id:{} - mb_id:{}".format(obj, obj.pk, self.mb_id)
        )

        self._data = None
        self._changes = {}
        self._data = self.load_data_from_api()

    def load_data_from_api(self):
        """
        load data from mb service
        """

        if not self.mb_id:
            return {}

        url = "http://{host}/ws/2/{mb_ctype}/{mb_id}/?fmt=json&inc={inc}".format(
            host=MUSICBRAINZ_HOST,
            mb_id=self.mb_id,
            mb_ctype=self.mb_ctype,
            inc="+".join(self.api_inc),
        )

        log.debug("load data from: {}".format(url))

        try:
            r = requests.get(url)
        except Exception as e:
            log.warning("unable to load data from {}".format(url))
            return {}

        if not r.status_code == 200:
            log.warning("unable to load data: {} - {}".format(r.status_code, url))
            return {}

        return r.json()

    ###################################################################
    # direct field mappings
    # to be defined in type specific crawler
    ###################################################################
    def update_fields(self):
        raise NotImplementedError("implement on derived class")

    def update_relations(self):
        """
        relation mappings (urls)
        """

        relations = self._data.get("relations")
        if relations:

            _relation_qs = self.obj.relations.all()
            _relation_urls = [strip_http(r.url) for r in _relation_qs]

            for relation in [r for r in relations if "url" in r]:
                _url = relation["url"]["resource"]
                if relation["type"] == "official homepage":
                    _service = "official"
                else:
                    _service = get_service_by_url(_url)

                if (
                    relation["type"] in MB_RELATION_USE_SERVICES
                    and not strip_http(_url) in _relation_urls
                ):
                    rel = Relation(content_object=self.obj, url=_url, service=_service)
                    rel.save()

                    if not "relations" in self._changes:
                        self._changes["relations"] = []

                    self._changes["relations"].append(_url)

    def run(self):
        """
        execute default sequence
        """
        # self.load_data_from_api()
        self.update_fields()
        self.update_relations()

        if self._changes:
            log.info("apply changes on {}: {}".format(self.obj, self._changes))
            return self._changes
        else:
            log.debug("no changes for {}".format(self.obj))


class MBArtistCrawler(MBCrawler):
    """
    crawl artist metadata
     - ipi_code
     - isni_code
     - type
     - country
     - date_start
     - date_end
    """

    mb_ctype = "artist"
    api_inc = ["url-rels", "artist-rels"]

    ###################################################################
    # direct field mappings
    ###################################################################
    def update_fields(self):

        if not self.obj.ipi_code:
            try:
                self._changes["ipi_code"] = self._data["ipis"][0]
            except (IndexError, KeyError, AttributeError):
                pass

        if not self.obj.isni_code:
            try:
                self._changes["isni_code"] = self._data["isnis"][0]
            except (IndexError, KeyError, AttributeError):
                pass

        if not self.obj.type:
            try:
                self._changes["type"] = self._data["type"].lower()
            except (IndexError, KeyError, AttributeError):
                pass

        if not self.obj.country:
            try:
                country_code = self._data["country"]
                self._changes["country"] = Country.objects.get(iso2_code=country_code)
            except (IndexError, KeyError, AttributeError, Country.DoesNotExist):
                pass

        if not self.obj.date_start:
            try:
                date_start = self._data["life-span"]["begin"]
                if date_start:
                    self._changes["date_start"] = format_approx_date(date_start)
            except (IndexError, KeyError, AttributeError):
                pass

        if not self.obj.date_end:
            try:
                date_end = self._data["life-span"]["end"]
                if date_end:
                    self._changes["date_end"] = format_approx_date(date_end)
            except (IndexError, KeyError, AttributeError):
                pass

        # update instance fields
        if self._changes:
            type(self.obj).objects.filter(pk=self.obj.pk).update(**self._changes)


class MBLabelCrawler(MBCrawler):
    """
    crawl label metadata
     - ipi_code
     - isni_code
     - country
     - date_start
     - date_end
     - labelcode
    """

    mb_ctype = "label"
    api_inc = ["url-rels", "label-rels"]

    ###################################################################
    # direct field mappings
    ###################################################################
    def update_fields(self):

        if not self.obj.ipi_code:
            try:
                self._changes["ipi_code"] = self._data["ipis"][0]
            except (IndexError, KeyError, AttributeError):
                pass

        if not self.obj.isni_code:
            try:
                self._changes["isni_code"] = self._data["isnis"][0]
            except (IndexError, KeyError, AttributeError):
                pass

        if not self.obj.country:
            try:
                country_code = self._data["country"]
                self._changes["country"] = Country.objects.get(iso2_code=country_code)
            except (IndexError, KeyError, AttributeError, Country.DoesNotExist):
                pass

        if not self.obj.date_start:
            try:
                date_start = self._data["life-span"]["begin"]
                if date_start:
                    self._changes["date_start"] = format_approx_date(date_start)
            except (IndexError, KeyError, AttributeError):
                pass

        if not self.obj.date_end:
            try:
                date_end = self._data["life-span"]["end"]
                if date_end:
                    self._changes["date_end"] = format_approx_date(date_end)
            except (IndexError, KeyError, AttributeError):
                pass

        if not self.obj.labelcode:
            try:
                self._changes["labelcode"] = "{}".format(self._data["label-code"])
            except (IndexError, KeyError, AttributeError):
                pass

        # update instance fields
        if self._changes:
            type(self.obj).objects.filter(pk=self.obj.pk).update(**self._changes)


class MBReleaseCrawler(MBCrawler):
    """
    crawl label metadata
     - country_code
     - releasedate_approx
     - barcode
    """

    mb_ctype = "release"
    api_inc = ["url-rels"]

    ###################################################################
    # direct field mappings
    ###################################################################
    def update_fields(self):

        if not self.obj.release_country:
            try:
                country_code = self._data["country"]
                self._changes["release_country"] = Country.objects.get(
                    iso2_code=country_code
                )
            except (IndexError, KeyError, AttributeError, Country.DoesNotExist):
                pass

        if not self.obj.releasedate_approx:
            try:
                releasedate = self._data["date"]
                if releasedate:
                    self._changes["releasedate_approx"] = format_approx_date(
                        releasedate
                    )
            except (IndexError, KeyError, AttributeError):
                pass

        if not self.obj.barcode:
            try:
                if self._data["barcode"]:
                    self._changes["barcode"] = self._data["barcode"]
            except (IndexError, KeyError, AttributeError):
                pass

        # update instance fields
        if self._changes:
            type(self.obj).objects.filter(pk=self.obj.pk).update(**self._changes)


class MBMediaCrawler(MBCrawler):
    """
    crawl label metadata
     - isrc
    """

    mb_ctype = "recording"
    api_inc = ["url-rels", "isrcs"]

    ###################################################################
    # direct field mappings
    ###################################################################
    def update_fields(self):

        if not self.obj.isrc:
            try:
                self._changes["isrc"] = self._data["isrcs"][0]
            except (IndexError, KeyError, AttributeError, TypeError):
                pass

        # update instance fields
        if self._changes:
            type(self.obj).objects.filter(pk=self.obj.pk).update(**self._changes)


#######################################################################
# 'shortcuts' for outside use
#######################################################################
def artist_crawl_musicbrainz(obj):
    c = MBArtistCrawler(obj)
    return c.run()


def label_crawl_musicbrainz(obj):
    c = MBLabelCrawler(obj)
    return c.run()


def release_crawl_musicbrainz(obj):
    c = MBReleaseCrawler(obj)
    return c.run()


def media_crawl_musicbrainz(obj):
    c = MBMediaCrawler(obj)
    return c.run()
