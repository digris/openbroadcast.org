# -*- coding: utf-8 -*-
import re
from django import template

register = template.Library()

@register.inclusion_tag('base/templatetags/video_by_url.html', takes_context=True)
def video_by_url(context, url):
    context.update({'video_id': extract_video_id(url)})
    return context

def extract_video_id(video_url):
    m = re.search(r"youtube\.com/.*v=([^&]*)", '%s' % video_url)
    try:
        video_id = m.group(1)
    except Exception as e:
        video_id  = None

    return video_id
