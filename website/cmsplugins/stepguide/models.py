# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from cms.models import CMSPlugin


HINT_CHOICES = (
    ('info', 'Info (green)'),
    ('warning', 'Warning (yellow)'),
    ('critical', 'Critical (red)'),
)


class Guide(models.Model):

    name = models.CharField(max_length=255)
    summary = models.TextField(blank=True, null=True)

    step_numbers = models.BooleanField(default=True)
    include_toc = models.BooleanField(verbose_name='Include Table of Content', default=False)

    class Meta(object):
        app_label = 'stepguide'
        verbose_name = _('Step Guide')
        verbose_name_plural = _("Step Guides")

    def __unicode__(self):
        return self.name


class Step(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    hint = models.TextField(blank=True, null=True)
    hint_type = models.CharField(max_length=10, default='info', choices=HINT_CHOICES)
    image = models.ImageField(upload_to='stepguide', blank=True, null=True)
    image_caption = models.CharField(max_length=255, blank=True, null=True)
    vimeo_video_id = models.CharField(help_text="Show vimeo video. If id is set, the video will be displayed instead of an image.", max_length=255, blank=True, null=True)

    position = models.PositiveSmallIntegerField(default=0)
    guide = models.ForeignKey(Guide, blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta(object):
        app_label = 'stepguide'
        verbose_name = _('Step')
        verbose_name_plural = _("Steps")
        ordering = ['-position',]

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.guide)
    
    
    def save(self, *args, **kwargs):

        super(Step, self).save(*args, **kwargs)




class GuidePlugin(CMSPlugin):

    guide = models.ForeignKey(Guide)

    class Meta:
        app_label = 'stepguide'

    def __unicode__(self):
        return  '%s' % (self.guide.name)

