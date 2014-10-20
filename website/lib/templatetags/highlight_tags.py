import re

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def highlight(text, word):
    
    pattern = re.compile(word, re.IGNORECASE)
    return mark_safe(pattern.sub("<em class='highlight'>%s</em>" % word, text))
    