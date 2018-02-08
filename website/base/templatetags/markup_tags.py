import markdown as mkdn

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter()
def markdown(value):
    value = value.replace('***', " <br>")
    return mark_safe(mkdn.markdown(value, enable_attributes=False))
    # return mark_safe(mkdn.markdown(value, safe_mode='escape'))
