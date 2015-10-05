#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from shop_ajax.views import AjaxCartDetails


urlpatterns = patterns('',
    url(r'^delete/$',
        AjaxCartDetails.as_view(action='delete'),
        name='cart_delete'),
    url('^item/$',
        AjaxCartDetails.as_view(action='post'),
        name='cart_item_add' ),
    url(r'^$',
        AjaxCartDetails.as_view(), name='cart'),
    url(r'^update/$',
        AjaxCartDetails.as_view(action='put'),
        name='cart_update'),
    url('^item/(?P<id>[0-9A-Za-z-_.//]+)$',
        AjaxCartDetails.as_view(),
        name='cart_item' ),
)
