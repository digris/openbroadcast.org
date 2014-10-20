from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from django.utils.translation import ugettext as _
from .models import GuidePlugin as GuidePluginModel
from .models import Step, Guide



@plugin_pool.register_plugin
class GuidePlugin(CMSPluginBase):
    model = GuidePluginModel
    name = _("Guide Plugin")
    module = 'Guide'
    render_template = "stepguide/cmsplugin/guide.html"

    def render(self, context, instance, placeholder):

        objects = Step.objects.filter(guide=instance.guide)
        objects = objects.order_by('position',)

        context.update({
            'instance': instance,
            'guide': instance.guide,
            'step_list': objects,
            'placeholder': placeholder,
        })
        return context
