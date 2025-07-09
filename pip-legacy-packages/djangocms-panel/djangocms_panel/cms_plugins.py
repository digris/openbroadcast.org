from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _
from .models import Panel

class PanelPlugin(CMSPluginBase):
    model = Panel
    name = _("Panel")
    allow_children = True
    render_template = "djangocms_panel/panel.html"

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context

plugin_pool.register_plugin(PanelPlugin)
