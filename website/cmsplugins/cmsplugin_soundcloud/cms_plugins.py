import re

from django.utils.translation import ugettext as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cmsplugin_soundcloud.models import Soundcloud as SoundcloudModel


class SoundcloudPlugin(CMSPluginBase):
    model = SoundcloudModel
    name = _("Soundcloud")
    render_template = "cmsplugin_soundcloud/embed.html"

    def render(self, context, instance, placeholder):
        context.update({
            'object': instance,
            'placeholder': placeholder,
            'ids': self.extract_track_id(instance.url)
        })
        return context
    
    
    def extract_track_id(self, url):
        
        REGEX_PATTERN = '^http://soundcloud.com/(?P<user_id>[-\w]+)/(?P<track_id>[-\w]+)/$'
        
        p = re.compile(REGEX_PATTERN)
        m = p.search(url)

        try:
            user_id = m.group('user_id')
            track_id = m.group('track_id')
        except Exception, e:
            print e
            user_id  = None
            track_id  = None
            
        return user_id, track_id

plugin_pool.register_plugin(SoundcloudPlugin)
