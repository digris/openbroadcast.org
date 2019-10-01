# -*- coding: utf-8 -*-
from django import template

register = template.Library()


@register.filter
def get_dict_item(dictionary, key):
    return dictionary.get(key)


@register.assignment_tag
def get_dict_item_as(dictionary, key):
    return dictionary.get(key)
