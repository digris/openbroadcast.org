from django.utils.translation import ugettext as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from abcast.models import OnAirPlugin as OnAirPluginModel


@plugin_pool.register_plugin
class OnAirPlugin(CMSPluginBase):
    model = OnAirPluginModel
    name = _("On-Air Plugin")

    #render_template = "abcast/cmsplugin/on_air.html"
    render_template = "abcast/cmsplugin/on_air.html"

    # meta
    class Meta:
        app_label = 'abcast'

    def render(self, context, instance, placeholder):

        context.update({
            'instance': instance,
            'channel': instance.channel,
            'placeholder': placeholder,
        })
        return context
