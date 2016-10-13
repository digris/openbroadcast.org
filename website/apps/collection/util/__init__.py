# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging

from django.contrib.contenttypes.models import ContentType

from ..models import CollectionItem, CollectionMember

def add_to_collection(object, user, collection):

    content_type = ContentType.objects.get_for_model(object)

    collection_item, collection_item_created = CollectionItem.objects.get_or_create(
        object_id=object.pk,
        content_type=content_type
    )

    collection_member, collection_member_created = CollectionMember.objects.get_or_create(
        item=collection_item,
        collection=collection,
        added_by=user
    )

    return collection_member
