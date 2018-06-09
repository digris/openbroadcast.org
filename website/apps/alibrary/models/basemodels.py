# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import tagging
import logging
import uuid

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from phonenumber_field.modelfields import PhoneNumberField
from hvad.models import TranslatableModel, TranslatedFields
from hvad.manager import TranslationManager
from django_extensions.db.fields import AutoSlugField
from l10n.models import Country
from tagging.registry import register as tagging_register

from alibrary.util.slug import unique_slugify
from alibrary.util.relations import get_service_by_url
from base.fields import extra
from base.mixins import TimestampedModelMixin, UUIDModelMixin


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


class Distributor(MigrationMixin, UUIDModelMixin, TimestampedModelMixin, models.Model):
    """
    TODO: suggest to remove 'distributor' implementation.
    it is not used at the moment (90 entries, last 2014...)
    """

    TYPE_CHOICES = (
        ('unknown', _('Unknown')),
        ('major', _('Major')),
        ('indy', _('Independent')),
        ('other', _('Other')),
    )

    type = models.CharField(
        verbose_name="Distributor type",
        max_length=12, default='unknown',
        choices=TYPE_CHOICES
    )
    slug = AutoSlugField(
        populate_from='name',
        editable=True, blank=True, overwrite=True
    )
    name = models.CharField(
        max_length=400
    )
    description = extra.MarkdownTextField(
        blank=True, null=True
    )
    code = models.CharField(
        max_length=50
    )
    address = models.TextField(
        blank=True, null=True
    )
    email = models.EmailField(
        blank=True, null=True
    )
    phone = PhoneNumberField(
        blank=True, null=True
    )
    fax = PhoneNumberField(
        blank=True, null=True
    )
    country = models.ForeignKey(
        Country,
        blank=True, null=True
    )

    # relations
    parent = models.ForeignKey(
        'self',
        null=True, blank=True,
        related_name='children'
    )
    labels = models.ManyToManyField(
        'Label',
        through='DistributorLabel', blank=True,
        related_name="distributors"
    )
    relations = GenericRelation('Relation')
    d_tags = tagging.fields.TagField(
        verbose_name="Tags",
        max_length=1024, blank=True, null=True
    )

    objects = models.Manager()

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

        t_tags = ''
        for tag in self.tags:
            t_tags += '%s, ' % tag

        self.tags = t_tags
        self.d_tags = t_tags

        super(Distributor, self).save(*args, **kwargs)


try:
    tagging_register(Distributor)
except Exception as e:
    pass


class DistributorLabel(models.Model):

    distributor = models.ForeignKey(
        'Distributor'
    )
    label = models.ForeignKey(
        'Label'
    )
    exclusive = models.BooleanField(
        default=False
    )
    countries = models.ManyToManyField(
        Country,
        related_name="distribution_countries"
    )

    class Meta:
        app_label = 'alibrary'
        verbose_name = _('Labels in catalog')
        verbose_name_plural = _('Labels in catalog')



class License(TranslatableModel, MigrationMixin, UUIDModelMixin, TimestampedModelMixin, models.Model):

    slug = models.SlugField(
        max_length=100, unique=False
    )
    name = models.CharField(
        max_length=200
    )
    key = models.CharField(
        verbose_name=_("License key"),
        max_length=36, blank=True, null=True,
        help_text=_("used e.g. for the icon-names")
    )
    restricted = models.NullBooleanField(
        null=True, blank=True
    )
    version = models.CharField(
        verbose_name=_("License version"),
        max_length=36, blank=True, null=True,
        help_text=_("e.g. 2.5 CH")
    )
    iconset =  models.CharField(
        verbose_name=_("Iconset"),
        max_length=36, blank=True, null=True,
        help_text=_("e.g. cc-by, cc-nc, cc-sa")
    )
    link = models.URLField(
        null=True, blank=True
    )
    parent = models.ForeignKey(
        'self',
        null=True, blank=True,
        related_name='license_children'
    )
    is_default = models.NullBooleanField(
        default=False, null=True, blank=True
    )
    selectable = models.NullBooleanField(
        default=True, null=True, blank=True
    )
    is_promotional = models.NullBooleanField(
        default=False, null=True, blank=True
    )

    translations = TranslatedFields(
        name_translated = models.CharField(max_length=200),
        excerpt = models.TextField(blank=True, null=True),
        license_text = models.TextField(blank=True, null=True)
    )

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


class Profession(TimestampedModelMixin, models.Model):

    name = models.CharField(
        max_length=200
    )
    in_listing = models.BooleanField(
        verbose_name='Include in listings',
        default=True,
    )
    excerpt = models.TextField(
        blank=True, null=True
    )

    objects = ProfessionManager()

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

    DAY_CHOICES = (
        (0, _('Mon')),
        (1, _('Tue')),
        (2, _('Wed')),
        (3, _('Thu')),
        (4, _('Fri')),
        (5, _('Sat')),
        (6, _('Sun')),
    )

    day = models.PositiveIntegerField(
        default=0, null=True,
        choices=DAY_CHOICES
    )
    time_start = models.TimeField()
    time_end = models.TimeField()
    active = models.BooleanField(
        default=True
    )

    objects = DaypartManager()

    class Meta:
        app_label = 'alibrary'
        verbose_name = _('Daypart')
        verbose_name_plural = _('Dayparts')
        ordering = ('day', 'time_start' )

    def __unicode__(self):
        return "%s | %s - %s" % (self.get_day_display(), self.time_start, self.time_end)

    def playlist_count(self):
        return self.daypart_plalists.count()



class RelationManager(models.Manager):

    def generic(self):
        qs = self.get_queryset().filter(service__in=['generic', 'official',])
        return qs.order_by('-service')

    def specific(self, key=None):

        qs = self.get_queryset().exclude(service__in=['generic', 'official',])

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
            'imdb',
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



class Relation(TimestampedModelMixin, models.Model):

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
        ('imdb', _('IMDb')),
        ('wikidata', _('wikidata')),
        ('viaf', _('VIAF')),
        ('official', _('Official website')),
        ('vimeo', _('Vimeo')),
        ('instagram', _('Instagram')),
    )

    ACTION_CHOICES = (
        ('information', _('Information')),
        ('buy', _('Buy')),
    )

    service = models.CharField(
        max_length=50,
        choices=SERVICE_CHOICES, blank=True, null=True, editable=True,
        default='generic',
        db_index=True
    )
    action = models.CharField(
        max_length=50, default='information',
        choices=ACTION_CHOICES
    )
    name = models.CharField(
        max_length=200, blank=True, null=True,
        help_text=_('Additionally override the name.')
    )
    url = models.URLField(
        max_length=512
    )
    content_type = models.ForeignKey(
        ContentType
    )
    object_id = models.PositiveIntegerField(
        db_index=True
    )
    content_object = GenericForeignKey(
        'content_type', 'object_id'
    )

    @property
    def _service(self):
        return self.service

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
        #if self.service in Relation.UNIQUE_SERVICES:
            # TODO: fix unique problem
            Relation.objects.filter(service=self.service, content_type=self.content_type, object_id=self.object_id).delete()

        super(Relation, self).save(*args, **kwargs)


    @property
    def service_icon(self):
        icon = self.service

        if icon == 'itunes':
            return 'apple'

        if icon == 'youtube':
            return 'youtube-play'

        if icon == 'discogs_master':
            return 'discogs'

        return icon


@receiver(post_save, sender=Relation)
def relation_post_save(sender, instance, signal, created, **kwargs):
    if instance.url[-4:] == 'None':
        instance.delete()

def update_relations():
    rs = Relation.objects.all()
    for r in rs:
        r.save()
