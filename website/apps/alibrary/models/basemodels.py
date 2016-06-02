# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import tagging
import logging

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch.dispatcher import receiver
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from cms.models.fields import PlaceholderField
from phonenumber_field.modelfields import PhoneNumberField
from hvad.models import TranslatableModel, TranslatedFields
from hvad.manager import TranslationManager
from django_extensions.db.fields import UUIDField, AutoSlugField
from l10n.models import Country
from tagging.registry import register as tagging_register

from alibrary.util.slug import unique_slugify
from alibrary.util.relations import get_service_by_url
from lib.fields import extra
import uuid

log = logging.getLogger(__name__)

class MigrationMixin(models.Model):
    
    legacy_id = models.IntegerField(null=True, blank=True, editable=False)
    migrated = models.DateField(null=True, blank=True, editable=False)

    class Meta:
        abstract = True
        app_label = 'alibrary'
        verbose_name = _('MigrationMixin')
        verbose_name_plural = _('MigrationMixins')
        ordering = ('pk', )

class Distributor(MigrationMixin):

    # core fields
    #uuid = UUIDField(primary_key=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=400)
    slug = AutoSlugField(populate_from='name', editable=True, blank=True, overwrite=True)
    
    code = models.CharField(max_length=50)
    country = models.ForeignKey(Country, blank=True, null=True)
    
    address = models.TextField(blank=True, null=True)
    
    email = models.EmailField(blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    fax = PhoneNumberField(blank=True, null=True)
    
    description = extra.MarkdownTextField(blank=True, null=True)
    
    first_placeholder = PlaceholderField('first_placeholder')
    
    # auto-update
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)
    
    # relations
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')

    labels = models.ManyToManyField('Label', through='DistributorLabel', blank=True, related_name="distributors")
    
    # user relations
    owner = models.ForeignKey(User, blank=True, null=True, related_name="distributors_owner", on_delete=models.SET_NULL)
    creator = models.ForeignKey(User, blank=True, null=True, related_name="distributors_creator", on_delete=models.SET_NULL)
    publisher = models.ForeignKey(User, blank=True, null=True, related_name="distributors_publisher", on_delete=models.SET_NULL)
    
    TYPE_CHOICES = (
        ('unknown', _('Unknown')),
        ('major', _('Major')),
        ('indy', _('Independent')),
        ('other', _('Other')),
    )
    
    type = models.CharField(verbose_name="Distributor type", max_length=12, default='unknown', choices=TYPE_CHOICES)


    # relations a.k.a. links
    relations = generic.GenericRelation('Relation')
    
    # tagging (d_tags = "display tags")
    d_tags = tagging.fields.TagField(max_length=1024, verbose_name="Tags", blank=True, null=True)
 
    
    # manager
    objects = models.Manager()

    # meta
    class Meta:
        app_label = 'alibrary'
        verbose_name = _('Distributor')
        verbose_name_plural = _('Distributors')
        ordering = ('name', )

    def __unicode__(self):
        return self.name



    @models.permalink
    def get_absolute_url(self):
        return ('alibrary-distributor-detail', [self.slug])

    @models.permalink
    def get_edit_url(self):
        return ('alibrary-distributor-edit', [self.pk])
    

    def save(self, *args, **kwargs):
        unique_slugify(self, self.name)
        
        # update d_tags
        t_tags = ''
        for tag in self.tags:
            t_tags += '%s, ' % tag    
        
        self.tags = t_tags
        self.d_tags = t_tags
        
        super(Distributor, self).save(*args, **kwargs)

       
    
        
try:
    tagging_register(Distributor)
except Exception as e:
    print '***** %s' % e
    pass
        

class DistributorLabel(models.Model):
    distributor = models.ForeignKey('Distributor')
    label = models.ForeignKey('Label')
    exclusive = models.BooleanField(default=False)
    countries = models.ManyToManyField(Country, related_name="distribution_countries")
    class Meta:
        app_label = 'alibrary'
        verbose_name = _('Labels in catalog')
        verbose_name_plural = _('Labels in catalog')
        












class Agency(MigrationMixin):

    # core fields
    #uuid = UUIDField(primary_key=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=400)
    slug = AutoSlugField(populate_from='name', editable=True, blank=True, overwrite=True)

    country = models.ForeignKey(Country, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    email = models.EmailField(blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    fax = PhoneNumberField(blank=True, null=True)

    description = extra.MarkdownTextField(blank=True, null=True)

    # auto-update
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    # relations
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')

    artists = models.ManyToManyField('Artist', through='AgencyArtist', blank=True, related_name="agencies")

    # user relations
    owner = models.ForeignKey(User, blank=True, null=True, related_name="agencies_owner", on_delete=models.SET_NULL)
    creator = models.ForeignKey(User, blank=True, null=True, related_name="agencies_creator", on_delete=models.SET_NULL)
    publisher = models.ForeignKey(User, blank=True, null=True, related_name="agencies_publisher", on_delete=models.SET_NULL)

    TYPE_CHOICES = (
        ('unknown', _('Unknown')),
        ('major', _('Major Agency')),
        ('indy', _('Independent Agency')),
    )
    type = models.CharField(verbose_name="Agency type", max_length=12, default='unknown', choices=TYPE_CHOICES)

    # relations a.k.a. links
    relations = generic.GenericRelation('Relation')

    # tagging (d_tags = "display tags")
    d_tags = tagging.fields.TagField(max_length=1024, verbose_name="Tags", blank=True, null=True)


    # manager
    objects = models.Manager()

    # meta
    class Meta:
        app_label = 'alibrary'
        verbose_name = _('Agency')
        verbose_name_plural = _('Agencies')
        ordering = ('name', )

    def __unicode__(self):
        return self.name



    @models.permalink
    def get_absolute_url(self):
        if self.disable_link:
            return None

        return ('alibrary-agency-detail', [self.slug])

    @models.permalink
    def get_edit_url(self):
        return ('alibrary-agency-edit', [self.pk])


    def save(self, *args, **kwargs):

        unique_slugify(self, self.name)

        # update d_tags
        t_tags = ''
        for tag in self.tags:
            t_tags += '%s, ' % tag

        self.tags = t_tags;
        self.d_tags = t_tags;

        super(Agency, self).save(*args, **kwargs)




try:
    tagging.register(Agency)
except:
    pass


class AgencyScope(models.Model):
    name = models.CharField(max_length=300)
    class Meta:
        app_label = 'alibrary'
        verbose_name = _('Scope (Agency)')
        verbose_name_plural = _('Scopes (Agency)')

    def __unicode__(self):
        return self.name


class AgencyArtist(models.Model):
    agency = models.ForeignKey('Agency')
    artist = models.ForeignKey('Artist')
    exclusive = models.BooleanField(default=False)
    countries = models.ManyToManyField(Country, related_name="agency_countries")
    scopes = models.ManyToManyField(AgencyScope, related_name="agency_scopes")
    class Meta:
        app_label = 'alibrary'
        verbose_name = _('Managing')
        verbose_name_plural = _('Managing')



class License(TranslatableModel, MigrationMixin):
    
    name = models.CharField(max_length=200)
    
    slug = models.SlugField(max_length=100, unique=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    key = models.CharField(verbose_name=_("License key"), help_text=_("used e.g. for the icon-names"), max_length=36, blank=True, null=True)
    version = models.CharField(verbose_name=_("License version"), help_text=_("e.g. 2.5 CH"), max_length=36, blank=True, null=True)

    iconset =  models.CharField(verbose_name=_("Iconset"), help_text=_("e.g. cc-by, cc-nc, cc-sa"), max_length=36, blank=True, null=True)

    
    link = models.URLField(null=True, blank=True)
    
    restricted = models.NullBooleanField(null=True, blank=True)
    
    is_default = models.NullBooleanField(default=False, null=True, blank=True)
    selectable = models.NullBooleanField(default=True, null=True, blank=True)
    is_promotional = models.NullBooleanField(default=False, null=True, blank=True)


    translations = TranslatedFields(
        name_translated = models.CharField(max_length=200),
        excerpt = models.TextField(blank=True, null=True),
        license_text = models.TextField(blank=True, null=True)
    )

    
    # auto-update
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    parent = models.ForeignKey('self', null=True, blank=True, related_name='license_children')

    objects = TranslationManager()


    class Meta:
        app_label = 'alibrary'
        verbose_name = _('License')
        verbose_name_plural = _('Licenses')
        ordering = ('parent__name', 'name', )

    def __unicode__(self):
        if self.parent:
            return '%s - %s' % (self.parent.name, self.name)
        else:
            return '%s' % (self.name)


    def get_absolute_url(self):
        return reverse('alibrary-license-detail', args=(self.slug,))

    def get_admin_url(self):
        return reverse("admin:alibrary_license_change", args=(self.pk,))

    @property
    def iconset_display(self):
        from django.utils.html import mark_safe
        html = ''
        if self.iconset:
            icons = self.iconset.split(',')
            for icon in icons:
                html += '<i class="icon icon-license-%s"></i>' % icon.strip(' ')

        return mark_safe(html)


class ProfessionManager(models.Manager):

    def listed(self):
        return self.get_queryset().filter(in_listing=True)
    
    
class Profession(models.Model):
    
    name = models.CharField(max_length=200)
    
    in_listing = models.BooleanField(default=True, verbose_name='Include in listings')
    
    excerpt = models.TextField(blank=True, null=True)  
    
    # auto-update
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    objects = ProfessionManager()

    # meta
    class Meta:
        app_label = 'alibrary'
        verbose_name = _('Role/Profession')
        verbose_name_plural = _('Roles/Profession')
        ordering = ('name', )
    
    def __unicode__(self):
        return self.name

class DaypartManager(models.Manager):
    
    def active(self):
        return self.get_queryset().filter(active=True)
       
class Daypart(models.Model):
    
    
    active = models.BooleanField(default=True)
    
    DAY_CHOICES = (
        (0, _('Mon')),
        (1, _('Tue')),
        (2, _('Wed')),
        (3, _('Thu')),
        (4, _('Fri')),
        (5, _('Sat')),
        (6, _('Sun')),
    )
    day = models.PositiveIntegerField(default=0, null=True, choices=DAY_CHOICES)
    time_start = models.TimeField()
    time_end = models.TimeField()
    
    
    
    # manager
    objects = DaypartManager()

    # meta
    class Meta:
        app_label = 'alibrary'
        verbose_name = _('Daypart')
        verbose_name_plural = _('Dayparts')
        ordering = ('day', 'time_start' )
    
    def __unicode__(self):
        return "%s | %s - %s" % (self.get_day_display(), self.time_start, self.time_end)
    
    def playlist_count(self):
        return self.daypart_plalists.count()
    
    



class Service(models.Model):
    
    name = models.CharField(max_length=200)
    key = models.CharField(max_length=200, blank=True, null=True)
    pattern = models.CharField(max_length=256, null=True, blank=True, help_text='Regex to match url against. eg ""')
    
    class Meta:
        app_label = 'alibrary'
        verbose_name = _('Service')
        verbose_name_plural = _('Services')
        ordering = ('name', )
    
    def __unicode__(self):
        return '%s - "%s"' % (self.name, self.pattern)
    
    

class RelationManager(models.Manager):

    def generic(self):
        qs = self.get_queryset().filter(service__in=['generic', 'official',])
        return qs.order_by('-service')

    def specific(self, key=None):

        qs = self.get_queryset().exclude(service__in=['generic', 'official',])

        """
        try to order by dict
        """
        services = [
                    'discogs_master',
                    'discogs',
                    'musicbrainz',
                    'wikipedia',
                    'soundcloud',
                    'bandcamp',
                    'lastfm',
                    'youtube',
                    'itunes',
                    'facebook',
                    'twitter',
                    'linkedin',
                    ]

        objects = {obj.service: obj for obj in qs}

        sorted = []
        for service in services:
            if service in objects:
                sorted.append(objects[service])

        return sorted

    def highlighted(self, key=None):

        qs = self.get_queryset().exclude(service__in=['generic', 'official',])

        objects = {obj.service: obj for obj in qs}

        sorted = []
        for service in ['wikipedia', 'youtube',]:
            if service in objects:
                sorted.append(objects[service])

        return sorted


    
class Relation(models.Model):
    
    name = models.CharField(max_length=200, blank=True, null=True, help_text=(_('Additionally override the name.')))
    url = models.URLField(max_length=512)

    content_type = models.ForeignKey(ContentType)
    object_id = UUIDField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    SERVICE_CHOICES = (
        ('', _('Not specified')),
        ('generic', _('Generic')),
        ('facebook', _('Facebook')),
        ('youtube', _('YouTube')),
        ('discogs', _('Discogs')),
        ('lastfm', _('Last.fm')),
        ('linkedin', _('Linked In')),
        ('soundcloud', _('Soundcloud')),
        ('twitter', _('Twitter')),
        ('discogs_master', _('Discogs | master-release')),
        ('wikipedia', _('Wikipedia')),
        ('musicbrainz', _('Musicbrainz')),
        ('bandcamp', _('Bandcamp')),
        ('itunes', _('iTunes')),
        ('official', _('Official website')),
    )
    service = models.CharField(
        max_length=50,
        choices=SERVICE_CHOICES, blank=True, null=True, editable=True,
        default='generic',
        db_index=True
    )

    ACTION_CHOICES = (
        ('information', _('Information')),
        ('buy', _('Buy')),
    )
    action = models.CharField(max_length=50, default='information', choices=ACTION_CHOICES)

    @property
    def _service(cls):
        return cls.service

    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    objects = RelationManager()

    class Meta:
        app_label = 'alibrary'
        verbose_name = _('Relation')
        verbose_name_plural = _('Relations')
        ordering = ('url', )
    
    def __unicode__(self):
        return self.url

    def save(self, *args, **kwargs):

        self.service = get_service_by_url(self.url, self.service)

        # find already assigned services and delete them
        if self.service != 'generic':
            # TODO: fix unique problem
            Relation.objects.filter(service=self.service, content_type=self.content_type, object_id=self.object_id).delete()

        super(Relation, self).save(*args, **kwargs)    
        


    @property
    def service_icon(self):
        icon = self.service

        if icon == 'itunes':
            icon = 'apple'

        if icon == 'youtube':
            icon = 'youtube-play'

        if icon == 'discogs_master':
            icon = 'discogs'

        return icon


@receiver(post_save, sender=Relation)
def relation_post_save(sender, instance, signal, created, **kwargs):
    if instance.url[-4:] == 'None':
        #log.debug('deleting wrongly formated relation')
        instance.delete()

def update_relations():
    rs = Relation.objects.all()
    for r in rs:
        r.save()
