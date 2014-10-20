# -*- coding: utf-8 -*-
import re

from django import template
from django.utils.safestring import mark_safe

from alibrary.models import Daypart, Playlist

register = template.Library()

@register.filter
def download_url(obj, format, version):
    return obj.get_download_url(format, version)


@register.filter
def quality_indicator(obj):
    return obj.get_media_indicator()

@register.assignment_tag(takes_context=True)
def transform_status(context, obj, target_type):
    return obj.get_transform_status(target_type)


@register.filter
def parse_cuepoints(text):
    
    p = re.compile("(?P<time>[\d]{1,2}:[\d]{2})");
    text = re.sub(p, format_cuelinks, text)

    return mark_safe(text)


def format_cuelinks(m):

    t = m.group(0)
    s = sum(int(x) * 60 ** i for i,x in enumerate(reversed(t.split(":"))))

    str = '<a class="cuepoint" href="#%s">%s</a>' % (s, t)
    print m.group(0)
    return str



@register.inclusion_tag('alibrary/templatetags/playlists_inline.html', takes_context=True)
def playlists_inline(context):
    #context.update({'foo': '...'})
    
    request = context['request']
    playlist = None
    try:
        playlist = Playlist.objects.filter(user=request.user, is_current=True)[0]
    except:
        pass
    context.update({'current_playlist': playlist})
    
    return context

@register.inclusion_tag('alibrary/templatetags/dayparts_inline.html', takes_context=True)
def dayparts_inline(context, object):
    context.update({'object': object})
    return context

@register.inclusion_tag('alibrary/templatetags/dayparts_visual.html', takes_context=True)
def dayparts_visual(context, object):
    context.update({'object': object})
    context.update({'object_dayparts': object.dayparts.all()})
    context.update({'available_dayparts': Daypart.objects.active().order_by('day')})
    return context

@register.inclusion_tag('alibrary/templatetags/dayparts_grid.html', takes_context=True)
def dayparts_grid(context, object):
    context.update({'object': object})
    context.update({'object_dayparts': object.dayparts.all()})
    context.update({'available_dayparts': Daypart.objects.active().order_by('day', 'time_start')})
    return context

@register.inclusion_tag('alibrary/templatetags/m2m_inline.html', takes_context=True)
def m2m_inline(context, items):
    context.update({'items': items})
    return context

@register.inclusion_tag('alibrary/templatetags/relations_inline.html', takes_context=True)
def relations_inline(context, object):
    context.update({'object': object})
    return context

@register.inclusion_tag('alibrary/templatetags/relations_inline.html', takes_context=True)
def all_relations_inline(context, object):
    context.update({'object': object, 'include_generic': True})
    return context
