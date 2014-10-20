from django.db import models
from django.utils.translation import ugettext as _
from guardian.shortcuts import assign

from shop.models import Product
from filer.fields.image import FilerImageField
from filer.fields.file import FilerFileField
from filer.models.filemodels import *
from filer.models.foldermodels import *
from cms.models import CMSPlugin
from shop.models.productmodel import Product
from shop.models.ordermodel import Order
from shop.order_signals import *
from alibrary.models import Release, Media


class Releaseproduct(Product):
    
    # relations
    release = models.ForeignKey(Release, related_name='releaseproduct')
    
    class Meta:
        app_label = 'ashop'
        verbose_name = _('Releaseproduct')
        verbose_name_plural = _('Releaseproducts')
        ordering = ['-polymorphic_ctype', '-unit_price', 'name',]
        
        
    def get_type(self):
        # TODO: Improve!
        if self.__class__.__name__ == 'Hardwarerelease':
            return 'hardware'

        if self.__class__.__name__ == 'Downloadrelease':
            return 'download'
    

    def is_soldout(self):
        
        if self.get_type() == 'download':
            return False
        
        if self.get_type() == 'hardware' and self.stock < 1:
            return True
        

    
    def get_download_url(self):
        if self.release:
            return self.release.get_download_url(str(self.format), 'base')
        
    def save(self, *args, **kwargs):
        
        release = self.release

        self.slug = str(self.get_type()) + '-' + str(release.slug)
        self.name = release.name
        
        super(Releaseproduct, self).save(*args, **kwargs)
        
        

        
        



class Hardwarerelease(Releaseproduct):
    # 
    weight = models.IntegerField(null=True, blank=True)
    needs_shipping = models.BooleanField(default=True, blank=True)
    
    description = models.TextField(null=True, blank=True, help_text=_('Additional description for Hardware edition. (e.g. packing, extras etc.)'))
    
    circulation = models.IntegerField(null=True, blank=True, help_text=_('Circulation'))
    
    stock = models.IntegerField(null=True, blank=True, help_text=_('Stock. [If set to 0 the release will be marked as sold-out]'))
    
    MEDIUM_CHOICES = (
        ('Vinyl', (
                ('7inch', "7''"),
                ('10inch', "10''"),
                ('12inch', "12''"),
                ('cd', "CD"),
                ('tape', "Tape"),
                ('tapedvd', "Tape/DVD"),
                ('puzzle', "Puzzle"),
            )
        ),
        ('other', 'Other'),
    )
    
    medium = models.CharField(max_length=10, null=True, blank=True, choices=MEDIUM_CHOICES)
    
    def format(self):
        return self.medium


    class Meta:
        app_label = 'ashop'
        verbose_name = _('Hardware Release')
        verbose_name_plural = _('Hardware Releases')
        ordering = ['name']

        
class Downloadrelease(Releaseproduct):
    # 
    # weight = models.IntegerField(null=True, blank=True)
    # needs_shipping = models.BooleanField(default=False, blank=True)
    
    # relations
    
    needs_shipping = False
    medium = _('Digital')
    circulation = False

    
    format = models.ForeignKey('alibrary.Format', related_name='releaseformat')
    
    def description(self):
        return _('Digital Download.')

    class Meta:
        app_label = 'ashop'
        verbose_name = _('Downloadable Release')
        verbose_name_plural = _('Downloadable Releases')
        ordering = ['name']
        permissions = (
            ('download', 'Download Release'),
        )

        




        
        
"""
Not subclassed here - single tracks are only available as download (no hardware...)
"""

class Downloadmedia(Product):
    
    # relations
    media = models.ForeignKey(Media, related_name='mediaproduct')
    
    format = models.ForeignKey('alibrary.Format', related_name='mediaformat')

    needs_shipping = False
    medium = _('Digital')
    
    class Meta:
        app_label = 'ashop'
        verbose_name = _('Downloadable Track')
        verbose_name_plural = _('Downloadable Tracks')
        ordering = ['name']
        permissions = (
            ('download', 'Download Track'),
        )
        
    def __unicode__(self):
        return '%s | %s' % (self.name, self.format)
    
    
    def get_type(self):
        return 'download'
    

    def get_download_url(self):
        
        if self.media:
            return self.media.get_download_url(str(self.format), 'base')
        
    def save(self, *args, **kwargs):
        
        media = self.media
        
        self.slug = str(self.get_type()) + '-' + str(media.slug)
        self.name = '%s | %s' % (media.name, self.format)
        
        super(Downloadmedia, self).save(*args, **kwargs)
        







        
"""
class SingleProduct(CMSPlugin):
    product = models.ForeignKey(Releaseproduct)
    STYLE_CHOICES = (
        ('s', _('Small')),
        ('m', _('Medium (Not implemented)')),
        ('l', _('Large')),
    )
    style = models.CharField(max_length=24, default='l', choices=STYLE_CHOICES)
"""











"""
Add object permissions after successfull purchase (logged in users only)
"""
def confirmed_purchase(sender, **kwargs):

    order = kwargs.get('order')
    
    # emails...
    print
    print '#########################################'
    print 'PURCHASE CONFIRMED'
    print '#########################################'
    print
    
    
    
    if order.user:
        """
        applies if ordered by logged-in user
        """
        
        user = order.user
 
 
        # get downloadable tracks
        for item in order.items.filter(product__downloadmedia__active=True):

            print "product__downloadmedia__active"
            product = item.product
            
            if product.get_type() == 'download':

            
                print 'permissions', 
                print user.has_perm('download', product)
                
                if not user.has_perm('download', product):
                    assign('download', user, product)
 
 
 
        # get downloadable releases
        for item in order.items.filter(product__releaseproduct__active=True):

            product = item.product
            
            
            if product.get_type() == 'download':

            
                print 'permissions', 
                print user.has_perm('download', product)
                
                if not user.has_perm('download', product):
                    assign('download', user, product)
            


            """
            The ultimate bad style... 
            """
            if product.get_type() == 'hardware':
                try:
                    release = product.release
                    download_products = Downloadrelease.objects.filter(release=release)
    
                    for download_product in download_products:
                        if download_product and not user.has_perm('download', download_product):
                            assign('download', user, download_product)
                        
                except Exception, e:
                    print e
                



completed.connect(confirmed_purchase)








