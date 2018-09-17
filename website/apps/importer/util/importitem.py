# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.contenttypes.models import ContentType

from ..models import ImportItem

def get_import_sessions_for_obj(obj):
    """
    returns `Import` instance for object
    (`obj` is media, release, artist or label)
    """

    content_type = ContentType.objects.get_for_model(obj)
    object_id = obj.id

    qs = ImportItem.objects.filter(
        content_type=content_type,
        object_id=object_id
    )

    return [i.import_session for i in qs if i.import_session]
