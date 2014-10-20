# -*- coding: utf-8 -*-
from django import template
from statistics.util import PlatformStatistics

register = template.Library()

@register.inclusion_tag('statistics/templatetags/platform_statistics.html', takes_context=True)
def platform_statistics(context):
    statistics = PlatformStatistics()
    context.update({'statistics': statistics.generate()})
    return context


