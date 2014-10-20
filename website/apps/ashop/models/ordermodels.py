from django.db import models

"""
NOT WORKING!! NOT WORKING!! NOT WORKING!! NOT WORKING!! NOT WORKING!! NOT WORKING!! NOT WORKING!! NOT WORKING!
NOT WORKING!! NOT WORKING!! NOT WORKING!! NOT WORKING!! NOT WORKING!! NOT WORKING!! NOT WORKING!! NOT WORKING!! 

> patched into shop.*

"""


from shop.models.defaults.bases import BaseOrder
from shop.models.defaults.managers import OrderManager

from ashop.addressmodel.models import Address


"""
Custom order model (settings.SHOP_ORDER_MODEL)
add methods for downloadable products
"""
class Order(BaseOrder):
    
    objects = OrderManager()
    
    billing_address = models.ForeignKey(Address, blank=True, null=True, related_name='order_billing_address')
    shipping_address = models.ForeignKey(Address, blank=True, null=True, related_name='order_shipping_address')

    class Meta(object):
        abstract = False
        app_label = 'shop'
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def set_billing_address(self, billing_address):
        """
        Override for shop.models.defaults.bases.set_billing_address
        """
        if  hasattr(billing_address, 'as_text'):
            self.billing_address_text = billing_address.as_text()
            
        self.billing_address = billing_address
        self.save()

    def set_shipping_address(self, shipping_address):
        """
        Override for shop.models.defaults.bases.set_shipping_address
        """
        if hasattr(shipping_address, 'as_text'):
            self.shipping_address_text = shipping_address.as_text()
            
        self.shipping_address = shipping_address  
        self.save()
