# -*- coding: utf-8 -*-
from django import template
import dateutil.parser

register = template.Library()

@register.filter
def parse_datetime(str):
    return dateutil.parser.parse(str)
