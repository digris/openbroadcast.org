# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from cms.models import CMSPlugin

LANGUAGES = getattr(settings, 'LANGUAGES', None)


class FAQCateqory(models.Model):

    name = models.CharField(max_length=255)
    lang = models.CharField(verbose_name=_("Language"), max_length=7, choices=LANGUAGES, null=True)

    class Meta(object):
        app_label = 'faq'
        verbose_name = _('FAQ Category')
        verbose_name_plural = _("FAQ Categories")

    def __unicode__(self):
        return self.name


class FAQ(models.Model):

    question = models.CharField(max_length=255)
    answer = models.TextField()
    WEIGHT_CHOICES = [(i,i) for i in range(1, 6)]
    weight = models.PositiveSmallIntegerField(default=12, choices=WEIGHT_CHOICES)
    category = models.ForeignKey(FAQCateqory, blank=True, null=True)
    lang = models.CharField(verbose_name=_("Language"), max_length=7, choices=LANGUAGES, blank=True, null=True, help_text=_('Will be taken from category if specifyed.'))

    
    # auto-update
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta(object):
        app_label = 'faq'
        verbose_name = _('FAQ')
        verbose_name_plural = _("FAQs")
        ordering = ['-weight', 'question']

    def __unicode__(self):
        return '%s (%s, %s)' % (self.question, self.category, self.lang)
    
    
    def save(self, *args, **kwargs):

        if self.category:
            self.lang = self.category.lang


        super(FAQ, self).save(*args, **kwargs)



class FAQPlugin(CMSPlugin):
    """
    not implemented yet
    actually not needed either
    """
    faq = models.ForeignKey(FAQ)

    class Meta:
        app_label = 'faq'

    def __unicode__(self):
        return self.faq.name
        

class FAQListPlugin(CMSPlugin):
    """
    renders entries from the respective category
    """
    category = models.ForeignKey(FAQCateqory, blank=True, null=True)
    lang = models.CharField(verbose_name=_("Language"), max_length=7, choices=LANGUAGES)

    class Meta:
        app_label = 'faq'

    def __unicode__(self):
        return  '%s : %s' % (self.category.name, self.get_lang_display())


class FAQMultiListPlugin(CMSPlugin):

    """
    renders a complete faq section from a single instance
    """
    #categories = models.ManyToManyField(FAQCateqory, blank=False, null=True)
    lang = models.CharField(verbose_name=_("Language"), max_length=7, choices=LANGUAGES)
    two_columns = models.BooleanField(default=False)

    class Meta:
        app_label = 'faq'

    def __unicode__(self):
        #return  '%s : %s' % (self.category.name, self.get_lang_display())
        return  '%s' % (self.get_lang_display())
