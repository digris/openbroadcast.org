# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import collections
import logging
import os
import re
import shutil
import time
from Levenshtein import distance

import requests
from actstream import action
from alibrary.models import NameVariation as ArtistNameVariation
from alibrary.models import (
    Relation,
    Release,
    Artist,
    Media,
    MediaExtraartists,
    Profession,
    ArtistMembership,
    ArtistAlias,
    MediaArtists,
)
from alibrary.util import lookup
from alibrary.util.storage import get_file_from_url
from celery.task import task
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from importer.util.tools import discogs_image_by_url, discogs_id_by_url
from l10n.models import Country

log = logging.getLogger(__name__)

DISCOGS_HOST = getattr(settings, "DISCOGS_HOST", None)
MUSICBRAINZ_HOST = getattr(settings, "MUSICBRAINZ_HOST", None)
MUSICBRAINZ_RATE_LIMIT = getattr(settings, "MUSICBRAINZ_RATE_LIMIT", True)
MEDIA_ROOT = getattr(settings, "MEDIA_ROOT", True)

USE_CELERYD = getattr(settings, "IMORTER_USE_CELERYD", False)

# promt for continuation (does not work with USE_CELERYD = True)
DEBUG_WAIT = False


def clean_filename(filename):
    import unicodedata
    import string

    valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
    cleaned = unicodedata.normalize("NFKD", filename).encode("ASCII", "ignore")
    return "".join(c for c in cleaned if c in valid_chars)


def masterpath_by_uuid(instance, filename):
    filename, extension = os.path.splitext(filename)
    folder = "private/%s/" % (str(instance.uuid).replace("-", "/")[5:])
    filename = "master"
    return os.path.join(
        folder, "%s%s" % (clean_filename(filename).lower(), extension.lower())
    )


class Importer(object):
    def __init__(self, user=None):

        self.mb_completed = []
        self.user = user

    def run(self, obj):

        # from importer.util.tools import discogs_image_by_url, discogs_id_by_url

        it = obj.import_tag
        rt = obj.results_tag

        """
        get import settings
        """

        # media
        name = None
        tracknumber = None
        filename = obj.filename
        alibrary_media_id = None
        mb_track_id = None

        if "name" in it and it["name"]:
            name = it["name"]

        if "media_tracknumber" in rt and rt["media_tracknumber"]:
            tracknumber = rt["media_tracknumber"]

        if not tracknumber:
            if "media_tracknumber" in it and it["media_tracknumber"]:
                tracknumber = it["media_tracknumber"]

        if "alibrary_media_id" in it and it["alibrary_media_id"]:
            alibrary_media_id = it["alibrary_media_id"]

        if "mb_track_id" in it and it["mb_track_id"]:
            mb_track_id = it["mb_track_id"]

        # release
        release = None
        alibrary_release_id = None
        mb_release_id = None
        force_release = False

        if "release" in it and it["release"]:
            release = it["release"]

        if "alibrary_release_id" in it and it["alibrary_release_id"]:
            alibrary_release_id = it["alibrary_release_id"]

        if "mb_release_id" in it and it["mb_release_id"]:
            mb_release_id = it["mb_release_id"]

        if "force_release" in it and it["force_release"]:
            force_release = it["force_release"]

        # artist
        artist = None
        alibrary_artist_id = None
        mb_artist_id = None
        mb_artist_combo_ids = None
        force_artist = False

        if "artist" in it and it["artist"]:
            artist = it["artist"]

        if "alibrary_artist_id" in it and it["alibrary_artist_id"]:
            alibrary_artist_id = it["alibrary_artist_id"]

        if "mb_artist_id" in it and it["mb_artist_id"]:
            mb_artist_id = it["mb_artist_id"]

            # there can be multiple ids split by '/' here
            if "/" in mb_artist_id:
                log.debug("got multiple mb artist ids: {}".format(mb_artist_id))

                url = "http://%s/ws/2/artist/%s/?fmt=json" % (
                    MUSICBRAINZ_HOST,
                    mb_artist_id.split("/")[0],
                )
                log.info("url: %s" % url)
                r = requests.get(url, timeout=5)
                result = r.json()
                log.info(
                    "aquired name for split-artist: {} > {}".format(
                        artist, result["name"]
                    )
                )
                artist = result["name"]

                mb_artist_combo_ids = mb_artist_id.split("/")
                mb_artist_id = mb_artist_id.split("/")[0]

        if "force_artist" in it and it["force_artist"]:
            force_artist = it["force_artist"]

        # label
        label = None
        alibrary_label_id = None
        mb_label_id = None
        force_label = False

        if "label" in it and it["label"]:
            label = it["label"]

        if "alibrary_label_id" in it and it["alibrary_label_id"]:
            alibrary_label_id = it["alibrary_label_id"]

        if "mb_label_id" in it and it["mb_label_id"]:
            mb_label_id = it["mb_label_id"]

        if "force_label" in it and it["force_label"]:
            force_label = it["force_label"]

        if not name:
            name = clean_filename(filename)

        # print '***************************************************************'
        # print '*   import settings                                           *'
        # print '***************************************************************'
        # print '* media *******************************************************'
        # print '  name:                 %s' % name
        # print '  tracknumber:          %s' % tracknumber
        # print '  filename:             %s' % filename
        # print '  alibrary_media_id:    %s' % alibrary_media_id
        # print '  mb_track_id:          %s' % mb_track_id
        # print '* release *****************************************************'
        # print '  release:              %s' % release
        # print '  alibrary_release_id:  %s' % alibrary_release_id
        # print '  mb_release_id:        %s' % mb_release_id
        # print '  force_release:        %s' % force_release
        # print '* artist *****************************************************'
        # print '  artist:              %s' % artist
        # print '  alibrary_artist_id:  %s' % alibrary_artist_id
        # print '  mb_artist_id:        %s' % mb_artist_id
        # print '  force_artist:        %s' % force_artist
        # print '* label *****************************************************'
        # print '  label:              %s' % label
        # print '  alibrary_label_id:  %s' % alibrary_label_id
        # print '  mb_label_id:        %s' % mb_label_id
        # print '  force_label:        %s' % force_label
        # print '***************************************************************'

        """
        create media
        always executed, as duplicates are handled before this step
        """
        m = None
        m_created = False
        log.info("creating media: %s" % name)
        m = Media(name=name)
        m.filename = filename
        if tracknumber:
            m.tracknumber = tracknumber
        m.save()
        m_created = True

        """
        get or create release
        get release by:
         - mb_id
         - internal_id
         - or force creation
        """

        """
        Section to search / create / lookup release information
        """

        r = None
        r_created = False

        # look in imports importitems if release is already here
        # (case where same item is 'forced' several times - so we have to avoid recreation)
        try:
            ctype = ContentType.objects.get(app_label="alibrary", model="release")
            ii_ids = obj.import_session.get_importitem_ids(ctype)
            ir = Release.objects.filter(pk__in=ii_ids, name=release)
        except:
            ir = None

        if ir and ir.count > 0:
            r = ir[0]

        # create release if forced
        if force_release and not r:
            log.info("release, force creation: %s" % release)

            r = Release(name=release)
            r.save()
            r_created = True

        # try to get release by alibrary_id
        if alibrary_release_id and not r:
            # log.debug('release, lookup by alibrary_release_id: %s' % alibrary_release_id)
            try:
                r = Release.objects.get(pk=alibrary_release_id)
                log.debug(
                    "got release: %s by alibrary_release_id: %s"
                    % (r.pk, alibrary_release_id)
                )
            except Exception as e:
                log.debug(
                    "could not get release by alibrary_release_id: %s"
                    % alibrary_release_id
                )

        # try to get release by mb_id
        if mb_release_id and not r:
            log.debug("release, local lookup by mb_release_id: %s" % mb_release_id)
            try:
                lrs = lookup.release_by_mb_id(mb_release_id)
                r = lrs[0]
                log.debug(
                    "got local release: %s by mb_release_id: %s" % (r.pk, mb_release_id)
                )
            except Exception as e:
                log.debug(
                    "could not find local release by mb_release_id: %s" % mb_release_id
                )

        # no luck yet, so create the release
        if not r:
            log.info("no release yet, so create it: %s" % release)
            r = Release(name=release)
            r.creator = self.user
            r.save()
            r_created = True

        # attach item to current import
        if r:
            log.info("release here, add it to importitems: %s" % r)
            if obj.import_session:
                try:
                    ii = obj.import_session.add_importitem(r)
                    log.info("importitem created: %s" % ii)
                except:
                    pass

            # assign
            m.release = r

        """
        Section to search / create / lookup artist information
        """
        a = None
        a_created = False

        # look in imports importitems if artist is already here
        # (case where same item is 'forced' several times - so we have to avoid recreation)
        try:
            ctype = ContentType.objects.get(app_label="alibrary", model="artist")
            ii_ids = obj.import_session.get_importitem_ids(ctype)
            ia = Artist.objects.filter(pk__in=ii_ids, name=artist)
        except:
            ia = None

        if ia and ia.count > 0:
            a = ia[0]

        # create artist if forced
        if force_artist and not a:
            log.info("artist, force creation: %s" % artist)

            a = Artist(name=artist)
            a.save()
            a_created = True

        # try to get artist by alibrary_id
        if alibrary_artist_id and not a:
            # log.debug('artist, lookup by alibrary_artist_id: %s' % alibrary_artist_id)
            try:
                a = Artist.objects.get(pk=alibrary_artist_id)
                log.debug(
                    "got artist: %s by alibrary_artist_id: %s"
                    % (a.pk, alibrary_artist_id)
                )
            except Exception as e:
                # print e
                log.debug(
                    "could not get artist by alibrary_artist_id: %s"
                    % alibrary_artist_id
                )

        # try to get artist by mb_id
        if mb_artist_id and not a:
            log.debug("artist, local lookup by mb_artist_id: %s" % mb_artist_id)
            try:
                las = lookup.artist_by_mb_id(mb_artist_id)
                a = las[0]
                log.debug(
                    "got local artist: %s by mb_artist_id: %s" % (a.pk, mb_artist_id)
                )
            except Exception as e:
                # print e
                log.debug(
                    "could not find local artist by mb_artist_id: %s" % mb_artist_id
                )

        # no luck yet, so create the artist
        if not a:
            log.info("no artist yet, so create it: %s" % artist)
            a = Artist(name=artist)
            a.save()
            a_created = True

        # attach item to current import
        if a:
            log.info("artist here, add it to importitems: %s" % a)
            if obj.import_session:
                ii = obj.import_session.add_importitem(a)
                log.info("importitem created: %s" % ii)

            # assign
            m.artist = a

        # for debugging completion, place here
        # m = self.mb_complete_media(m, mb_track_id)

        # try to complete release metadata
        if r_created:
            if self.user:
                r.creator = self.user
                action.send(r.creator, verb="added", target=r)

            # create mb reference immediately - to avoid db inconsistencies
            if mb_release_id:
                mb_url = "http://musicbrainz.org/release/%s" % mb_release_id

                try:
                    Relation.objects.get(object_id=r.pk, url=mb_url)
                except Relation.DoesNotExist:
                    log.debug("relation not here yet, add it: %s" % mb_url)
                    rel = Relation(content_object=r, url=mb_url)
                    rel.save()

            r = self.mb_complete_release(r, mb_release_id)

        # try to complete artist metadata
        if a_created:
            if self.user:
                a.creator = self.user
                action.send(a.creator, verb="added", target=a)

            # create mb reference immediately - to avoid db inconsistencies
            if mb_artist_id:
                mb_url = "http://musicbrainz.org/artist/%s" % mb_artist_id

                try:
                    Relation.objects.get(object_id=a.pk, url=mb_url)
                except Relation.DoesNotExist:
                    log.debug("relation not here yet, add it: %s" % mb_url)
                    rel = Relation(content_object=a, url=mb_url)
                    rel.save()

            a = self.mb_complete_artist(a, mb_artist_id)

        # try to complete media metadata
        # comes after artist creation to prevent duplicates!
        if m_created:
            if self.user:
                m.creator = self.user
                action.send(m.creator, verb="added", target=m)
            m = self.mb_complete_media(
                m,
                mb_track_id,
                mb_release_id,
                mb_artist_combo_ids,
                excludes=(mb_artist_id,),
            )

        # save assignments
        m.save()

        if obj.import_session:
            obj.import_session.add_importitem(m)

        # add file
        folder = "private/%s/" % (str(m.uuid).replace("-", "/"))
        src = obj.file.path
        filename, extension = os.path.splitext(obj.file.path)
        dst = os.path.join(folder, "master%s" % extension.lower())
        log.debug("source path: %s" % src)
        log.debug("destination path: %s" % dst)
        try:
            log.debug("os.makedirs: %s" % os.path.join(MEDIA_ROOT, folder))
            os.makedirs(os.path.join(MEDIA_ROOT, folder))

            log.debug("os.shutil.copy: %s - %s" % (src, os.path.join(MEDIA_ROOT, dst)))
            shutil.copy(src, os.path.join(MEDIA_ROOT, dst))

            log.debug("set master for pk: %s to %s" % (m.pk, dst))
            m.master = dst
            m.original_filename = obj.filename

            m.save()

        except Exception as e:
            log.warning(
                'unable to create directory "%s": %s'
                % (os.path.join(MEDIA_ROOT, folder), e)
            )

        return m, 1

    """
    method mappers to send to background queue
    """

    def mb_complete_media(
        self, obj, mb_id, mb_release_id, mb_artist_combo_ids=None, excludes=()
    ):

        if USE_CELERYD:
            mb_complete_media_task.delay(
                obj,
                mb_id,
                mb_release_id,
                mb_artist_combo_ids,
                excludes=(),
                user=self.user,
            )
        else:
            mb_complete_media_task(
                obj,
                mb_id,
                mb_release_id,
                mb_artist_combo_ids,
                excludes=(),
                user=self.user,
            )
        return obj

    def mb_complete_release(self, obj, mb_id):

        if USE_CELERYD:
            mb_complete_release_task.delay(obj, mb_id, user=self.user)
        else:
            mb_complete_release_task(obj, mb_id, user=self.user)
        return obj

    def mb_complete_artist(self, obj, mb_id):

        if USE_CELERYD:
            mb_complete_artist_task.delay(obj, mb_id, user=self.user)
        else:
            mb_complete_artist_task(obj, mb_id, user=self.user)
        return obj

    def complete_import_tag(self, obj):

        import_tag = obj.import_tag
        results_musicbrainz = obj.results_musicbrainz
        results_tag = obj.results_tag
        selected_import_tag = import_tag.copy()

        """
        Apply musicbrainz tags if unique
        """
        if results_musicbrainz:
            log.debug("got musicbrainz result -> apply it")

            mb = None

            # try to match by name
            tag_release_name = None
            if "release_name" in results_tag:
                tag_release_name = results_tag["release_name"]

            for res in results_musicbrainz:
                if tag_release_name and "name" in res:
                    result_release_name = res["name"]
                    dist = distance(
                        tag_release_name.lower(), result_release_name.lower()
                    )

                    if dist < 4:
                        mb = res
                        break

            if not mb:
                mb = results_musicbrainz[0]

            # media
            if not "name" in import_tag or not import_tag["name"]:
                import_tag["name"] = mb["media"]["name"]

            if not "mb_track_id" in import_tag or not import_tag["mb_track_id"]:
                import_tag["mb_track_id"] = mb["media"]["mb_id"]

            # release
            if not "release" in import_tag or not import_tag["release"]:
                import_tag["release"] = mb["name"]

            if not "mb_release_id" in import_tag or not import_tag["mb_release_id"]:
                import_tag["mb_release_id"] = mb["mb_id"]

            # artist
            if not "artist" in import_tag or not import_tag["artist"]:
                import_tag["artist"] = mb["artist"]["name"]

            if not "mb_artist_id" in import_tag or not import_tag["mb_artist_id"]:
                import_tag["mb_artist_id"] = mb["artist"]["mb_id"]

        if "artist" in import_tag:
            a = Artist.objects.filter(name=import_tag["artist"])

            # TODO: investigate this condition
            # issue #1876
            # this wrongly assigns a `alibrary_artist_id` in the case the
            # ide/file metadata selection is clicked more than once
            if a.count() > 0:
                import_tag["alibrary_artist_id"] = a[0].pk
                import_tag["alibrary_artist_resource_uri"] = a[0].get_api_url()

        if "release" in import_tag:
            r = Release.objects.filter(name=import_tag["release"])

            # TODO: investigate this condition
            # issue #1876
            # this wrongly assigns a `alibrary_release_id` in the case the
            # id/file metadata selection is clicked more than once
            if r.count() > 0:
                import_tag["alibrary_release_id"] = r[0].pk
                import_tag["alibrary_release_resource_uri"] = r[0].get_api_url()

        # remove musicbrainz & discogs ids in case that assigned by ID3
        if selected_import_tag:
            if not "mb_release_id" in selected_import_tag:
                import_tag.pop("mb_release_id", None)

            if not "mb_artist_id" in selected_import_tag:
                import_tag.pop("mb_artist_id", None)

            if not "mb_track_id" in selected_import_tag:
                import_tag.pop("mb_track_id", None)

            if not "mb_label_id" in selected_import_tag:
                import_tag.pop("mb_label_id", None)

        # clean 'wrong' relations
        # https://lab.hazelfire.com/issues/681
        pop_release = False
        pop_artist = False
        pop_media = False
        if results_musicbrainz:

            if "mb_release_id" in import_tag:
                for result in results_musicbrainz:

                    if (
                        "mb_id" in result
                        and result["mb_id"] == import_tag["mb_release_id"]
                    ):

                        if not result["name"] == import_tag["release"]:
                            pop_release = True

            if "mb_artist_id" in import_tag:
                for result in results_musicbrainz:

                    if (
                        "artist" in result
                        and "mb_id" in result["artist"]
                        and result["artist"]["mb_id"] == import_tag["mb_artist_id"]
                    ):

                        if not result["artist"]["name"] == import_tag["artist"]:
                            pop_artist = True

            if "mb_track_id" in import_tag:
                for result in results_musicbrainz:
                    if (
                        "media" in result
                        and "mb_id" in result["media"]
                        and result["media"]["mb_id"] == import_tag["mb_track_id"]
                    ):
                        if not result["media"]["name"] == import_tag["name"]:
                            pop_media = True

        if pop_release:
            import_tag.pop("mb_release_id", None)
            import_tag.pop("mb_label_id", None)
            import_tag.pop("alibrary_release_id", None)
            import_tag.pop("alibrary_release_resource_uri", None)

        if pop_artist:
            import_tag.pop("mb_artist_id", None)
            import_tag.pop("alibrary_artist_id", None)
            import_tag.pop("alibrary_artist_resource_uri", None)

        if pop_media:
            import_tag.pop("mb_track_id", None)

        return import_tag


"""
task definitions
"""


@task
def mb_complete_media_task(
    obj, mb_id, mb_release_id, mb_artist_combo_ids=None, excludes=(), user=None
):
    log.info("complete media, m: %s | mb_id: %s" % (obj.name, mb_id))

    time.sleep(1.1)

    inc = (
        "artists",
        "url-rels",
        "aliases",
        "tags",
        "recording-rels",
        "artist-rels",
        "work-level-rels",
        "artist-credits",
    )
    url = "http://%s/ws/2/recording/%s/?fmt=json&inc=%s" % (
        MUSICBRAINZ_HOST,
        mb_id,
        "+".join(inc),
    )
    log.debug("API request for: %s" % url)
    r = requests.get(url, timeout=5)
    result = r.json()

    # get release based information (to map track- and disc-number)
    inc = ("recordings",)
    url = "http://%s/ws/2/release/%s/?fmt=json&inc=%s" % (
        MUSICBRAINZ_HOST,
        mb_release_id,
        "+".join(inc),
    )
    log.debug("API request for: %s" % url)
    r = requests.get(url, timeout=5)
    result_release = r.json()

    # loop release recordings, trying to get our track...
    if "media" in result_release:
        disc_index = 0
        media_index = 0
        media_offset = 0
        for disc in result_release["media"]:

            for m in disc["tracks"]:

                x_mb_id = m["recording"]["id"]
                x_pos = m["number"]

                if x_mb_id == mb_id:

                    try:
                        obj.tracknumber = int(media_offset) + int(x_pos)
                    except:
                        pass

                    try:
                        obj.medianumber = int(disc_index)
                    except:
                        pass

                media_index = +1

            disc_index += 1
            media_offset += int(disc["track-count"])

    # if mb_artist_combo_ids and 'artist-credit' in result:
    if "artist-credit" in result and len(result["artist-credit"]) > 1:

        artist_credits = result["artist-credit"]
        last_join_phrase = None
        position = 0
        for credit in artist_credits:
            if "artist" in credit:

                log.info("got creditet artist: {}".format(credit["artist"]))

                time.sleep(0.5)
                c_as = lookup.artist_by_mb_id(credit["artist"]["id"])
                c_a = None

                if len(c_as) < 1:
                    # instance.mb_completed.append(relation['artist']['id'])
                    c_a = Artist(name=credit["artist"]["name"])
                    c_a.creator = user
                    c_a.save()

                    url = "http://musicbrainz.org/artist/%s" % credit["artist"]["id"]
                    rel = Relation(content_object=c_a, url=url)
                    rel.save()

                    if not credit["artist"]["id"] in excludes:
                        if USE_CELERYD:
                            mb_complete_artist_task.delay(
                                c_a, credit["artist"]["id"], user=user
                            )
                        else:
                            mb_complete_artist_task(
                                c_a, credit["artist"]["id"], user=user
                            )

                if len(c_as) == 1:
                    c_a = c_as[0]

                if c_a:
                    MediaArtists.objects.get_or_create(
                        artist=c_a,
                        media=obj,
                        join_phrase=last_join_phrase,
                        position=position,
                    )
                    position += 1

            """
            musicbrainz uses join element _after_ artist, we do it the opposite way
            TODO: eventually change to that structure as well
            """
            if "joinphrase" in credit and len(credit["joinphrase"]) > 0:
                last_join_phrase = credit["joinphrase"].strip()

    if "relations" in result:
        for relation in result["relations"]:

            # map artists
            if "artist" in relation:

                time.sleep(0.5)
                l_as = lookup.artist_by_mb_id(relation["artist"]["id"])
                l_a = None

                if len(l_as) < 1 and relation["artist"]["id"] not in excludes:
                    # instance.mb_completed.append(relation['artist']['id'])
                    l_a = Artist(name=relation["artist"]["name"])
                    l_a.creator = user
                    l_a.save()

                    url = "http://musicbrainz.org/artist/%s" % relation["artist"]["id"]
                    rel = Relation(content_object=l_a, url=url)
                    rel.save()

                    if USE_CELERYD:
                        mb_complete_artist_task.delay(
                            l_a, relation["artist"]["id"], user=user
                        )
                    else:
                        mb_complete_artist_task(
                            l_a, relation["artist"]["id"], user=user
                        )

                if len(l_as) == 1:
                    l_a = l_as[0]

                profession = None
                if "type" in relation:
                    profession, created = Profession.objects.get_or_create(
                        name=relation["type"]
                    )

                if l_a:
                    MediaExtraartists.objects.get_or_create(
                        artist=l_a, media=obj, profession=profession
                    )

    """
    Tags disabled cause of bad quality
    """
    # tags = result.get('tags', ())
    # for tag in tags:
    #    log.debug('got tag: %s' % (tag['name']))
    #    try:
    #        Tag.objects.add_tag(obj, '"%s"' % tag['name'])
    #    except:
    #        pass

    # add mb relation
    if mb_id:
        mb_url = "http://musicbrainz.org/recording/%s" % mb_id
        try:
            Relation.objects.get(object_id=obj.pk, url=mb_url)
        except:
            log.debug("relation not here yet, add it: %s" % mb_url)
            rel = Relation(content_object=obj, url=mb_url)
            rel.save()

    # acousticbrainz musical analysis
    if mb_id:
        url = "http://acousticbrainz.org/{mb_id}/low-level".format(mb_id=mb_id)
        log.debug("API request for: %s" % url)
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            result = r.json()
            try:
                bpm = result["rhythm"]["bpm"]
                log.debug("aquired tempo - {}bpm".format(bpm))
                obj.tempo = float(bpm)
            except Exception as e:
                pass

                # try:
                #     key = result['tonal']['key_key']
                #     scale = result['tonal']['key_scale']
                #     obj.tempo = bpm
                # except:
                #     pass

    return obj


@task
def mb_complete_release_task(obj, mb_id, user=None):
    log.info("complete release, r: %s | mb_id: %s" % (obj.name, mb_id))

    inc = (
        "artists",
        "url-rels",
        "aliases",
        "recordings",
        "tags",
        "recording-rels",
        "work-rels",
        "work-level-rels",
        "artist-credits",
        "labels",
        "label-rels",
        "release-groups",
    )
    url = "http://%s/ws/2/release/%s/?fmt=json&inc=%s" % (
        MUSICBRAINZ_HOST,
        mb_id,
        "+".join(inc),
    )

    log.debug("query url: %s" % url)

    r = requests.get(url, timeout=5)
    result = r.json()

    rg_id = None
    release_group = result.get("release-group", None)
    if release_group:
        rg_id = release_group.get("id", None)

    log.debug("release-group id: %s" % rg_id)

    discogs_url = None
    discogs_master_url = None
    discogs_image = None
    discogs_tags = []
    # try to get relations
    if "relations" in result:
        for relation in result["relations"]:

            if relation["type"] == "discogs":
                log.debug(
                    "got discogs url for release: %s" % relation["url"]["resource"]
                )
                discogs_url = relation["url"]["resource"]

                # obj.save()

            if relation["type"] == "purchase for download":
                log.debug(
                    "got purchase url for release: %s" % relation["url"]["resource"]
                )

                try:
                    Relation.objects.get(
                        object_id=obj.pk, url=relation["url"]["resource"]
                    )
                except:
                    rel = Relation(content_object=obj, url=relation["url"]["resource"])
                    rel.save()

    if rg_id:
        # try to get discogs master url
        inc = ("url-rels",)
        url = "http://%s/ws/2/release-group/%s/?fmt=json&inc=%s" % (
            MUSICBRAINZ_HOST,
            rg_id,
            "+".join(inc),
        )

        r = requests.get(url, timeout=5)
        rg_result = r.json()

        # try to get relations from master
        if "relations" in rg_result:
            for relation in rg_result["relations"]:

                if relation["type"] == "discogs":
                    log.debug(
                        "got discogs master-url for release: %s"
                        % relation["url"]["resource"]
                    )
                    discogs_master_url = relation["url"]["resource"]

                if relation["type"] == "wikipedia":
                    log.debug(
                        "got wikipedia url for release: %s"
                        % relation["url"]["resource"]
                    )

                    try:
                        Relation.objects.get(
                            object_id=obj.pk, url=relation["url"]["resource"]
                        )
                    except:
                        rel = Relation(
                            content_object=obj, url=relation["url"]["resource"]
                        )
                        rel.save()

                if relation["type"] == "lyrics":
                    log.debug(
                        "got lyrics url for release: %s" % relation["url"]["resource"]
                    )

                    try:
                        Relation.objects.get(
                            object_id=obj.pk, url=relation["url"]["resource"]
                        )
                    except:
                        rel = Relation(
                            content_object=obj, url=relation["url"]["resource"]
                        )
                        rel.save()

                if relation["type"] == "allmusic":
                    log.debug(
                        "got allmusic url for release: %s" % relation["url"]["resource"]
                    )

                    try:
                        Relation.objects.get(
                            object_id=obj.pk, url=relation["url"]["resource"]
                        )
                    except:
                        rel = Relation(
                            content_object=obj, url=relation["url"]["resource"]
                        )
                        rel.save()

                if relation["type"] == "review":
                    log.debug(
                        "got review url for release: %s" % relation["url"]["resource"]
                    )

                    try:
                        Relation.objects.get(
                            object_id=obj.pk, url=relation["url"]["resource"]
                        )
                    except:
                        rel = Relation(
                            content_object=obj, url=relation["url"]["resource"]
                        )
                        rel.save()

    if discogs_url:

        try:
            Relation.objects.get(object_id=obj.pk, url=discogs_url)
        except:
            rel = Relation(content_object=obj, url=discogs_url)
            rel.save()

        # try to get image
        try:
            discogs_image = discogs_image_by_url(discogs_url, "resource_url")
            log.debug("discogs image located at: %s" % discogs_image)
        except:
            pass

    if discogs_master_url:

        try:
            Relation.objects.get(object_id=obj.pk, url=discogs_master_url)
        except:
            rel = Relation(content_object=obj, url=discogs_master_url)
            rel.save()

        # try to get image from master
        if not discogs_image:
            try:
                discogs_image = discogs_image_by_url(discogs_master_url, "resource_url")
                log.debug("discogs image located at: %s" % discogs_master_url)
            except:
                pass

    # try to load & assign image
    if discogs_image:
        try:
            img = get_file_from_url(discogs_image)
            obj.main_image = img
            obj.save()
        except:
            log.info("unable to assign discogs image")

    else:
        # try at coverartarchive...
        url = "http://coverartarchive.org/release/%s" % mb_id
        try:
            r = requests.get(url, timeout=5)
            ca_result = r.json()
            ca_url = ca_result["images"][0]["image"]
            img = get_file_from_url(ca_url)
            obj.main_image = img
            obj.save()
        except Exception as e:
            pass

    # try to get some additional information from discogs
    if discogs_url:
        discogs_id = None
        try:
            discogs_id = re.findall(r"\d+", discogs_url)[0]
            log.info("extracted discogs id (release): %s" % discogs_id)
        except:
            pass

        if discogs_id:
            url = "http://%s/releases/%s" % (DISCOGS_HOST, discogs_id)
            r = requests.get(url, timeout=5)

            try:
                dgs_result = r.json()

                styles = dgs_result.get("styles", [])
                for style in styles:
                    log.debug("got style: %s" % style)
                    if not "%s" % style in discogs_tags:
                        discogs_tags.append("%s" % style)

                genres = dgs_result.get("genres", [])
                for genre in genres:
                    log.debug("got genre: %s" % genre)
                    if not "%s" % genre in discogs_tags:
                        discogs_tags.append("%s" % genre)

                notes = dgs_result.get("notes", None)
                if notes:
                    obj.description = notes
            except Exception as e:
                log.warning("unable to get data from discogs: %s" % e)

    if discogs_master_url:
        discogs_id = None
        try:
            discogs_id = re.findall(r"\d+", discogs_master_url)[0]
            log.info("extracted discogs id (master-release): %s" % discogs_id)
        except:
            pass

        if discogs_id:
            url = "http://%s/masters/%s" % (DISCOGS_HOST, discogs_id)
            r = requests.get(url, timeout=5)

            try:
                dgs_result = r.json()

                styles = dgs_result.get("styles", [])
                for style in styles:
                    log.debug("got style: %s" % style)
                    if not "%s" % style in discogs_tags:
                        discogs_tags.append("%s" % style)

                genres = dgs_result.get("genres", [])
                for genre in genres:
                    log.debug("got genre: %s" % genre)
                    if not "%s" % genre in discogs_tags:
                        discogs_tags.append("%s" % genre)

                notes = dgs_result.get("notes", None)
                if notes:
                    obj.description = notes

            except Exception as e:
                log.warning("unable to get data from discogs: %s" % e)

    # adding discogs tags
    obj.d_tags = ",".join(discogs_tags)

    status = result.get("status", None)
    if status:
        log.debug("got status: %s" % status)
        obj.releasestatus = status

    country = result.get("country", None)
    if country:
        log.debug("got country: %s" % country)
        try:
            release_country = Country.objects.filter(iso2_code=country)[0]
            obj.release_country = release_country
        except:
            pass

    date = result.get("date", None)
    if date:
        log.debug("got date: %s" % date)
        # TODO: rework field
        if len(date) == 4:
            date = "%s-00-00" % date
        elif len(date) == 7:
            date = "%s-00" % date
        elif len(date) == 10:
            date = "%s" % date

        re_date = re.compile("^\d{4}-\d{2}-\d{2}$")
        if re_date.match(date) and date != "0000-00-00":
            obj.releasedate_approx = "%s" % date

    asin = result.get("asin", None)
    if asin:
        log.debug("got asin: %s" % asin)
        obj.asin = asin

    barcode = result.get("barcode", None)
    if barcode:
        log.debug("got barcode: %s" % barcode)
        obj.barcode = barcode

    # add mb relation
    # moved to be completed before running mb_complete_* so could be redundant here
    if mb_id:
        mb_url = "http://musicbrainz.org/release/%s" % mb_id
        try:
            Relation.objects.get(object_id=obj.pk, url=mb_url)
        except:
            log.debug("relation not here yet, add it: %s" % mb_url)
            rel = Relation(content_object=obj, url=mb_url)
            rel.save()

    # try to get type
    try:
        obj.releasetype = result["release-group"]["primary-type"].lower()
    except Exception as e:
        log.debug("unable to get releasetype: %s" % e)

    # try to get total tracks
    media_list = result.get("media", None)
    if media_list:
        try:
            totaltracks = 0
            for m in media_list:
                totaltracks += int(m.get("track-count", 0))
            obj.totaltracks = totaltracks
        except:
            pass

    """
    trying to get label information
    """
    label_info = result.get("label-info", None)
    if label_info:
        catalog_number = label_info[0].get("catalog-number", None)
        label = label_info[0].get("label", None)

        # print 'catno: %s' % catalog_number
        # print 'label: %s' % label

        label_name = label.get("name", None)
        label_code = label.get("label-code", None)
        mb_label_id = label.get("id", None)
        # print 'label_name:  %s' % label_name
        # print 'label_code:  %s' % label_code
        # print 'label_mb_id: %s' % mb_label_id

        if catalog_number:
            obj.catalognumber = catalog_number

        l = obj.label
        l_created = False
        if label_name and mb_label_id and not l:
            log.debug("label, lookup by mb_label_id: %s" % mb_label_id)
            try:
                lls = lookup.label_by_mb_id(mb_label_id)
                l = lls[0]
                log.debug("got label: %s by mb_label_id: %s" % (l.pk, mb_label_id))
            except Exception as e:
                log.debug("could not get label by mb_label_id: %s" % mb_label_id)
                log.info("create label with mb_id: %s" % mb_label_id)
                from alibrary.models.labelmodels import Label

                l = Label(name=label_name)
                l_created = True
                l.save()

        if l:
            log.debug("got label, attach it to release")
            obj.label = l

        if l_created and l:
            if user:
                l.creator = user
                action.send(l.creator, verb="added", target=l)

            if USE_CELERYD:
                mb_complete_label_task.delay(l, mb_label_id)
            else:
                mb_complete_label_task(l, mb_label_id)

    obj.save()

    return obj


@task
def mb_complete_artist_task(obj, mb_id, user=None):
    log.info("complete artist, a: %s %s | mb_id: %s" % (obj.name, obj.pk, mb_id))

    lock_key = "complete-{}".format(mb_id)

    if cache.get(lock_key) is not None:

        log.warning("completeion locked for id: {}".format(mb_id))

    else:

        cache.set(lock_key, "lock", 60)

        inc = ("artist-rels", "url-rels", "tags")
        url = "http://%s/ws/2/artist/%s/?fmt=json&inc=%s" % (
            MUSICBRAINZ_HOST,
            mb_id,
            "+".join(inc),
        )

        log.info("url: %s" % url)

        r = requests.get(url, timeout=5)
        result = r.json()

        discogs_url = None
        discogs_image = None

        valid_relations = (
            "wikipedia",
            "allmusic",
            "BBC Music page",
            "social network",
            "official homepage",
            "youtube",
            "myspace",
            "IMDb",
            "wikidata",
            "VIAF",
            "lyrics",
            "last.fm",
            "other databases",
            "fanpage",
        )

        life_span = result.get("life-span", None)
        if life_span:
            date_start = life_span.get("begin", None)
            date_end = life_span.get("end", None)
            log.debug("got lifespan: %s to %s" % (date_start, date_end))
            if date_start:
                if len(date_start) == 4:
                    date_start = "%s-00-00" % date_start
                elif len(date_start) == 7:
                    date_start = "%s-00" % date_start
                elif len(date_start) == 10:
                    date_start = "%s" % date_start
                re_date_start = re.compile("^\d{4}-\d{2}-\d{2}$")
                if re_date_start.match(date_start) and date_start != "0000-00-00":
                    obj.date_start = "%s" % date_start

            if date_end:
                if len(date_end) == 4:
                    date_end = "%s-00-00" % date_end
                elif len(date_end) == 7:
                    date_end = "%s-00" % date_end
                elif len(date_end) == 10:
                    date_end = "%s" % date_end
                re_date_end = re.compile("^\d{4}-\d{2}-\d{2}$")
                if re_date_end.match(date_end) and date_end != "0000-00-00":
                    obj.date_end = "%s" % date_end

        try:
            obj.country = Country.objects.filter(name=result["area"]["name"])[0]
        except Exception as e:
            pass

        # retrieve exact name
        # if 'name' in result:
        #     obj.name = result['name']

        # ipis
        if "ipis" in result:
            try:
                obj.ipi_code = result["ipis"][0]
            except:
                pass

        relations = result.get("relations", ())

        for relation in relations:

            if relation["type"] == "discogs":
                log.debug("got discogs url for artist: %s" % relation["url"])
                discogs_url = relation["url"]["resource"]

            if relation["type"] in valid_relations:
                log.debug(
                    "got %s url for artist: %s" % (relation["type"], relation["url"])
                )

                try:
                    Relation.objects.get(
                        object_id=obj.pk, url=relation["url"]["resource"]
                    )
                except:
                    rel = Relation(content_object=obj, url=relation["url"]["resource"])
                    if relation["type"] == "official homepage":
                        rel.service = "official"

                    rel.save()

            else:
                log.debug("ignore relation type: %s" % relation["type"])

        # loop artist based relations ('band member')
        for relation in relations:

            if (
                relation["type"] == "member of band"
                and relation["direction"] == "backward"
            ):
                # if relation['type'] == 'member of band':
                log.debug("got band member")
                rel_mb_id = relation["artist"]["id"]
                l_as = lookup.artist_by_mb_id(rel_mb_id)
                l_a = None

                if len(l_as) < 1:
                    l_a = Artist(name=relation["artist"]["name"])
                    l_a.creator = user
                    l_a.save()

                    if USE_CELERYD:
                        mb_complete_artist_task.delay(l_a, rel_mb_id, user=user)
                    else:
                        mb_complete_artist_task(l_a, rel_mb_id, user=user)

                    mb_url = "http://musicbrainz.org/artist/%s" % rel_mb_id
                    rel = Relation(content_object=l_a, url=mb_url)
                    rel.save()

                if len(l_as) == 1:
                    l_a = l_as[0]

                if l_a:
                    if relation["direction"] == "backward":
                        ArtistMembership.objects.get_or_create(parent=obj, child=l_a)
                    if relation["direction"] == "forward":
                        ArtistMembership.objects.get_or_create(parent=l_a, child=obj)

        if discogs_url:

            try:
                Relation.objects.get(object_id=obj.pk, url=discogs_url)
            except:
                rel = Relation(content_object=obj, url=discogs_url)
                rel.save()

            # try to get image
            try:
                discogs_image = discogs_image_by_url(discogs_url, "resource_url")
                log.debug("discogs image located at: %s" % discogs_image)
            except:
                pass

        # try to load & assign image
        if discogs_image:
            try:
                img = get_file_from_url(discogs_image)
                obj.main_image = img
                obj.save()
            except:
                log.info("unable to assign discogs image")

        if discogs_url:

            discogs_id = None
            try:
                # TODO: not sure if always working
                discogs_id = discogs_id_by_url(discogs_url)
                log.info("extracted discogs id: %s" % discogs_id)
            except:
                pass

            if discogs_id:
                url = "http://%s/artists/%s" % (DISCOGS_HOST, discogs_id)
                r = requests.get(url, timeout=5)

                try:
                    dgs_result = r.json()
                    profile = dgs_result.get("profile", None)
                    if profile:
                        obj.biography = profile

                    realname = dgs_result.get("realname", None)
                    if realname:
                        obj.real_name = realname

                    namevariations = dgs_result.get("namevariations", None)
                    if namevariations:
                        for namevariation in namevariations:
                            # log.debug(u'got namevariation: %s' % namevariation)
                            ArtistNameVariation.objects.get_or_create(
                                name=namevariation[0:245], artist=obj
                            )

                    """
                    verry hackish part here, just as proof-of-concept
                    """
                    aliases = dgs_result.get("aliases", ())
                    aliases = []
                    for alias in aliases:
                        try:
                            log.debug("got alias: %s" % alias["name"])
                            # TODO: improve! handle duplicates!
                            time.sleep(1.1)
                            r = requests.get(alias["resource_url"], timeout=5)
                            aa_result = r.json()
                            aa_discogs_url = aa_result.get("uri", None)
                            aa_name = aa_result.get("name", None)
                            aa_profile = aa_result.get("profile", None)
                            if aa_discogs_url and aa_name:

                                l_as = lookup.artist_by_relation_url(aa_discogs_url)
                                l_a = None

                                if len(l_as) < 1:
                                    l_a = Artist(name=aa_name, biography=aa_profile)
                                    l_a.creator = user
                                    l_a.save()

                                    rel = Relation(
                                        content_object=l_a, url=aa_discogs_url
                                    )
                                    rel.save()

                                if len(l_as) == 1:
                                    l_a = l_as[0]

                                if l_a:
                                    ArtistAlias.objects.get_or_create(
                                        parent=obj, child=l_a
                                    )
                        except:
                            pass

                    """
                    verry hackish part here, just as proof-of-concept
                    """
                    members = dgs_result.get("members", ())
                    members = []  # just temporary disabled
                    for member in members:
                        try:
                            log.debug("got member: %s" % member["name"])
                            # TODO: improve! handle duplicates!
                            time.sleep(1.1)
                            r = requests.get(member["resource_url"], timeout=5)
                            ma_result = r.json()
                            ma_discogs_url = ma_result.get("uri", None)
                            ma_name = ma_result.get("name", None)
                            ma_profile = ma_result.get("profile", None)
                            if ma_discogs_url and ma_name:

                                l_as = lookup.artist_by_relation_url(ma_discogs_url)
                                l_a = None

                                if len(l_as) < 1:
                                    l_a = Artist(name=ma_name, biography=ma_profile)
                                    l_a.creator = user
                                    l_a.save()

                                    rel = Relation(
                                        content_object=l_a, url=ma_discogs_url
                                    )
                                    rel.save()

                                if len(l_as) == 1:
                                    l_a = l_as[0]

                                if l_a:
                                    ArtistMembership.objects.get_or_create(
                                        parent=obj, child=l_a
                                    )

                        except:
                            pass

                except:
                    pass

        type = result.get("type", None)
        if type:
            # log.debug('got type: %s' % (type))
            obj.type = type

        disambiguation = result.get("disambiguation", None)
        if disambiguation:
            # log.debug('got disambiguation: %s' % (disambiguation))
            obj.disambiguation = disambiguation

        # add mb relation
        # moved to be completed before running mb_complete_* so could be redundant here
        if mb_id:
            mb_url = "http://musicbrainz.org/artist/%s" % mb_id
            try:
                Relation.objects.get(object_id=obj.pk, url=mb_url)
            except:
                log.debug("relation not here yet, add it: %s" % mb_url)
                rel = Relation(content_object=obj, url=mb_url)
                rel.save()

            obj.save()

        cache.delete(lock_key)

    return obj


@task
def mb_complete_label_task(obj, mb_id, user=None):
    log.info("complete label, mb_id: %s" % mb_id)

    inc = ("url-rels", "tags", "aliases")
    url = "http://%s/ws/2/label/%s/?fmt=json&inc=%s" % (
        MUSICBRAINZ_HOST,
        mb_id,
        "+".join(inc),
    )

    log.info("url: %s" % url)

    r = requests.get(url, timeout=5)
    result = r.json()

    discogs_url = None
    discogs_image = None

    valid_relations = (
        "wikipedia",
        "allmusic",
        "BBC Music page",
        "social network",
        "official homepage",
        "youtube",
        "myspace",
        "wikidata",
        "official site",
    )

    relations = result.get("relations", ())

    for relation in relations:

        if relation["type"] == "discogs":
            log.debug("got discogs url for label: %s" % relation["url"]["resource"])
            discogs_url = relation["url"]["resource"]

        if relation["type"] in valid_relations:

            log.debug(
                "got %s url for label: %s"
                % (relation["type"], relation["url"]["resource"])
            )

            try:
                Relation.objects.get(object_id=obj.pk, url=relation["url"]["resource"])
            except:
                rel = Relation(content_object=obj, url=relation["url"]["resource"])

                if relation["type"] == "official homepage":
                    rel.service = "official"

                rel.save()

        else:
            log.debug("ignore relation type: %s" % relation["type"])

    if discogs_url:

        try:
            Relation.objects.get(object_id=obj.pk, url=discogs_url)
        except:
            rel = Relation(content_object=obj, url=discogs_url)
            rel.save()

        # try to get image
        try:
            discogs_image = discogs_image_by_url(discogs_url, "resource_url")
            log.debug("discogs image located at: %s" % discogs_image)
        except:
            pass

    # try to load & assign image
    if discogs_image:
        try:
            img = get_file_from_url(discogs_image)
            obj.main_image = img
            obj.save()
        except:
            log.info("unable to assign discogs image")

    if discogs_url:

        discogs_id = None
        try:
            # TODO: not sure if always working
            discogs_id = discogs_id_by_url(discogs_url)
            log.info("extracted discogs id: %s" % discogs_id)
        except:
            pass

        if discogs_id:
            url = "http://%s/labels/%s" % (DISCOGS_HOST, discogs_id)

            log.debug("url: %s" % url)
            r = requests.get(url, timeout=5)

            try:
                dgs_result = r.json()
                profile = dgs_result.get("profile", None)
                if profile:
                    obj.description = profile
                contact_info = dgs_result.get("contact_info", None)
                if contact_info:
                    obj.address = contact_info

            except Exception as e:
                log.info("unable to get discogs data: %s" % e)

    # https://lab.hazelfire.com/issues/927
    # type = result.get('type', None)
    # if type:
    #     log.debug('got type: %s' % (type))
    #     obj.type = type

    times = result.get("life-span", None)
    if times:
        log.debug("got times: %s" % times)
        date_start = times["begin"] if "begin" in times else None
        date_end = times["end"] if "begin" in times else None
        log.debug("date_start: %s" % date_start)
        log.debug("date_end: %s" % date_end)

        if date_start:
            if len(date_start) == 4:
                date = "%s-00-00" % date_start
            elif len(date_start) == 7:
                date = "%s-00" % date_start
            elif len(date_start) == 10:
                date = "%s" % date_start

            re_date = re.compile("^\d{4}-\d{2}-\d{2}$")
            if re_date.match(date) and date != "0000-00-00":
                obj.date_start = "%s" % date

        if date_end:
            if len(date_end) == 4:
                date = "%s-00-00" % date_end
            elif len(date_end) == 7:
                date = "%s-00" % date_end
            elif len(date_end) == 10:
                date = "%s" % date_end

            re_date = re.compile("^\d{4}-\d{2}-\d{2}$")
            if re_date.match(date) and date != "0000-00-00":
                obj.date_end = "%s" % date

    labelcode = result.get("label-code", None)
    if labelcode:
        log.debug("got labelcode: %s" % labelcode)
        obj.labelcode = labelcode

    disambiguation = result.get("disambiguation", None)
    if disambiguation:
        log.debug("got disambiguation: %s" % disambiguation)
        obj.disambiguation = disambiguation

    country = result.get("country", None)
    if country:
        log.debug("got country: %s" % country)
        try:
            country = Country.objects.filter(iso2_code=country)[0]
            obj.country = country
        except:
            pass

    if mb_id:
        mb_url = "http://musicbrainz.org/label/%s" % mb_id
        try:
            Relation.objects.get(object_id=obj.pk, url=mb_url)
        except:
            log.debug("relation not here yet, add it: %s" % mb_url)
            rel = Relation(content_object=obj, url=mb_url)
            rel.save()

    obj.save()

    return obj
