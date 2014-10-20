from django.utils.translation import ugettext as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from bcmon.models import Playout
from bcmon.models import ChannelPlugin as ChannelPluginModel


@plugin_pool.register_plugin
class ChannelPlugin(CMSPluginBase):
    model = ChannelPluginModel
    name = _("Channel Plugin")
    render_template = "bcmon/plugins/channel.html"

    # meta
    class Meta:
        app_label = 'bcmon'

    def render(self, context, instance, placeholder):
        
        playouts = Playout.objects.filter(channel=instance.channel).order_by('-time_start')[0:10]
        
        context.update({
            'instance': instance,
            'object': instance.channel,
            'placeholder': placeholder,
            'playouts': playouts,
        })
        return context
