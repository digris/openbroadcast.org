#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime

from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django_extensions.db.fields import *

from celery.task import task

from cms.models import CMSPlugin

# filer
from filer.fields.image import FilerImageField
from filer.fields.file import FilerFileField


# 
from lib.fields import extra

from alibrary.models import Playlist

from abcast.models import BaseModel, Channel


from caching.base import CachingMixin, CachingManager

USE_CELERY = True

class Broadcast(BaseModel):
    
    # core fields
    name = models.CharField(max_length=200, db_index=True)
    slug = AutoSlugField(populate_from='name', editable=True, blank=True, overwrite=True)

    STATUS_CHOICES = (
        (0, _('Waiting')),
        (1, _('Done')),
        (2, _('Error')),
    )
    status = models.PositiveIntegerField(max_length=2, default=0, choices=STATUS_CHOICES)

    TYPE_CHOICES = (
        ('studio', _('Studio')),
        ('playlist', _('Playlist')),
        ('couchcast', _('Couchcast')),
    )
    type = models.CharField(verbose_name=_('Type'), max_length=12, default='jingle', choices=TYPE_CHOICES)
    
    description = models.TextField(verbose_name="Extra Description", blank=True, null=True)
    duration = models.PositiveIntegerField(verbose_name="Duration (in ms)", max_length=12, blank=True, null=True, editable=True)
    
    # relations
    user = models.ForeignKey(User, blank=True, null=True, related_name="scheduler_broadcasts", on_delete=models.SET_NULL)

    # REFACTORED: playlist not used, modeled via emission -> co
    playlist = models.ForeignKey(Playlist, blank=True, null=True, related_name="scheduler_broadcasts", on_delete=models.SET_NULL)

    # manager
    objects = models.Manager()

    class Meta:
        app_label = 'abcast'
        verbose_name = _('Broadcast')
        verbose_name_plural = _('Broadcasts')
        ordering = ('created', )
    
    
    def __unicode__(self):
        return u'%s' % self.name


#class EmissionManager(CachingManager):
class EmissionManager(models.Manager):

    def future(self):
        now = datetime.datetime.now()
        return self.get_query_set().filter(time_end__gte=now)

    def past(self):
        now = datetime.datetime.now()
        return self.get_query_set().filter(time_end__lt=now)




#class Emission(BaseModel, CachingMixin):
class Emission(BaseModel):

    # core fields
    name = models.CharField(max_length=200, db_index=True)
    slug = AutoSlugField(populate_from='name', editable=True, blank=True, overwrite=True)

    STATUS_CHOICES = (
        (0, _('Waiting')),
        (1, _('Done')),
        (2, _('Error')),
    )
    status = models.PositiveIntegerField(max_length=2, default=0, choices=STATUS_CHOICES)
    
    COLOR_CHOICES = (
        (0, _('Theme 1')),
        (1, _('Theme 2')),
        (2, _('Theme 3')),
        (3, _('Theme 4')),
    )
    color = models.PositiveIntegerField(max_length=2, default=0, choices=COLOR_CHOICES)

    TYPE_CHOICES = (
        ('studio', _('Studio')),
        ('playlist', _('Playlist')),
        ('couchcast', _('Couchcast')),
    )
    type = models.CharField(verbose_name=_('Type'), max_length=12, default='playlist', choices=TYPE_CHOICES)

    SOURCE_CHOICES = (
        ('user', _('User')),
        ('autopilot', _('Autopilot')),
    )
    source = models.CharField(verbose_name=_('Source'), max_length=12, default='user', choices=SOURCE_CHOICES)
    
    
    time_start = models.DateTimeField(blank=True, null=True)
    time_end = models.DateTimeField(blank=True, null=True)
    
    # eventually use this
    duration = models.PositiveIntegerField(verbose_name="Duration (in ms)", max_length=12, blank=True, null=True, editable=False)
    
    
    # relations
    user = models.ForeignKey(User, blank=True, null=True, related_name="scheduler_emissions", on_delete=models.SET_NULL)
    channel = models.ForeignKey(Channel, blank=True, null=True, related_name="scheduler_emissions", on_delete=models.SET_NULL)
    
    
    """
    content
    content objects have to implement certain methosds/properties:
     - get_duration()
     - t.b.d.
    """
    ct_limit = models.Q(app_label = 'alibrary', model = 'playlist') | models.Q(app_label = 'alibrary', model = 'release')
    content_type = models.ForeignKey(ContentType, limit_choices_to = ct_limit)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    locked = models.BooleanField(default=False)

    
    # manager
    objects = EmissionManager()

    class Meta:
        app_label = 'abcast'
        verbose_name = _('Emission')
        verbose_name_plural = _('Emissions')
        ordering = ('created', )

        permissions = (
            ('schedule_emission', 'Schedule Emission'),
        )
    
    
    def __unicode__(self):
        return u'%s' % self.name
    
    
    @models.permalink
    def get_absolute_url(self):      
        return ('abcast-emission-detail', [self.pk])
    
    
    def get_api_url(self):
        return reverse('api_dispatch_detail', kwargs={  
            'api_name': 'v1',  
            'resource_name': 'abcast/emission',  
            'pk': self.pk  
        }) + ''


    def get_api_list_url(self):
        return reverse('api_dispatch_list', kwargs={
            'api_name': 'v1',
            'resource_name': 'abcast/emission',
        })



    @property
    def has_lock(self):

        return False

        if self.locked:
            return self.locked
        
        lock = False
        if self.time_start < datetime.datetime.now():
            lock = True
        return lock
    
    @property
    def is_playing(self):
        playing = False
        if self.time_start < datetime.datetime.now() and datetime.datetime.now() < self.time_end:
            playing = True
        return playing


    def get_timestamped_media(self):

        items = self.content_object.get_items()
        offset = 0
        for item in items:
            item.timestamp = self.time_start + datetime.timedelta(milliseconds=offset)
            if item.timestamp > datetime.datetime.now():
                item.is_future = True
            offset += item.playout_duration

        return items



    def save(self, *args, **kwargs):
        
        print 'save'
        print self.content_object
        
        if not self.name:
            self.name = self.content_object.name
        
        
        self.duration = self.content_object.get_duration()
        
        print 'duration: %s' % self.content_object.get_duration()
        
        if self.duration:
            self.time_end = self.time_start + datetime.timedelta(milliseconds=self.duration)
        
        
        super(Emission, self).save(*args, **kwargs)
        



def post_save_emission(sender, **kwargs):

    obj = kwargs['instance']

    if USE_CELERY:
        post_save_emission_task.delay(obj)
    else:
        post_save_emission_task(obj)


@task
def post_save_emission_task(obj):

        """
        check if emission is in a critical range (eg it should start soon)
        """
        SCHEDULE_AHEAD = 60 * 60 * 3 # seconds
        range_start = datetime.datetime.now()
        range_end = datetime.datetime.now() + datetime.timedelta(seconds=SCHEDULE_AHEAD)

        # TODO: think about calculation
        # if obj.time_start > range_start and obj.time_start < range_end:
        if obj.time_end > range_start and obj.time_start < range_end:
            # notify pypy
            print 'emission in critical range: notify pypo'
            from lib.pypo_gateway import send as pypo_send
            from abcast.util import scheduler
            data = scheduler.get_schedule_for_pypo(range_start=range_start, range_end=range_end)

            message = {
                'event_type': 'update_schedule',
                'schedule': {'media': data},
            }
            pypo_send(message)
        else:
            print 'emission NOT in critical range: pass'


post_save.connect(post_save_emission, sender=Emission)


def pre_delete_emission(sender, **kwargs):
    print 'post_save_emission - kwargs'
    obj = kwargs['instance']

    """
    check if emission is in a critical range (eg it should start soon)
    """
    SCHEDULE_AHEAD = 60 * 60 * 3 # seconds
    range_start = datetime.datetime.now()
    range_end = datetime.datetime.now() + datetime.timedelta(seconds=SCHEDULE_AHEAD)

    # TODO: think about calculation
    # if obj.time_start > range_start and obj.time_start < range_end:

    if not obj or not obj.time_end or not obj.time_start:
        return

    if obj.time_end > range_start and obj.time_start < range_end:
        # notify pypy
        print 'emission in critical range: notify pypo'
        from lib.pypo_gateway import send as pypo_send
        from abcast.util import scheduler
        data = scheduler.get_schedule_for_pypo(range_start=range_start, range_end=range_end, exclude=[obj.pk])

        message = {
            'event_type': 'update_schedule',
            'schedule': {'media': data},
        }
        pypo_send(message)
    else:
        print 'emission NOT in critical range: pass'


pre_delete.connect(pre_delete_emission, sender=Emission)
        
        
        
class DaypartSet(BaseModel):
    
    channel = models.ForeignKey(Channel, blank=False, null=True, related_name="daypartset_set", on_delete=models.SET_NULL)

    time_start = models.DateField(blank=False, null=True)
    time_end = models.DateField(blank=False, null=True)

    class Meta:
        app_label = 'abcast'
        verbose_name = _('Daypart set')
        verbose_name_plural = _('Daypart sets')
        ordering = ('created', )
    
    
    def __unicode__(self):
        return u'%s' % self.time_start
        



class Weekday(models.Model):

    DAY_CHOICES = (
        (1, _('Sun')),
        (2, _('Mon')),
        (3, _('Tue')),
        (4, _('Wed')),
        (5, _('Thu')),
        (6, _('Fri')),
        (7, _('Sat')),
    )
    day = models.PositiveIntegerField(max_length=1, default=1, null=False, choices=DAY_CHOICES)

    class Meta:
        app_label = 'abcast'
        verbose_name = _('Weekay')
        verbose_name_plural = _('Weekays')
        ordering = ('day', )
    
    
    def __unicode__(self):
        return u'%s' % self.get_day_display()
    

class Daypart(BaseModel):

    DAY_CHOICES = (
        (0, _('Mon')),
        (1, _('Tue')),
        (2, _('Wed')),
        (3, _('Thu')),
        (4, _('Fri')),
        (5, _('Sat')),
        (6, _('Sun')),
    )
    daypartset = models.ForeignKey(DaypartSet, blank=False, null=True, on_delete=models.SET_NULL)
    weekdays = models.ManyToManyField(Weekday, null=True, blank=True)
    
    time_start = models.TimeField()
    time_end = models.TimeField()
    
    name = models.CharField(max_length=128, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    mood = models.TextField(null=True, blank=True)
    sound = models.TextField(null=True, blank=True)
    talk = models.TextField(null=True, blank=True)

    position = models.PositiveIntegerField(default=1, choices=((0, '0'),(1, '1'),(2, '2'),(3, '3'),))
    
    @property
    def duration(self):
        duration = (self.time_end.hour - self.time_start.hour)
        if duration < 0:
            duration = 24 + duration
        return duration

    class Meta:
        app_label = 'abcast'
        verbose_name = _('Daypart')
        verbose_name_plural = _('Dayparts')
        ordering = ('created', )
        ordering = ('position', 'time_start', )
    
    
    def __unicode__(self):
        return u'%s - %s' % (self.time_start, self.time_end)
        
        
    