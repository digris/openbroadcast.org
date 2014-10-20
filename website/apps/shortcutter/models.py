from django.db import models
#from django.contrib.gis.db import models
from django.utils.translation import ugettext as _

from cms.models import CMSPlugin, Page
from django_extensions.db.fields import *

from lib.fields import extra

# logging
import logging
log = logging.getLogger(__name__)


__all__ = ('ShortcutCollection', 'Shortcut')

class BaseModel(models.Model):
    
    uuid = UUIDField()
    created = CreationDateTimeField()
    updated = ModificationDateTimeField()
    
    class Meta:
        abstract = True



class ShortcutCollection(BaseModel):
    
    name = models.CharField(max_length=256, null=True, blank=False)
    title = models.CharField(max_length=256, null=True, blank=True)
    
    
    class Meta:
        app_label = 'shortcutter'
        verbose_name = _('Collection')
        verbose_name_plural = _('Collections')
        ordering = ('name', )

    def __unicode__(self):
        return "%s" % self.name
                
                

    def save(self, *args, **kwargs):
        obj = self
        super(ShortcutCollection, self).save(*args, **kwargs)



class Shortcut(BaseModel):

    name = models.CharField(max_length=256, null=True, blank=True)
    #description = models.TextField(null=True, blank=True)
    description = extra.MarkdownTextField(blank=True, null=True)

    key = models.CharField(max_length=256, null=True, blank=True)

    position = models.PositiveIntegerField(default=0)

    url = models.URLField(_("link"), blank=True, null=True)
    page_link = models.ForeignKey(Page, verbose_name=_("page"), blank=True, null=True, help_text=_("A link to a page has priority over a text link."))
    
    collection = models.ForeignKey('ShortcutCollection', null=True, blank=True, on_delete=models.SET_NULL, related_name='shortcuts')


    
    # meta
    class Meta:
        app_label = 'shortcutter'
        verbose_name = _('Shortcut')
        verbose_name_plural = _('Shortcuts')
        ordering = ('position', 'name', )

    def __unicode__(self):
        return "%s" % self.name
    
    
    def get_link(self):
        if self.page_link:
            link = self.page_link.get_absolute_url()
        elif self.url:
            link = self.url
        else:
            link = None
            
        return link
    
    def save(self, *args, **kwargs):
        obj = self        
        super(Shortcut, self).save(*args, **kwargs)


""""""
class ShortcutPlugin(CMSPlugin):    
    collection = models.ForeignKey('ShortcutCollection', related_name='plugins')
    class Meta:
        app_label = 'shortcutter'
    def __unicode__(self):
        return "%s" % self.collection.name

