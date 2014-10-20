from django.db import models
from django.utils.translation import ugettext as _

from cms.models import CMSPlugin

from cmsplugin_youtube import settings

class YouTube(CMSPlugin):
    
    video_url = models.URLField(max_length=512)
    name = models.CharField(max_length=200, blank=True, null=True, verbose_name='Optional title to display')

    width = models.IntegerField(_('width'),
            default=settings.CMS_YOUTUBE_DEFAULT_WIDTH)
    height = models.IntegerField(_('height'),
            default=settings.CMS_YOUTUBE_DEFAULT_HEIGHT)


    def __unicode__(self):
        return u'%s' % (self.video_url,)
