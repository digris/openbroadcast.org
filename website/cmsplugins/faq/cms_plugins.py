from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from django.utils.translation import ugettext as _
from .models import FAQPlugin as FAQPluginModel
from .models import FAQListPlugin as FAQListPluginModel
from .models import FAQMultiListPlugin as FAQMultiListPluginModel
from .models import FAQ, FAQCateqory


@plugin_pool.register_plugin
class FAQPlugin(CMSPluginBase):
    model = FAQPluginModel
    name = _("FAQ (single) Plugin")
    module = 'FAQ'
    render_template = "faq/cmsplugin/faq.html"

    class Meta:
        app_label = 'faq'

    def render(self, context, instance, placeholder):

        faq_list = FAQ.objects.exclude(lat=None, lng=None)

        context.update({
            'instance': instance,
            'object': instance.faq,
            'faq': instance.faq,
            'faq_list': faq_list,
            'placeholder': placeholder,
        })
        return context


@plugin_pool.register_plugin
class FAQListPlugin(CMSPluginBase):
    model = FAQListPluginModel
    name = _("FAQ List Plugin")
    module = 'FAQ'
    render_template = "faq/cmsplugin/faq_list.html"

    def render(self, context, instance, placeholder):

        objects = FAQ.objects.filter(lang=instance.lang, category=instance.category)
        objects = objects.order_by('-weight', 'question',)

        context.update({
            'instance': instance,
            'objects': objects,
            'placeholder': placeholder,
        })
        return context


@plugin_pool.register_plugin
class FAQMultiListPlugin(CMSPluginBase):
    model = FAQMultiListPluginModel
    name = _("FAQ multi-category list")
    module = 'FAQ'
    render_template = "faq/cmsplugin/faq_multi_list.html"

    def render(self, context, instance, placeholder):

        # get categories
        categories =  FAQCateqory.objects.filter(lang=instance.lang)
        # TODO: implement weight on category
        # categories = categories.order_by('-weight', 'name',)

        objects = categories


        print objects

        context.update({
            'instance': instance,
            'objects': objects,
            'placeholder': placeholder,
        })
        return context
