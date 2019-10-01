# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import logging

from django.dispatch.dispatcher import receiver

from importer.signals import importitem_created
from .models import Collection
from .util import add_to_collection

log = logging.getLogger(__name__)

@receiver(importitem_created)
def add_importitem_to_collection(sender, **kwargs):

    try:

        content_object = kwargs.get('content_object')
        user = kwargs.get('user')
        collection_name = kwargs.get('collection_name', 'Contributions')

        log.debug('adding "{}" to collection "{}" (by {})'.format(
            content_object, collection_name, user
        ))

        collection, collection_created = Collection.objects.get_or_create(
            name=collection_name,
            owner=user
        )

        add_to_collection(object=content_object, user=user, collection=collection)

    except Exception as e:
        log.debug('unable to add to collection. {}'.format(e))


