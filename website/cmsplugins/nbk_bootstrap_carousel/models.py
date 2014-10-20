from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import *
from cms.models import CMSPlugin
    
    

class CarouselPlugin(CMSPlugin):
    uuid = UUIDField()
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()
    
    name = models.CharField(_('Name'), max_length=255, null=True, blank=True)
    
    class Meta:
        verbose_name = _('Bootstrap Carousel')
        verbose_name_plural = _('Bootstrap Carousels')
    
    def __unicode__(self):
        return self.name
    
    
class CarouselSlide(models.Model):
    uuid = UUIDField()
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()
    
    name = models.CharField(_('Name'), max_length=255, null=True, blank=True)
    image = models.ImageField(_('Slide Image'), upload_to="carousel/slides", null=True, blank=True)
    image_link = models.URLField(_('Image Link'), blank=True, null=True)
    content = models.TextField(_('Content Text'), null=True, blank=True)
    
    add_text = models.CharField(_('Additional Text'), max_length=255, null=True, blank=True)
    add_file = models.FileField(_('File to Download'), upload_to="carousel/uploads", blank=True, null=True)
    
    carousel = models.ForeignKey('CarouselPlugin')
    
    class Meta:
        verbose_name = _('Bootstrap Carousel Slide')
        verbose_name_plural = _('Bootstrap Carousel Slides')
    
    def __unicode__(self):
        return self.name
    
    
    