from django.utils.translation import ugettext as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

@plugin_pool.register_plugin
class PlatformStatisticsPlugin(CMSPluginBase):

    name = _("Platform Statistics")
    render_template = "statistics/platform_statistics_plugin.html"

    def render(self, context, instance, placeholder):
        context.update({
            'object': instance,
            'placeholder': placeholder,
        })
        return context

