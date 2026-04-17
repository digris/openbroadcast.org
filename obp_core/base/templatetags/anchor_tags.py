from django import template
from django.template.defaultfilters import stringfilter

from urllib.parse import urlparse

register = template.Library()


@register.filter
@stringfilter
def dehttp(value):
    value = value.replace("http://", "").replace("https://", "")
    if value[-1] == "/":
        return value[:-1]
    return value


dehttp.is_safe = True


@register.filter
@stringfilter
def domain_for_url(value):
    parsed_uri = urlparse(value)
    domain = f"{parsed_uri.netloc}"
    return domain
