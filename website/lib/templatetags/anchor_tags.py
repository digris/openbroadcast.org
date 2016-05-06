# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template
from django.template.defaultfilters import stringfilter
from urlparse import urlparse

register = template.Library()

@register.filter
@stringfilter
def dehttp(value):
    value = value.replace('http://', '').replace('https://', '')
    if value[-1] == '/':
        return value[:-1]
    return value

dehttp.is_safe = True

@register.filter
@stringfilter
def domain_for_url(value):
    parsed_uri = urlparse(value)
    domain = '{uri.netloc}'.format(uri=parsed_uri)
    return domain

#domain_for_url.is_safe = True
