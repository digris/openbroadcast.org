# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import re
import logging
from django.db import models
from django.db.models import Q
from django.conf import settings
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch.dispatcher import receiver
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from hvad.models import TranslatableModel, TranslatedFields
from hvad.manager import TranslationManager
from cms.models import CMSPlugin
from cms.models.fields import PageField
from base.models import TimestampedModel

log = logging.getLogger(__name__)
User = settings.AUTH_USER_MODEL


from .backends.mc import MailchimpBackend

BACKEND_CHOICES = (
    ('mailchimp', 'Mailchimp'),
    ('madmimi', 'Madmimi (not implemented)'),
)


class Newsletter(TranslatableModel):

    name = models.CharField(max_length=256, verbose_name=_('Name (internal)'))

    translations = TranslatedFields(
        title = models.CharField(max_length=256, verbose_name=_('Title (translated)')),
        description = models.TextField(blank=True, null=True, verbose_name=_('Description')),
    )

    backend = models.CharField(max_length=36, default='mailchimp', choices=BACKEND_CHOICES)
    backend_id = models.CharField(max_length=64, blank=True, null=True)
    backend_api_key = models.CharField(max_length=64, blank=True, null=True)

    objects = TranslationManager()

    class Meta:
        app_label = 'subscription'
        verbose_name = _('Newsletter')
        #ordering = ('-publish',)

    def __unicode__(self):
        return u'%s' % self.lazy_translation_getter('name', str(self.pk))


    def get_backend(self):

        backend = None
        if self.backend == 'mailchimp':
            if self.backend_api_key:
                backend = MailchimpBackend(api_key=self.backend_api_key)
            else:
                backend = MailchimpBackend()
        return backend


    def subscribe(self, email, name, language=None, channel=None):
        log.info(u'subscribe %s - %s [%s] %s on %s' % (email, name, language, channel, self.name))
        backend = self.get_backend()
        backend.subscribe(list_id=self.backend_id, email=email, name=name, language=language, channel=channel)


    def unsubscribe(self, email):
        log.info(u'unsubscribe %s from %s' % (email, self.name))
        backend = self.get_backend()
        backend.unsubscribe(list_id=self.backend_id, email=email)

    def save(self, *args, **kwargs):
        super(Newsletter, self).save(*args, **kwargs)




class SubscriptionManager(models.Manager):
    pass
    #def published(self):
    #    return self.get_query_set().filter(publish__lte=datetime.datetime.utcnow())

class Subscription(TimestampedModel):

    user = models.ForeignKey(User, blank=True, null=True)
    email = models.EmailField(max_length=256, blank=True, null=True)
    name = models.CharField(max_length=256, blank=True, null=True)

    newsletter = models.ForeignKey(Newsletter, blank=True, null=True)
    backend_id = models.CharField(max_length=64, blank=True, null=True)

    #site = models.ForeignKey(Site, blank=True, null=True)
    channel = models.CharField(max_length=256, blank=True, null=True)
    language = models.CharField(max_length=5, blank=True, null=True)

    opted_out = models.DateTimeField(blank=True, null=True)
    confirmed = models.DateTimeField(blank=True, null=True)

    objects = SubscriptionManager()

    class Meta:
        app_label = 'subscription'
        verbose_name = _('Subscription')
        ordering = ('-created',)

    def __unicode__(self):
        if self.user:
            return u'%s - %s' % (self.user.username, self.user.email)
        return u'%s' % self.email


    def get_email(self):
        if self.user:
            return self.user.email
        else:
            return self.email

    def get_name(self):
        if self.user:
            return self.user.username
        else:
            return self.name


    def subscribe(self):
        log.info('subscribe: %s - %s - %s - %s' % (self.get_email(), self.get_name(), self.language, self.channel))
        self.newsletter.subscribe(email=self.get_email(), name=self.get_name(), language=self.language, channel=self.channel)

    def unsubscribe(self):
        log.info('unsubscribe: %s' % (self.get_email()))
        self.newsletter.unsubscribe(email=self.get_email())


    def update_subscription(self):

        if self.opted_out:
            self.unsubscribe()
        else:
            self.subscribe()


    def save(self, *args, **kwargs):
        super(Subscription, self).save(*args, **kwargs)

@receiver(post_save, sender=Subscription)
def subscription_post_save(sender, instance, **kwargs):
    log.debug('Subscription post-save: %s' % (instance))

    #instance.update_subscription()

@receiver(post_delete, sender=Subscription)
def subscription_post_delete(sender, instance, **kwargs):
    log.debug('Subscription post-delete: %s' % (instance))

    instance.unsubscribe()



# cms plugin data models

class SubscriptionButtonPlugin(CMSPlugin):

    button_text = models.CharField(max_length=64, default='Subscribe')
    button_subline = models.TextField(max_length=64, blank=True, null=True)
    popup_text = models.TextField(max_length=256, blank=True, null=True)
    newsletter = models.ForeignKey(Newsletter, blank=False, null=True)
    channel = models.CharField(max_length=32, default='general')
    redirect = PageField(verbose_name=_("redirect on success"), blank=True, null=True, help_text=_('Redirect to page after successfull subscription'))

    class Meta:
        app_label = 'subscription'
        #db_table = 'cmsplugin_faqmultilistplugin'

    def __unicode__(self):
        return self.channel
