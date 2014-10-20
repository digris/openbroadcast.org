from django.utils.translation import ugettext_lazy as _
from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase
from cms.plugins.link.forms import LinkForm
from models import ShortcutPlugin as ShortcutPluginModel

class ShortcutPlugin(CMSPluginBase):
    model = ShortcutPluginModel
    name = _("Shortcut Plugin")
    render_template = "shortcutter/cmsplugin/collection.html"
    text_enabled = False
    
    def render(self, context, instance, placeholder):

        context.update({
            'name': instance.collection.name,
            'placeholder': placeholder,
            'object': instance.collection
        })
        return context

    
plugin_pool.register_plugin(ShortcutPlugin)