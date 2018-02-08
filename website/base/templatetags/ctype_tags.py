from django import template
#from django.conf import settings
#from django.template import Library, Node, Template, resolve_variable

from django.contrib.contenttypes.models import ContentType

register = template.Library()

@register.filter 
def ct_pk_by_object(obj):
    try:
        return ContentType.objects.get_for_model(obj).pk
    except:
        return None
    
@register.filter 
def ct_name_by_object(obj):
    try:
        return '%s'.capitalize() % ContentType.objects.get_for_model(obj)
    except:
        return None
