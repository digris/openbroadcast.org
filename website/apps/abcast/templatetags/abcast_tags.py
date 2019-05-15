# -*- coding: utf-8 -*-
from django import template
from abcast.models import Channel

register = template.Library()

@register.inclusion_tag('abcast/templatetags/on_air_inline.html', takes_context=True)
def on_air_inline(context, channel_id=None):

    if not channel_id:
        channel_id = 1

    channel = Channel.objects.get(pk=channel_id)

    context.update({'channel': channel})
    return context

@register.inclusion_tag('abcast/templatetags/on_air_inline_full.html', takes_context=True)
def on_air_inline_full(context, channel_id=None):

    if not channel_id:
        channel_id = 1

    channel = Channel.objects.get(pk=channel_id)

    context.update({'channel': channel})
    return context
