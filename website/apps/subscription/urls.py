# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from .views import SubscribeView, WebhookView

urlpatterns = patterns('subscription.views',
    # site integration
    url(r'^subscribe/(?P<list_id>[-\w]+)/$', SubscribeView.as_view(), name='subscription-subscribe'),
    # webhooks
    url(r'^webhook/(?P<backend>[-\w]+)/(?P<token>[-\w]+)/$', WebhookView.as_view(), name='subscription-mailchimp-webhook'),
)