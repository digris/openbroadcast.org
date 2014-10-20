# -*- coding: utf-8 -*-
import re

from django import template
from django.utils.safestring import mark_safe

from alibrary.models import Daypart, Playlist

register = template.Library()

@register.inclusion_tag('lib/templatetags/video_by_url.html', takes_context=True)
def video_by_url(context, url):

    request = context['request']
    context.update({'video_id': extract_video_id(url)})

    return context




def extract_video_id(video_url):

    m = re.search(r"youtube\.com/.*v=([^&]*)", '%s' % video_url)
    try:
        video_id = m.group(1)
    except Exception, e:
        print e
        video_id  = None

    return video_id