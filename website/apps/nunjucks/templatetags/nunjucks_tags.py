# -*- coding: utf-8 -*-
from django import template

from nunjucks.settings import DEBUG

register = template.Library()


@register.inclusion_tag('nunjucks/templatetags/nunjucks_scripts.html', takes_context=True)
def nunjucks_scripts(context):
    context.update({'DEBUG': DEBUG})
    return context