import re

from django.utils.translation import ugettext as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cmsplugin_vimeo.models import Vimeo as VimeoModel


REGEX_PATTERN = '^http://vimeo.com/(?P<id>[0-9]+).*'

class VimeoPlugin(CMSPluginBase):
    model = VimeoModel
    name = _("Vimeo")
    render_template = "cmsplugin_vimeo/embed.html"

    def render(self, context, instance, placeholder):

        context.update({
            'object': instance,
            'placeholder': placeholder,
            'video_id': self.extract_video_id(instance.video_url)
        })
        return context
    
    
    def extract_video_id(self, video_url):
        
        p = re.compile(REGEX_PATTERN)
        m = p.search(video_url)
        
        try:
            video_id = m.group('id')
        except Exception, e:
            video_id  = None
            
        return video_id

plugin_pool.register_plugin(VimeoPlugin)
