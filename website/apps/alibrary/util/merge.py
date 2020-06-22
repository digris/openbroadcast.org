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

    raise NotImplementedError('merging of "{}" objects not implemented.'.format(type(master)))
