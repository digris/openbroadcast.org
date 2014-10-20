# -*- coding: utf-8 -*-
"""Shipping backend that skips the whole shipping process."""

from django.conf.urls.defaults import patterns, url


class SkipShippingBackend(object):

    backend_name = "Skip Shipping Backend"
    url_namespace = "skip-shipping"

    def __init__(self, shop):
        self.shop = shop

    def simple_view(self, request):
        """
        This simple view does nothing but forward to the final URL. When the
        money is sent, the shop owner can set this order to complete manually.
        """
        order = self.shop.get_order(request)
        return self.shop.finished(order)

    def get_urls(self):
        urlpatterns = patterns('',
            url(r'^$', self.simple_view, name='skip-shipping' ),
        )
        return urlpatterns