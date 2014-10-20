# ------------------------------------------------------------------------------
# A collection of template tags and filters for the Django web framework.
#
# Put this file in your layout that might look like this:
# tpl_lib/
#   __init__.py
#   templatetags/
#       __init__.py
#       urlback.py
# Add 'tpl_lib' to the INSTALLED_APPS setting.
# In your template, load the module: {% load urlback %}
#
# Copyright (C) 2010, Patrick Samson
# This program is licensed under the BSD License (see the file LICENSE).
# ------------------------------------------------------------------------------

# https://bitbucket.org/psam/django-template-lib/src

import urlparse

from django.template import Library
from django.template.defaulttags import URLNode, url

register = Library()

class UrlOrBackNode(URLNode):
    "For use in the url_or_back tag"
    def __init__(self, n):
        super(UrlOrBackNode, self).__init__(n.view_name, n.args, n.kwargs, n.asvar)

    def render(self, context):
        url = super(UrlOrBackNode, self).render(context)
        referer_url = 'request' in context and 'HTTP_REFERER' in context['request'].META \
            and urlparse.urlsplit(context['request'].META['HTTP_REFERER']).path or ''
        return referer_url and url == referer_url and 'javascript:history.back()' or url

@register.tag
def url_or_back(parser, token):
    """
    Returns the result of the default tag ``url`` unless it is the same target
    as the HTTP_REFERER header in which case a simple
        'javascript:history.back()'
    saves a useless hit to the server.
    """
    return UrlOrBackNode(url(parser, token))