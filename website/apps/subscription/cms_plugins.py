# -*- coding: utf-8 -*-
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext as _
from subscription.models import SubscriptionButtonPlugin as SubscriptionButtonPluginModel

@plugin_pool.register_plugin
class SubscriptionButtonPlugin(CMSPluginBase):

    module = _("Subscription")
    name = _("Subscribe Button")
    model = SubscriptionButtonPluginModel
    render_template = "subscription/cmsplugin/subscription_button.html"

    def render(self, context, instance, placeholder):

        context.update({
            'instance': instance,
            'newsletter': instance.newsletter,
            'placeholder': placeholder,
        })
        return context
