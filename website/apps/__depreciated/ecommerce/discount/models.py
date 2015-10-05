from datetime import datetime

from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from polymorphic.manager import PolymorphicManager
from polymorphic.polymorphic_model import PolymorphicModel

from shop.models.cartmodel import Cart
from shop.models.productmodel import Product
from shop.cart.cart_modifiers_base import BaseCartModifier


class DiscountBaseManager(PolymorphicManager):

    def active(self, at_datetime=None, code=''):
        if not at_datetime:
            at_datetime = datetime.now
        qs = self.filter(Q(is_active=True) & 
                Q(valid_from__lte=at_datetime) & 
                (Q(valid_until__isnull=True) | Q(valid_until__gt=at_datetime)))
        qs = qs.filter(Q(code='') | Q(code=code))
        return qs


class DiscountBase(PolymorphicModel, BaseCartModifier):
    """
    """
    name = models.CharField(_('Name'), max_length=100)
    code = models.CharField(_('Code'), max_length=30,
            blank=True, null=False, 
            help_text=_('Is discount valid only with included code'))

    is_active = models.BooleanField(_('Is active'), default=True)
    valid_from = models.DateTimeField(_('Valid from'), default=datetime.now)
    valid_until = models.DateTimeField(_('Valid until'), blank=True, null=True)

    num_uses = models.IntegerField(_('Number of times already used'),
            default=0)

    objects = DiscountBaseManager()
    product_filters = []

    def __init__(self, *args, **kwargs):
        self._eligible_products_cache = {}
        return super(DiscountBase, self).__init__(*args, **kwargs)

    class Meta:
        verbose_name = _('Discount')
        verbose_name_plural = _('Discounts')
        ordering = []

    def __unicode__(self):
        return self.get_name()

    def get_name(self):
        return self.name

    @classmethod
    def register_product_filter(cls, filt):
        """
        Register filters that affects which products this discount class
        may apply to.
        """
        cls.product_filters.append(filt)

    def eligible_products(self, in_products=None):
       """
       Returns queryset of products this discounts may apply to.
       """
       cache_key = tuple(in_products) if in_products else None
       try:
           qs = self._eligible_products_cache[cache_key]
       except KeyError:
           qs = Product.objects.all()
           for filt in self.__class__.product_filters:
               if callable(filt):
                   qs = filt(self, qs)
               elif type(filt) is dict:
                   qs = qs.filter(**filt)
               else:
                   qs = qs.filter(filt)
           if in_products:
               qs = qs.filter(id__in=[p.id for p in in_products])
           self._eligible_products_cache[cache_key] = qs
       return qs

    def is_eligible_product(self, product, cart):
        """
        Returns if given product in cart should be discounted.
        """
        products = set([cart_item.product for cart_item in cart.items.all()])
        eligible_products_in_cart = self.eligible_products(products)
        return product in eligible_products_in_cart


class CartDiscountCode(models.Model):
    cart = models.ForeignKey(Cart, editable=False)
    code = models.CharField(_('Discount code'), max_length=30)

    class Meta:
        verbose_name = _('Cart discount code')
        verbose_name_plural = _('Cart discount codes')


class PercentDiscount(DiscountBase):
    """
    Apply ``amount`` percent discount to whole cart.
    """
    amount = models.DecimalField(_('Amount'), max_digits=5, decimal_places=2)

    def get_extra_cart_price_field(self, cart):
        amount = (self.amount/100) * cart.subtotal_price
        return (self.get_name(), amount,)

    class Meta:
        verbose_name = _('Cart percent discount')
        verbose_name_plural = _('Cart percent discounts')


class CartItemPercentDiscount(DiscountBase):
    """
    Apply ``amount`` percent discount to eligible_products in Cart.
    """
    amount = models.DecimalField(_('Amount'), max_digits=5, decimal_places=2)

    def get_extra_cart_item_price_field(self, cart_item):
        if self.is_eligible_product(cart_item.product, cart_item.cart):
            return (self.get_name(),
                    self.calculate_discount(cart_item.line_subtotal))

    def calculate_discount(self, price):
        return (self.amount/100) * price
    class Meta:
        verbose_name = _('Cart item percent discount')
        verbose_name_plural = _('Cart item percent discounts')


class CartItemAbsoluteDiscount(DiscountBase):
    """
    Apply ``amount`` discount to eligible_products in Cart.
    """
    amount = models.DecimalField(_('Amount'), max_digits=5, decimal_places=2)

    def get_extra_cart_item_price_field(self, cart_item):
        if self.is_eligible_product(cart_item.product, cart_item.cart):
            return (self.get_name(),
                    self.calculate_discount(cart_item.line_subtotal))

    def calculate_discount(self, price):
        return self.amount

    class Meta:
        verbose_name = _('Cart item absolute discount')
        verbose_name_plural = _('Cart item absolute discounts')
