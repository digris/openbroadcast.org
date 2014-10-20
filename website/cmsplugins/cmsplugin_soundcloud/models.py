from django.db import models
from django.utils.translation import ugettext as _

from cms.models import CMSPlugin

from cmsplugin_soundcloud import settings

class Soundcloud(CMSPlugin):
    
    url = models.URLField(max_length=512)

    autoplay = models.BooleanField(
        _('autoplay'),
        default=settings.CMS_SOUNDCLOUD_DEFAULT_AUTOPLAY
    )

    def __unicode__(self):
        return u'%s' % (self.pk)
