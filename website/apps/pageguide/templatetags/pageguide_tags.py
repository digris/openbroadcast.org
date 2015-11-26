# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import template

register = template.Library()

@register.inclusion_tag('pageguide/templatetags/inline.html', takes_context=True)
def pageguide_inline(context, key):

    if key:
        context['render_template'] = 'pageguide/guides/{template}.html'.format(template=key)

    return context
