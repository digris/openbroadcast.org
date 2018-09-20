# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import os
import uuid

import arating
import tagging
from actstream import action
from alibrary.models import MigrationMixin, Relation, Profession
from alibrary.util.slug import unique_slugify
from alibrary.util.storage import get_dir_for_object, OverwriteStorage
from base.cacheops_extra import cached_uuid_aware
from base.mixins import TimestampedModelMixin
from celery.task import task
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.core.urlresolvers import reverse, NoReverseMatch
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.functional import cached_property
from django.utils.translation import ugettext as _
from django.utils import translation
from django_date_extensions.fields import ApproximateDateField
from django_extensions.db.fields import AutoSlugField
from l10n.models import Country
from tagging.registry import register as tagging_register

from .mediamodels import MediaArtists, MediaExtraartists, Media
from .releasemodels import Release

log = logging.getLogger(__name__)

LOOKUP_PROVIDERS = (
    ('discogs', _('Discogs')),
    ('musicbrainz', _('Musicbrainz')),
)

def upload_image_to(instance, filename):
    filename, extension = os.path.splitext(filename)
    return os.path.join(get_dir_for_object(instance), 'image%s' % extension.lower())


class NameVariation(models.Model):
    name = models.CharField(max_length=250, db_index=True)
    artist = models.ForeignKey(
        'Artist',
        related_name="namevariations",
        on_delete=models.CASCADE,
        null=True, blank=True
    )

    class Meta:
        app_label = 'alibrary'
        verbose_name = _('Name variation')
        verbose_name_plural = _('Name variation')
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class ArtistManager(models.Manager):
    def listed(self):
        return self.get_queryset().filter(listed=True, priority__gt=0)


class Artist(MigrationMixin, TimestampedModelMixin, models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250, db_index=True)
    slug = AutoSlugField(populate_from='name', editable=True, blank=True, overwrite=True, db_index=True)

    TYPE_CHOICES = (
        ('person', _('Person')),
        ('group', _('Group')),
        ('orchestra', _('Orchestra')),
        ('other', _('Other')),
    )
    type = models.CharField(
        verbose_name="Artist type",
        max_length=128,
        blank=True, null=True,
        choices=TYPE_CHOICES
    )
    main_image = models.ImageField(
        verbose_name=_('Image'),
        upload_to=upload_image_to,
        storage=OverwriteStorage(),
        null=True, blank=True
    )
    real_name = models.CharField(
        max_length=250,
        blank=True, null=True
    )
    disambiguation = models.CharField(
        max_length=256,
        blank=True, null=True
    )
    country = models.ForeignKey(
        Country,
        blank=True, null=True
    )
    booking_contact = models.CharField(
        verbose_name=_('Booking'),
        max_length=256,
        blank=True, null=True
    )
    email = models.EmailField(
        verbose_name=_('E-Mail'),
        max_length=256,
        blank=True, null=True
    )
    date_start = ApproximateDateField(
        verbose_name=_("Begin"),
        blank=True, null=True,
        help_text=_("date of formation / date of birth")
    )
    date_end = ApproximateDateField(
        verbose_name=_("End"),
        blank=True, null=True,
        help_text=_("date of breakup / date of death")
    )
    # properties to create 'special' objects. (like 'Unknown')
    listed = models.BooleanField(
        verbose_name='Include in listings',
        default=True,
        help_text=_('Should this Artist be shown on the default Artist-list?')
    )
    disable_link = models.BooleanField(
        verbose_name='Disable Link',
        default=False,
        help_text=_('Disable Linking. Useful e.g. for "Varius Artists"')
    )
    disable_editing = models.BooleanField(
        verbose_name='Disable Editing',
        default=False,
        help_text=_('Disable Editing. Useful e.g. for "Unknown Artist"')
    )
    excerpt = models.TextField(blank=True, null=True)
    biography = models.TextField(blank=True, null=True)
    # relations
    members = models.ManyToManyField(
        'self',
        through='ArtistMembership',
        symmetrical=False
    )
    aliases = models.ManyToManyField(
        "self",
        through='ArtistAlias',
        related_name='artist_aliases',
        blank=True,
        symmetrical=False
    )
    # relations a.k.a. links
    relations = GenericRelation(Relation)

    # tagging (d_tags = "display tags")
    d_tags = tagging.fields.TagField(
        max_length=1024,
        verbose_name="Tags",
        blank=True, null=True
    )
    professions = models.ManyToManyField(Profession, through='ArtistProfessions')

    # user relations
    owner = models.ForeignKey(
        User,
        blank=True, null=True,
        related_name="artists_owner",
        on_delete=models.SET_NULL
    )
    creator = models.ForeignKey(
        User,
        blank=True, null=True,
        related_name="artists_creator",
        on_delete=models.SET_NULL
    )
    last_editor = models.ForeignKey(
        User,
        blank=True, null=True,
        related_name="artists_last_editor",
        on_delete=models.SET_NULL
    )
    publisher = models.ForeignKey(
        User,
        blank=True, null=True,
        related_name="artists_publisher",
        on_delete=models.SET_NULL
    )

    # identifiers
    ipi_code = models.CharField(
        verbose_name=_('IPI Code'),
        max_length=32,
        blank=True, null=True
    )
    isni_code = models.CharField(
        verbose_name=_('ISNI Code'),
        max_length=32,
        blank=True, null=True
    )

    objects = ArtistManager()

    class Meta:
        app_label = 'alibrary'
        verbose_name = _('Artist')
        verbose_name_plural = _('Artists')
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    @property
    def classname(self):
        return self.__class__.__name__


    def get_absolute_url(self):
        if self.disable_link:
            return None
        try:
            return reverse('alibrary-artist-detail', kwargs={
                'pk': self.pk,
                'slug': self.slug,
            })
        except NoReverseMatch:
            translation.activate('en')
            return reverse('alibrary-artist-detail', kwargs={
                'pk': self.pk,
                'slug': self.slug,
            })

    def get_edit_url(self):
        return reverse("alibrary-artist-edit", args=(self.pk,))

    def get_admin_url(self):
        return reverse("admin:alibrary_artist_change", args=(self.pk,))

    def get_api_url(self):
        return reverse('api_dispatch_detail', kwargs={
            'api_name': 'v1',
            'resource_name': 'library/artist',
            'pk': self.pk
        }) + ''

    @property
    def description(self):
        """mapping to generic field"""
        return self.biography

    @cached_property
    def get_membership(self):
        """ get artists group/band membership """
        return [m.parent for m in ArtistMembership.objects.filter(child=self)]

    def get_alias_ids(self, exclude=None):
        """ get ids of artists aliases """
        exclude = exclude or []
        alias_ids = []
        parent_alias_ids = ArtistAlias.objects.filter(child__pk=self.pk).values_list('parent__pk', flat=True).distinct()
        child_alias_ids = ArtistAlias.objects.filter(parent__pk=self.pk).values_list('child__pk', flat=True).distinct()

        alias_ids.extend(parent_alias_ids)
        alias_ids.extend(child_alias_ids)

        for alias_id in alias_ids:
            if not alias_id == self.pk and not alias_id in exclude:
                exclude.append(alias_id)
                alias_ids.extend(Artist.objects.get(pk=alias_id).get_alias_ids(exclude=exclude))

        return alias_ids

    def get_aliases(self):
        """ get artists aliases """
        return Artist.objects.filter(pk__in=self.get_alias_ids([])).exclude(pk=self.pk).distinct()


    ###################################################################
    # TODO: look for a better (=faster) way to get appearances!
    ###################################################################
    @cached_uuid_aware(timeout=60 * 60 * 24)
    def get_releases(self):
        """ get releases where artist appears """

        media_ids = []

        qs_a = Media.objects.filter(artist=self)
        qs_mediaartist = MediaArtists.objects.filter(artist=self)

        media_ids += qs_a.values_list('id', flat=True)
        media_ids += qs_mediaartist.values_list('media_id', flat=True)

        return Release.objects.filter(
            Q(media_release__pk__in=media_ids) | Q(album_artists__pk=self.pk)
        ).distinct()


    @cached_uuid_aware(timeout=60 * 60 * 24)
    def get_media(self):
        """ get tracks where artist appears """

        media_ids = []

        qs_a = Media.objects.filter(artist=self)
        qs_mediaartist = MediaArtists.objects.filter(artist=self)
        qs_credited = MediaExtraartists.objects.filter(artist=self)

        media_ids += qs_a.values_list('id', flat=True)
        media_ids += qs_mediaartist.values_list('media_id', flat=True)
        media_ids += qs_credited.values_list('media_id', flat=True)

        return Media.objects.filter(pk__in=list(set(media_ids)))


    def appearances(self):
        """ get artists appearances (releases/tracks) """
        try:
            num_releases = self.get_releases().count()
        except:
            num_releases = 0

        try:
            num_media = self.get_media().count()
        except:
            num_media = 0

        appearances = {
            'num_releases': num_releases,
            'num_media': num_media
        }
        return appearances


    def get_lookup_providers(self):

        providers = []
        for key, name in LOOKUP_PROVIDERS:
            relations = self.relations.filter(service=key)
            relation = None
            if relations.exists():
                relation = relations[0]

            providers.append({'key': key, 'name': name, 'relation': relation})

        return providers

    def save(self, *args, **kwargs):
        unique_slugify(self, self.name)

        if self.type:
            self.type = self.type.lower()

        """
        TODO: implement otherwise
        there is a special-case artist called "Various Artists" that should only exist once.
        in the case we - for whatever unplanned reason - there is a duplicate coming in we
        add a counter to the name ensure uniqueness.
        """

        if self.name == 'Various Artists' and self.pk is None:
            log.warning('attempt to create "Various Artists"')
            original_name = self.name
            i = 1
            while Artist.objects.filter(name=self.name).count() > 0:
                self.name = u'%s %s' % (original_name, i)
                i += 1

        super(Artist, self).save(*args, **kwargs)



tagging_register(Artist)
arating.enable_voting_on(Artist)

# @receiver(post_save, sender=Artist)
# def action_handler(sender, instance, created, **kwargs):
#     try:
#         action_handler_task.delay(instance, created)
#     except:
#         pass
#
# @task
# def action_handler_task(instance, created):
#     if created and instance.creator:
#         action.send(instance.creator, verb=_('created'), target=instance)
#
#     elif instance.last_editor:
#         action.send(instance.last_editor, verb=_('updated'), target=instance)


class ArtistMembership(models.Model):
    parent = models.ForeignKey(Artist, related_name='artist_parent', blank=True, null=True)
    child = models.ForeignKey(Artist, related_name='artist_child', blank=True, null=True)
    profession = models.ForeignKey(Profession, related_name='artist_membership_profession', blank=True, null=True)

    class Meta:
        app_label = 'alibrary'
        verbose_name = _('Membersip')
        verbose_name_plural = _('Membersips')

    def __unicode__(self):
        return '"%s" <> "%s"' % (self.parent.name, self.child.name)

    def save(self, *args, **kwargs):

        if not self.child or not self.parent:
            self.delete()

        super(ArtistMembership, self).save(*args, **kwargs)


class ArtistAlias(models.Model):
    parent = models.ForeignKey(Artist, related_name='alias_parent')
    child = models.ForeignKey(Artist, related_name='alias_child')

    class Meta:
        app_label = 'alibrary'
        verbose_name = _('Alias')
        verbose_name_plural = _('Aliases')

    def __unicode__(self):
        return '"%s" <> "%s"' % (self.parent.name, self.child.name)


class ArtistProfessions(models.Model):
    artist = models.ForeignKey('Artist')
    profession = models.ForeignKey('Profession')

    class Meta:
        app_label = 'alibrary'
        verbose_name = _('Profession')
        verbose_name_plural = _('Professions')

    def __unicode__(self):
        return '"%s" : "%s"' % (self.artist.name, self.profession.name)
