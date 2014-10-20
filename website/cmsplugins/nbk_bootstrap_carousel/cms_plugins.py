from django.contrib import admin
from django.utils.translation import ugettext as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin


# app specific imports
from nbk_bootstrap_carousel.models import CarouselPlugin as CarouselPluginModel
from nbk_bootstrap_carousel.models import CarouselSlide

class CarouselSlideInline(admin.TabularInline):
    model = CarouselSlide

class CarouselPlugin(CMSPluginBase):
    model = CarouselPluginModel
    name = _("NBK Bootstrap Carousel")
    render_template = "nbk_bootstrap_carousel/cmsplugin/carousel.html"
    
    inlines = [CarouselSlideInline, ]
    
    def render(self, context, instance, placeholder):

        context.update({
            'object':instance,
            'placeholder':placeholder,
            'image_list' : CarouselSlide.objects.all().filter(carousel=instance)
        })
        return context

plugin_pool.register_plugin(CarouselPlugin)