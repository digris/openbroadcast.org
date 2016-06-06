# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import arating
from abcast.util import notify
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext as _
from django_extensions.db.fields import UUIDField, CreationDateTimeField, ModificationDateTimeField, AutoSlugField
from filer.fields.image import FilerImageField
from l10n.models import Country
from lib.fields import extra
from phonenumber_field.modelfields import PhoneNumberField


class BaseModel(models.Model):
    
    uuid = UUIDField()
    created = CreationDateTimeField()
    updated = ModificationDateTimeField()
    
    class Meta:
        abstract = True


class Station(BaseModel):

    name = models.CharField(max_length=256, null=True, blank=True)
    teaser = models.CharField(max_length=512, null=True, blank=True)
    slug = AutoSlugField(populate_from='name')
    
    TYPE_CHOICES = (
        ('stream', _('Stream')),
        ('djmon', _('DJ-Monitor')),
    )
    type = models.CharField(verbose_name=_('Type'), max_length=12, default='stream', choices=TYPE_CHOICES)
    
    main_image = FilerImageField(null=True, blank=True, related_name="station_main_image", rel='')
    description = extra.MarkdownTextField(blank=True, null=True)
    members = models.ManyToManyField(User, through='StationMembers', blank=True)
    website = models.URLField(max_length=256, null=True, blank=True)
    phone = PhoneNumberField(_('phone'), blank=True, null=True)
    fax = PhoneNumberField(_('fax'), blank=True, null=True)
    address1 = models.CharField(_('address'), null=True, blank=True, max_length=100)
    address2 = models.CharField(_('address (secondary)'), null=True, blank=True, max_length=100)
    city = models.CharField(_('city'), null=True, blank=True, max_length=100)
    zip = models.CharField(_('zip'), null=True, blank=True, max_length=10)
    country = models.ForeignKey(Country, blank=True, null=True)

    class Meta:
        app_label = 'abcast'
        verbose_name = _('Station')
        verbose_name_plural = _('Stations')
        ordering = ('name', )

    def __unicode__(self):
        return "%s" % self.name

    @models.permalink
    def get_absolute_url(self):
        return 'abcast-station-detail', [self.slug]

    def get_admin_url(self):
        return reverse("admin:abcast_station_change", args=(self.pk,))


arating.enable_voting_on(Station)



class Role(BaseModel):

    name = models.CharField(max_length=200)

    class Meta:
        app_label = 'abcast'
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')
        ordering = ('name', )

    def __unicode__(self):
        return self.name


class StationMembers(models.Model):
    user = models.ForeignKey(User, related_name='station_membership')
    station = models.ForeignKey(Station)
    roles = models.ManyToManyField(Role, blank=True, related_name='memgership_roles')

    class Meta:
        app_label = 'abcast'
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')

    
"""
Holds what is on air right now
"""
class OnAirItem(BaseModel):

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        app_label = 'abcast'
        verbose_name = _('On Air')
        verbose_name_plural = _('On Air')
        unique_together = ('content_type', 'object_id',)

    def __unicode__(self):
        return "%s : %s" % (self.channel.pk, self.channel.pk)


class Channel(BaseModel):

    name = models.CharField(max_length=256, null=True, blank=True)
    teaser = models.CharField(max_length=512, null=True, blank=True)
    slug = AutoSlugField(populate_from='name')
    
    TYPE_CHOICES = (
        ('stream', _('Stream')),
        ('djmon', _('DJ-Monitor')),
    )
    type = models.CharField(verbose_name=_('Type'), max_length=12, default='stream', choices=TYPE_CHOICES)
    
    stream_url = models.CharField(max_length=256, null=True, blank=True, help_text=_('setting the stream-url overrides server settings'))
    description = extra.MarkdownTextField(blank=True, null=True)
    station = models.ForeignKey('Station', null=True, blank=True, on_delete=models.SET_NULL)
    rtmp_app = models.CharField(max_length=256, null=True, blank=True)
    rtmp_path = models.CharField(max_length=256, null=True, blank=True)
    has_scheduler = models.BooleanField(default=False)
    mount = models.CharField(max_length=64, null=True, blank=True)

    tunein_station_id = models.CharField(max_length=16, null=True, blank=True)
    tunein_partner_id = models.CharField(max_length=16, null=True, blank=True)
    tunein_partner_key = models.CharField(max_length=16, null=True, blank=True)

    on_air_type = models.ForeignKey(ContentType, null=True, blank=True)
    on_air_id = models.PositiveIntegerField(null=True, blank=True)
    on_air = GenericForeignKey('on_air_type', 'on_air_id')

    class Meta:
        app_label = 'abcast'
        verbose_name = _('Channel')
        verbose_name_plural = _('Channels')
        ordering = ('name', )
        unique_together = ('on_air_type', 'on_air_id')

    def __unicode__(self):
        return "%s" % self.name


    def get_absolute_url(self):
        return reverse('abcast-station-detail', kwargs={
            'slug': self.station.slug
        })
    
    def get_api_url(self):
        return reverse('api_dispatch_detail', kwargs={  
            'api_name': 'v1',  
            'resource_name': 'abcast/channel',  
            'pk': self.pk  
        }) + ''

    def get_dayparts(self, day):
        dayparts = []
        daypart_sets = self.daypartsets.filter(time_start__lte=day, time_end__gte=day, channel=self)
        daypart_set = None
        if daypart_sets.count() > 0:
            daypart_set = daypart_sets[0]

        if daypart_set:
            for dp in daypart_set.daypart_set.all():
                dayparts.append(dp)
        
        return dayparts


    def get_on_air(self):
        """
        merge currently playing item (told by pypo) with estimated scheduler entry for the emission
        """
        now = datetime.datetime.now()
        emissions = self.scheduler_emissions.filter(channel__pk=self.pk, time_start__lte=now, time_end__gte=now)
        if emissions.count() > 0:

            emission = emissions[0]
            emission_url = emissions[0].get_api_url()

            emission_items = []
            """
            for e in emission.get_timestamped_media():
                item = e.content_object
                emission_items.append({
                    'pk': item.pk,
                    'time_start': e.timestamp,
                    'resource_uri': item.get_api_url()
                })
            """

        else:
            emission_url = None
            emission_items = []

        try:
            item_url = self.on_air.get_api_url()
        except:
            item_url = None

        on_air = {
            'item': item_url,
            'emission': emission_url,
            'emission_items': emission_items
        }

        return on_air


def post_save_channel(sender, **kwargs):

    obj = kwargs['instance']
    try:
        notify.start_play(obj.on_air, obj)
    except Exception as e:
        pass

post_save.connect(post_save_channel, sender=Channel)

