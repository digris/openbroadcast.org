from django import template

register = template.Library()


@register.inclusion_tag("player/templatetags/_inline.html", takes_context=True)
def player_inline(context):
    return context
