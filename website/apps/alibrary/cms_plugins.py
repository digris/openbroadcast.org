from django.utils.translation import ugettext as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from alibrary.models import MediaPlugin as MediaPluginModel
from alibrary.models import ReleasePlugin as ReleasePluginModel
from alibrary.models import ArtistPlugin as ArtistPluginModel


@plugin_pool.register_plugin
class MediaPlugin(CMSPluginBase):
    model = MediaPluginModel
    name = _("Track Plugin")
    render_template = "alibrary/cmsplugin/media.html"

    # meta
    class Meta:
        app_label = 'alibrary'

    def render(self, context, instance, placeholder):

   
        context.update({
            'instance': instance,
            'object': instance.media,
            'media': instance.media,
            'placeholder': placeholder,
        })
        return context


@plugin_pool.register_plugin
class ReleasePlugin(CMSPluginBase):
    model = ReleasePluginModel
    name = _("Release Plugin")
    render_template = "alibrary/cmsplugin/release.html"

    # meta
    class Meta:
        app_label = 'alibrary'

    def render(self, context, instance, placeholder):

   
        context.update({
            'instance': instance,
            'object': instance.release,
            'item': instance.release,
            'release': instance.release,
            'placeholder': placeholder,
        })
        return context

""""""
@plugin_pool.register_plugin
class ArtistPlugin(CMSPluginBase):
    model = ArtistPluginModel
    name = _("Artist Plugin")
    render_template = "alibrary/cmsplugin/artist.html"

    # meta
    class Meta:
        app_label = 'alibrary'

    def render(self, context, instance, placeholder):
        
        context.update({
            'instance': instance,
            'object': instance.artist,
            'placeholder': placeholder,
        })
        return context
