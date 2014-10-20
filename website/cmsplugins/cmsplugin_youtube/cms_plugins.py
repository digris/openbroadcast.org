import re

from django.utils.translation import ugettext as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cmsplugin_youtube.models import YouTube as YouTubeModel


class YouTubePlugin(CMSPluginBase):
    model = YouTubeModel
    name = _("YouTube")
    render_template = "cmsplugin_youtube/embed_jwp.html"

    def render(self, context, instance, placeholder):

        context.update({
            'object': instance,
            'placeholder': placeholder,
            'video_id': self.extract_video_id(instance.video_url)
        })
        return context
    
    
    def extract_video_id(self, video_url):
        
        
        m = re.search(r"youtube\.com/.*v=([^&]*)", video_url)

        try:
            video_id = m.group(1)
        except Exception, e:
            print e
            video_id  = None
            
        return video_id

plugin_pool.register_plugin(YouTubePlugin)
