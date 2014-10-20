#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django_extensions.db.fields import *
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.urlresolvers import reverse

from cms.models import CMSPlugin

# filer
from filer.fields.image import FilerImageField
from filer.fields.file import FilerFileField

import arating

from phonenumber_field.modelfields import PhoneNumberField
from l10n.models import Country

from abcast.util import notify

# 
from lib.fields import extra

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


    # members
    members = models.ManyToManyField(User, through='StationMembers', blank=True, null=True)

    # stations contact information
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
        return ('abcast-station-detail', [self.slug])

    """
    @models.permalink
    def get_edit_url(self):
        return ('alibrary-artist-edit', [self.pk])
    """

    def get_admin_url(self):
        from lib.util.get_admin_url import change_url
        return change_url(self)


arating.enable_voting_on(Station)



class Role(BaseModel):

    name = models.CharField(max_length=200)

    # meta
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
    # role = models.ForeignKey(Role, blank=True, null=True)
    roles = models.ManyToManyField(Role, blank=True, null=True, related_name='memgership_roles')

    class Meta:
        app_label = 'abcast'
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')



    
"""
Holds what is on air right now
"""
class OnAirItem(BaseModel):

    #channel = models.ForeignKey('Channel')

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        app_label = 'abcast'
        verbose_name = _('On Air')
        verbose_name_plural = _('On Air')
        unique_together = ('content_type', 'object_id',)
        #ordering = ('name', )

    def __unicode__(self):
        return "%s : %s" % (self.channel.pk, self.channel.pk)


"""
A bit verbose, as already channel in bcmon - but different type of app f.t.m.
"""
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


    """
    RTMP settings
    """
    rtmp_app = models.CharField(max_length=256, null=True, blank=True)
    rtmp_path = models.CharField(max_length=256, null=True, blank=True)

    """
    settings for 'owned' channels
    """
    has_scheduler = models.BooleanField(default=False)
    stream_server = models.ForeignKey('StreamServer', null=True, blank=True, on_delete=models.SET_NULL)
    mount = models.CharField(max_length=64, null=True, blank=True)

    # on_air = JSONField(null=True, blank=True)
    # on_air = generic.GenericRelation(OnAirItem, object_id_field="object_id")
    on_air_type = models.ForeignKey(ContentType, null=True, blank=True)
    on_air_id = models.PositiveIntegerField(null=True, blank=True)
    on_air = generic.GenericForeignKey('on_air_type', 'on_air_id')

    
    class Meta:
        app_label = 'abcast'
        verbose_name = _('Channel')
        verbose_name_plural = _('Channels')
        ordering = ('name', )
        unique_together = ('on_air_type', 'on_air_id')

    def __unicode__(self):
        return "%s" % self.name

    @models.permalink
    def get_absolute_url(self):
        return ('abcast-channel-detail', [self.pk])
    
    def get_api_url(self):
        return reverse('api_dispatch_detail', kwargs={  
            'api_name': 'v1',  
            'resource_name': 'abcast/channel',  
            'pk': self.pk  
        }) + ''
        
        
    def get_stream_url(self, format=None):
        
        if self.stream_url:
            return self.stream_url

        if self.stream_server:
            stream_server = self.stream_server
            format = self.stream_server.formats.all()[0]

            return '%s%s-%s.%s' % (stream_server.host, self.mount, format.bitrate, format.type)

        return None


    def get_dayparts(self, day):
        dayparts = []
        daypart_sets = self.daypartset_set.filter(time_start__lte=day, time_end__gte=day, channel=self)
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
    print 'post_save_channel - kwargs'
    obj = kwargs['instance']

    # call notification
    try:
        notify.start_play(obj.on_air, obj)
    except:
        pass

post_save.connect(post_save_channel, sender=Channel)





class StreamServer(BaseModel):
    
    name = models.CharField(max_length=256, null=True, blank=False)     
    host = models.URLField(max_length=256, null=True, blank=False) 
    source_pass = models.CharField(max_length=64, null=True, blank=True)
    admin_pass = models.CharField(max_length=64, null=True, blank=True)
    
    active = models.BooleanField(default=True)
    mountpoint = models.CharField(max_length=64, null=True, help_text=_('e.g. main-hifi.mp3'))
    meta_prefix = models.CharField(max_length=64, null=True, blank=True, help_text=_('e.g. My Station!'))


    formats = models.ManyToManyField('StreamFormat', null=True, blank=True)

    
    
     
    TYPE_CHOICES = (
        ('icecast2', _('Icecast 2')),
        ('rtmp', _('RTMP / Wowza')),
    )
    type = models.CharField(verbose_name=_('Type'), max_length=12, default='icecast2', choices=TYPE_CHOICES)
    
    
    class Meta:
        app_label = 'abcast'
        verbose_name = _('Streaming server')
        verbose_name_plural = _('Streaming servers')
        ordering = ('name', )

    def __unicode__(self):
        return "%s" % self.name

"""
class StreamMountpoint(BaseModel):

    server = models.ForeignKey(StreamServer, null=True, blank=True)
    path = models.CharField(max_length=64, null=True, help_text=_('e.g. main-hifi.mp3'))


    class Meta:
        app_label = 'abcast'
        verbose_name = _('Mountpoint')
        ordering = ('server', 'path',)
"""


class StreamFormat(BaseModel):

    TYPE_CHOICES = (
        ('mp3', _('MP3')),
        ('ogg', _('ogg/vorbis')),
        ('aac', _('AAC')),
    )
    type = models.CharField(max_length=12, default='mp3', choices=TYPE_CHOICES)
    BITRATE_CHOICES = (
        (64, _('64 kbps')),
        (96, _('96 kbps')),
        (128, _('128 kbps')),
        (160, _('160 kbps')),
        (192, _('192 kbps')),
        (256, _('256 kbps')),
        (320, _('320 kbps')),
    )
    bitrate = models.PositiveIntegerField(default=256, choices=BITRATE_CHOICES)
    
    
    class Meta:
        app_label = 'abcast'
        verbose_name = _('Streaming format')
        verbose_name_plural = _('Streaming formats')
        ordering = ('type', )

    def __unicode__(self):
        return "%s | %s" % (self.type, self.bitrate)

"""
class StreamMount(BaseModel):

    TYPE_CHOICES = (
        ('icecast2', _('Icecast 2')),
        ('rtmp', _('RTMP / Wowza')),
    )
    type = models.CharField(max_length=12, default='icecast2', choices=TYPE_CHOICES)
    formats = models.ManyToManyField('StreamFormat', null=True, blank=True)
    active = models.BooleanField(default=True)
    
    stream_url = models.URLField(null=True, blank=True, max_length=256, help_text=_('stream-url has priority over streams-erver'))
    stream_server = models.ForeignKey('StreamServer', null=True, blank=True, on_delete=models.SET_NULL)

    # url is either generated through an assigned stream-server, or the given stream-url.
    # the stream-url has priority.
    
    @property
    def url(selfself):
        if self.stream_url:
            return self.stream_url
        
        if self.stream_server:
            return self.stream_server.host
        
        return None
            
    class Meta:
        app_label = 'abcast'
        verbose_name = _('Mountpoint')
        verbose_name_plural = _('Mountpoints')
        ordering = ('type', )

    def __unicode__(self):
        return "%s | %s" % (self.type, self.bitrate)
"""    
    
    

class OnAirPlugin(CMSPlugin):    
    channel = models.ForeignKey(Channel, related_name='plugins')
    show_channel_info = models.BooleanField(default=True)
    class Meta:
        app_label = 'abcast'

    def __unicode__(self):
        return "%s" % self.channel.name

