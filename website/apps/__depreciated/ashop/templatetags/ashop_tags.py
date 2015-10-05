# -*- coding: utf-8 -*-
from django import template

from classytags.helpers import InclusionTag
from classytags.core import Options
from classytags.arguments import Argument

from shop.util.cart import get_or_create_cart
from shop.models.productmodel import Product

from alibrary.models import Release

from ashop.util.base import *


register = template.Library()

class Downloads(InclusionTag):
    """
    Inclusion tag for displaying downloads.
    """
    template = 'shop/templatetags/_downloads.html'
    options = Options(
        Argument('order', resolve=True),
        )

    def get_context(self, context, order):
        
        downloads = Release.objects.filter(releaseproduct__orderitem__order=order) 
        
        return {
            'downloads': downloads
        }
        
register.tag(Downloads)



@register.filter
def get_products(object, request):
    """
    usage in template: {% for download in media|get_downloads:request  %}
    """
    
    # sorry for reverseing, comes from simpler filter usage
    downloads = get_object_products(request, object)

    return downloads
