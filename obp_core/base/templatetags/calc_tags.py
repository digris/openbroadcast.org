import time

from django import template

register = template.Library()


@register.filter
def multiply(value, arg):
    return float(value) * float(arg)


@register.filter
def divide(value, arg):
    try:
        return int(float(value) / float(arg))
    except BaseException:
        return None


@register.filter
def subtract(value, arg):
    return int(float(value) - float(arg))


@register.filter
def roundint(value):
    return int(value)


@register.filter
def squaretuple(value):
    return f"{value}x{value}"


@register.filter
def halftuple(value):
    return f"{value}x{int(value) / 2}"


@register.filter
def widetuple(value):
    return f"{value}x{int(value) / 16 * 9}"


@register.filter
def sec_to_time(value):
    if not value:
        return "--:--"
    if value >= 3600:
        return time.strftime("%H:%M:%S", time.gmtime(value))
    else:
        return time.strftime("%M:%S", time.gmtime(value))


@register.filter
def msec_to_time(value):
    if not value:
        return "--:--"
    value = int(value / 1000)
    if value >= 3600:
        return time.strftime("%H:%M:%S", time.gmtime(value))
    else:
        return time.strftime("%M:%S", time.gmtime(value))
