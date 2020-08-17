# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from base.models.utils.merge import (
    merge_objects,
    merge_votes,
    merge_relations,
    merge_tags,
)

from ..models import Release, Artist, Label, Media

log = logging.getLogger(__name__)


def merge(master, slaves):

    # log.info('merge objects: {} - {}'.format(master, slaves))

    if isinstance(master, Release):

        # clear relations to prevent duplicates
        for r in slaves:
            r.album_artists.clear()

        merge_votes(master, slaves)
        merge_relations(master, slaves)
        merge_tags(master, slaves)
        master = merge_objects(master, slaves)

        # trigger save to update cache
        for media in master.media_release.all():
            media.save()

        return master

    if isinstance(master, Artist):

        merge_votes(master, slaves)
        merge_relations(master, slaves)
        merge_tags(master, slaves)
        master = merge_objects(master, slaves)

        # trigger save to update cache
        for media in master.media_artist.all():
            media.save()

        master.save()

        return master

    if isinstance(master, Label):

        merge_votes(master, slaves)
        merge_relations(master, slaves)
        merge_tags(master, slaves)
        master = merge_objects(master, slaves)

        master.save()

        return master

    if isinstance(master, Media):

        from alibrary.models import MediaExtraartists

        extra_artists = []

        for m in slaves:
            m.waveforms.all().delete()
            m.formats.all().delete()

            # store extra artists before deleting assignment
            # we need to extract artist and profession to a separate dict, as the 'MediaExtraartists'
            # instances will be deleted in the next step
            extra_artists += [
                {"artist": ea.artist, "profession": ea.profession}
                for ea in MediaExtraartists.objects.filter(media=m)
            ]

            # delete media- and extra artist assignments
            m.media_artists.clear()
            m.extra_artists.clear()

            m.refresh_from_db()

        merge_votes(master, slaves)
        merge_relations(master, slaves)
        merge_tags(master, slaves)
        master = merge_objects(master, slaves)

        # re-attach stored extra artists to master
        for extra_artist in extra_artists:
            MediaExtraartists.objects.get_or_create(
                artist=extra_artist["artist"],
                profession=extra_artist["profession"],
                media=master,
            )

        master.save()

        return master

    raise NotImplementedError('merging of "{}" objects not implemented.'.format(type(master)))
