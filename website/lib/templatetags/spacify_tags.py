import re

from django.template import Library
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe


register = Library()

@stringfilter
def spacify(value, autoescape=None):
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    return mark_safe(re.sub('\s', '&'+'nbsp;', esc(value)))
spacify.needs_autoescape = True
register.filter(spacify)