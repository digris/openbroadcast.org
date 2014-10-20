# -*- coding: utf-8 -*-
from django import template
from django.contrib.sites.models import Site

from allauth.facebook.models import FacebookApp

register = template.Library()



class OpenGraphNode(template.Node):
    def __init__(self):
        pass

    def render(self, context):
        return '<h1>lalala</h1>'

@register.tag
def opengraph_tags(parser, token):
    """
    usage in template: {% opengraph_tags %}
    """
    
    facebook_app = FacebookApp.objects.get_current()
    
    print facebook_app

    return OpenGraphNode()


class CurrentSiteNode(template.Node):
    def __init__(self):
        pass

    def render(self, context):
        current_site = Site.objects.get_current()
        return current_site.domain

    
@register.tag
def base_url(parser, token):
    """
    usage in template: {% base_url %}
    """
    return CurrentSiteNode()





