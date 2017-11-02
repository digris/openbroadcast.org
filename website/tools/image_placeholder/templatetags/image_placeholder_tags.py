# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template

from ..placeholder import generate_image_placeholder


register = template.Library()

@register.simple_tag
def image_placeholder(size=None, color=None):

    if size:
        _size = size.split('x')

        if len(_size) == 1:
            size = [int(_size[0]), int(_size[0])]

        if len(_size) == 2:
            size = [int(_size[0]), int(_size[1])]

    return generate_image_placeholder(size, color)
