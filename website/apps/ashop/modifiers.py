from decimal import Decimal

from django.conf import settings

from shop.cart.cart_modifiers_base import BaseCartModifier


class FixedTaxRate(BaseCartModifier):
    """
    A basic Tax calculator: it simply adds a taxes field to the *order*,
    and makes it a fixed percentage of the subtotal (10%)

    Obviously, this is only provided as an example, and anything serious should
    use a more dynamic configuration system, such as settings or models to
    hold the tax values...
    """
    TAX_PERCENTAGE = Decimal('8')

    def get_extra_cart_price_field(self, cart):
        """
        Add a field on cart.extra_price_fields:
        """
        taxes = (self.TAX_PERCENTAGE / 100) * cart.current_total
        result_tuple = ('Taxes total', taxes)
        return result_tuple


class BulkRebateModifier(BaseCartModifier):

    def get_extra_cart_item_price_field(self, cart_item):
        """
        Add a rebate to a line item depending on the quantity ordered:

        This serves as an example mass rebate modifier: if you buy more than
        5 items of the same kind, you get 10% off the bunch

        >>> cart_item.extra_price_fields.update({'Rebate': Decimal('10.0')})
        """
        REBATE_PERCENTAGE = Decimal('10')
        NUMBER_OF_ITEMS_TO_TRIGGER_REBATE = 5
        result_tuple = None
        if cart_item.quantity >= NUMBER_OF_ITEMS_TO_TRIGGER_REBATE:
            rebate = (REBATE_PERCENTAGE / 100) * cart_item.line_subtotal
            result_tuple = ('Rebate', -rebate)
        return result_tuple  # Returning None is ok
    
    
    
    
    
class FixedShippingCosts(BaseCartModifier):
    
    def get_extra_cart_price_field(self, cart):
        """
        Add a field on cart.extra_price_fields:
        """
        shipping = 0
        try:
            for item in cart.items.all():
                if item.product.needs_shipping:
                    shipping = 1
        except Exception, e:
            pass
        
        
        result_tuple = ('Shipping', shipping)
        return result_tuple
    
    """
    This will add a fixed amount of money for shipping costs.
    """
    def add_extra_cart_price_field(self, cart):
        cart.extra_price_fields.append(
            ('Shipping costs', Decimal(
                settings.SHOP_SHIPPING_FLAT_RATE)))
        return cart
    