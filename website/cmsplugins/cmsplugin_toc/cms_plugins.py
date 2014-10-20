from django.utils.translation import ugettext as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from settings import CMS_GIT_FILE

@plugin_pool.register_plugin
class TOCPlugin(CMSPluginBase):

    name = _("TOC Plugin")
    render_template = "cmsplugin_toc/toc.html"

    def render(self, context, instance, placeholder):

        context.update({
            'object': instance,
            'placeholder': placeholder,
            'changelog': self.parse_git_changelog()
        })
        return context
    
    
    def parse_git_changelog(self):

        path = CMS_GIT_FILE

        try:
            with open(path, 'r') as content_file:
                content = content_file.read()
        except:
            content = 'Unable to parse changelog.'


        return content

#plugin_pool.register_plugin(GitStatusPlugin)
