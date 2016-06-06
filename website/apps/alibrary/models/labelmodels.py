# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.db import models
import tagging
import os
import logging
import reversion
import uuid
import arating
from actstream import action
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from celery.task import task
from phonenumber_field.modelfields import PhoneNumberField
from l10n.models import Country
from tagging.registry import register as tagging_register
from django_date_extensions.fields import ApproximateDateField
from django_extensions.db.fields import UUIDField, AutoSlugField
from alibrary import settings as alibrary_settings
from lib.fields import extra
from alibrary.models import MigrationMixin
from alibrary.util.slug import unique_slugify
from alibrary.util.storage import get_dir_for_object, OverwriteStorage

logger = logging.getLogger(__name__)

LOOKUP_PROVIDERS = (
    ('discogs', _('Discogs')),
    ('musicbrainz', _('Musicbrainz')),
)

def upload_image_to(instance, filename):
    filename, extension = os.path.splitext(filename)
    return os.path.join(get_dir_for_object(instance), 'logo%s' % extension.lower())


class LabelManager(models.Manager):

    def active(self):
        return self.get_queryset().exclude(listed=False)

class Label(MigrationMixin):

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=400)
    slug = AutoSlugField(populate_from='name', editable=True, blank=True, overwrite=True)

    labelcode = models.CharField(max_length=250, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    country = models.ForeignKey(Country, blank=True, null=True)
    
    email = models.EmailField(blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    fax = PhoneNumberField(blank=True, null=True)
    main_image = models.ImageField(verbose_name=_('Logo Image'), upload_to=upload_image_to, storage=OverwriteStorage(), null=True, blank=True)
    description = extra.MarkdownTextField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    date_start = ApproximateDateField(verbose_name="Life-span begin", blank=True, null=True)
    date_end = ApproximateDateField(verbose_name="Life-span end", blank=True, null=True)

    owner = models.ForeignKey(User, blank=True, null=True, related_name="labels_owner", on_delete=models.SET_NULL)
    creator = models.ForeignKey(User, blank=True, null=True, related_name="labels_creator", on_delete=models.SET_NULL)
    last_editor = models.ForeignKey(User, blank=True, null=True, related_name="labels_last_editor", on_delete=models.SET_NULL)
    publisher = models.ForeignKey(User, blank=True, null=True, related_name="labels_publisher", on_delete=models.SET_NULL)

    listed = models.BooleanField(verbose_name='Include in listings', default=True, help_text=_('Should this Label be shown on the default Label-list?'))
    disable_link = models.BooleanField(verbose_name='Disable Link', default=False, help_text=_('Disable Linking. Useful e.g. for "Unknown Label"'))
    disable_editing = models.BooleanField(verbose_name='Disable Editing', default=False, help_text=_('Disable Editing. Useful e.g. for "Unknown Label"'))

    type = models.CharField(verbose_name="Label type", max_length=128, default='unknown', choices=alibrary_settings.LABELTYPE_CHOICES)

    relations = GenericRelation('Relation')
    d_tags = tagging.fields.TagField(max_length=1024,verbose_name="Tags", blank=True, null=True)

    # refactoring parent handling
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')
    parent_temporary_id = models.PositiveIntegerField(null=True, blank=True)

    objects = LabelManager()

    class Meta:
        app_label = 'alibrary'
        verbose_name = _('Label')
        verbose_name_plural = _('Labels')
        ordering = ('name', )

        permissions = (
            ('merge_label', 'Merge Labels'),
        )


    def __unicode__(self):
        return self.name

    def get_versions(self):
        try:
            return reversion.get_for_object(self)
        except:
            return None

    def get_last_revision(self):
        try:
            return reversion.get_unique_for_object(self)[0].revision
        except:
            return None

    def get_last_editor(self):
        latest_revision = self.get_last_revision()
        if latest_revision:
            return latest_revision.user
        else:
            return None

    def get_folder(self, name):
        return

    def get_lookup_providers(self):

        providers = []
        for key, name in LOOKUP_PROVIDERS:
            relations = self.relations.filter(service=key)
            relation = None
            if relations.count() == 1:
                relation = relations[0]

            providers.append({'key': key, 'name': name, 'relation': relation})

        return providers


    def get_absolute_url(self):
        if self.disable_link:
            return None
        return reverse('alibrary-label-detail', kwargs={
            'pk': self.pk,
            'slug': self.slug,
        })

    def get_edit_url(self):
        return reverse("alibrary-label-edit", args=(self.pk,))

    def get_admin_url(self):
        return reverse("admin:alibrary_label_change", args=(self.pk,))


    def get_api_url(self):
        return reverse('api_dispatch_detail', kwargs={
            'api_name': 'v1',
            'resource_name': 'library/label',
            'pk': self.pk
        }) + ''


    def get_root(self):

        if not self.parent:
            return None

        parent = self.parent
        last_parent = None
        while parent:
            parent = parent.parent
            if parent:
                last_parent = parent

        return last_parent



    def save(self, *args, **kwargs):
        unique_slugify(self, self.name)
        super(Label, self).save(*args, **kwargs)




tagging_register(Label)
arating.enable_voting_on(Label)

def action_handler(sender, instance, created, **kwargs):
    action_handler_task.delay(instance, created)

post_save.connect(action_handler, sender=Label)

@task
def action_handler_task(instance, created):

    if created and instance.creator:
        action.send(instance.creator, verb=_('created'), target=instance)

    elif instance.last_editor:
        action.send(instance.last_editor, verb=_('updated'), target=instance)
