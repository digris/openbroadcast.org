from django import template

from django.contrib.humanize.templatetags.humanize import intcomma

from settings import SHOP_CURRENCY

register = template.Library()

@register.filter
def currency(dollars):
    dollars = float(dollars)
    return "%s%s%s" % (SHOP_CURRENCY['character'] + SHOP_CURRENCY['separator'], intcomma(int(dollars)), ("%0.2f" % dollars)[-3:])
