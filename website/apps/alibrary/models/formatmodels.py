# python

# django
from django.db import models
from django.utils.translation import ugettext as _

# logging
import logging
logger = logging.getLogger(__name__)


################


class Format(models.Model):
    
    #name = models.CharField(max_length=200)
    
    
    FORMAT_CHOICES = (
        ('mp3', _('MP3')),
        ('flac', _('Flac')),
        ('wav', _('WAV')),
        ('aiff', _('AIFF')),
    )
    format = models.CharField(max_length=4, choices=FORMAT_CHOICES)
    
    default_price = models.PositiveIntegerField(max_length=6, default=1, blank=True, null=True)
    
    VERSION_CHOICES = (
        ('base', _('Base')),
    )
    version = models.CharField(max_length=10, default='base', choices=VERSION_CHOICES)
    
    excerpt = models.TextField(blank=True, null=True, verbose_name=_("Notes")) 
    
    # auto-update
    created = models.DateField(auto_now_add=True, editable=False)
    updated = models.DateField(auto_now=True, editable=False)
    
    # manager
    objects = models.Manager()

    # meta
    class Meta:
        app_label = 'alibrary'
        verbose_name = _('Format')
        verbose_name_plural = _('Formats')
        ordering = ('format', 'version' )

    
    def __unicode__(self):
        return '%s' % (self.format)
    
    @property
    def name(self):
        return '%s - %s' % (self.format, self.version)



