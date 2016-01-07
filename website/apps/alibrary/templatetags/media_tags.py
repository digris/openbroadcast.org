# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import template
from django.contrib.contenttypes.models import ContentType
from alibrary.models import Playlist, PlaylistItem
from django.db.models import Q

register = template.Library()

@register.assignment_tag
def appearance_for_media(media, include_private=False, user=None):

    pis = PlaylistItem.objects.filter(
        object_id=media.pk,
        content_type=ContentType.objects.get_for_model(media)
    )

    qs = Playlist.objects.filter(items__in=pis)

    if user and user.is_authenticated():
        qs = qs.exclude(
            Q(type='other') | (Q(type='basket') & ~Q(user=user)),
        )
    elif include_private:
        qs = qs.exclude(type='other')
    else:
        qs = qs.exclude(type__in=['other', 'basket'])

    return qs.order_by('-type', '-created',).nocache().distinct()
