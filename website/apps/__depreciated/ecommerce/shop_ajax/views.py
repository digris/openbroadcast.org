# -*- coding: utf-8 -*-
from urlparse import urlsplit

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from shop.models.cartmodel import CartItem
from shop.models.productmodel import Product
from shop.util.cart import get_or_create_cart
from shop.views.cart import CartDetails


class AjaxCartDetails(CartDetails):



    def post(self, *args, **kwargs):
        """
        This is to *add* a new item to the cart. Optionally, you can pass it a
        quantity parameter to specify how many you wish to add at once
        (defaults to 1)
        """

        product_id = self.request.POST['add_item_id']
        product_quantity = self.request.POST.get('add_item_quantity')
        if not product_quantity:
            product_quantity = 1
        product = Product.objects.get(pk=product_id)
        cart_object = get_or_create_cart(self.request)
        cart_item = cart_object.add_product(product, product_quantity)
        cart_object.save()
        return self.post_success(product, cart_item, cart_object)

    def post_success(self, product, cart_item, cart_object):
        # set cart object to use later
        self.cart_object = cart_object
        return self.success()
    
    # success hooks
    def success(self, *args, **kwargs):

        if self.request.is_ajax():
            
            context = self.get_context_data(**kwargs)
            return render_to_response('shop/ajax/_cart.html', context, context_instance=RequestContext(self.request))

        else:

            try:
                referer = self.request.META.get('HTTP_REFERER', None)
                redirect_to = urlsplit(referer, 'http', False)[2] 
            except Exception, e: 
                redirect_to = reverse('cart')
                print e
                
            return HttpResponseRedirect(redirect_to)
