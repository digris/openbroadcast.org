# python
import datetime

# django
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

from django.contrib.contenttypes import generic


# cms
# from cms.models import CMSPlugin, Page
from cms.models.fields import PlaceholderField
from cms.utils.placeholder import get_page_from_placeholder_if_exists

# filer
from filer.models.filemodels import *
from filer.models.foldermodels import *
from filer.models.audiomodels import *
from filer.models.imagemodels import *
from filer.fields.image import FilerImageField

from django_date_extensions.fields import ApproximateDateField

# modules
#from taggit.managers import TaggableManager
from phonenumber_field.modelfields import PhoneNumberField

from l10n.models import Country

import tagging
import reversion 

# model extensions
from mptt.models import MPTTModel, TreeForeignKey

# django-extensions (http://packages.python.org/django-extensions/)
from django_extensions.db.fields import UUIDField, AutoSlugField

from alibrary import settings as alibrary_settings

# logging
import logging
logger = logging.getLogger(__name__)

import arating

################
from alibrary.models import MigrationMixin
from alibrary.util.signals import library_post_save
from alibrary.util.slug import unique_slugify
from alibrary.util.storage import get_dir_for_object, OverwriteStorage


from lib.fields import extra


LOOKUP_PROVIDERS = (
    ('discogs', _('Discogs')),
    ('musicbrainz', _('Musicbrainz')),
)

def upload_image_to(instance, filename):
    filename, extension = os.path.splitext(filename)
    return os.path.join(get_dir_for_object(instance), 'logo%s' % extension.lower())


class LabelManager(models.Manager):

    def active(self):
        now = datetime.now()
        return self.get_query_set().exclude(listed=False)


class Label(MPTTModel, MigrationMixin):

    # core fields
    uuid = UUIDField(primary_key=False)
    name = models.CharField(max_length=400)
    slug = AutoSlugField(populate_from='name', editable=True, blank=True, overwrite=True)
    
    
    labelcode = models.CharField(max_length=250, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    #country = CountryField(blank=True, null=True)
    country = models.ForeignKey(Country, blank=True, null=True)
    
    email = models.EmailField(blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    fax = PhoneNumberField(blank=True, null=True)
    
    main_image = models.ImageField(verbose_name=_('Cover'), upload_to=upload_image_to, storage=OverwriteStorage(), null=True, blank=True)
    #main_image = FilerImageField(null=True, blank=True, related_name="label_main_image", rel='')
    
    description = extra.MarkdownTextField(blank=True, null=True)
    
    #first_placeholder = PlaceholderField('first_placeholder')
    
    # auto-update
    created = models.DateField(auto_now_add=True, editable=False)
    updated = models.DateField(auto_now=True, editable=False)

    # life-span
    date_start = ApproximateDateField(verbose_name="Life-span begin", blank=True, null=True)
    date_end = ApproximateDateField(verbose_name="Life-span end", blank=True, null=True)

    # relations
    parent = TreeForeignKey('self', null=True, blank=True, related_name='label_children')
    folder = models.ForeignKey(Folder, blank=True, null=True, related_name='label_folder')
    
    # user relations
    owner = models.ForeignKey(User, blank=True, null=True, related_name="labels_owner", on_delete=models.SET_NULL)
    creator = models.ForeignKey(User, blank=True, null=True, related_name="labels_creator", on_delete=models.SET_NULL)
    publisher = models.ForeignKey(User, blank=True, null=True, related_name="labels_publisher", on_delete=models.SET_NULL)
    
    # properties to create 'special' objects. (like 'Unknown')
    listed = models.BooleanField(verbose_name='Include in listings', default=True, help_text=_('Should this Label be shown on the default Label-list?'))
    disable_link = models.BooleanField(verbose_name='Disable Link', default=False, help_text=_('Disable Linking. Useful e.g. for "Unknown Label"'))
    disable_editing = models.BooleanField(verbose_name='Disable Editing', default=False, help_text=_('Disable Editing. Useful e.g. for "Unknown Label"'))

    
    type = models.CharField(verbose_name="Label type", max_length=12, default='unknown', choices=alibrary_settings.LABELTYPE_CHOICES)


    # relations a.k.a. links
    relations = generic.GenericRelation('Relation')
    
    # tagging (d_tags = "display tags")
    d_tags = tagging.fields.TagField(max_length=1024,verbose_name="Tags", blank=True, null=True)
 
    
    # manager
    objects = LabelManager()

    # meta
    class Meta:
        app_label = 'alibrary'
        verbose_name = _('Label')
        verbose_name_plural = _('Labels')
        ordering = ('name', )

        permissions = (
            ('merge_label', 'Merge Labels'),
        )

    class MPTTMeta:
        order_insertion_by = ['name']
    
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
        folder, created = Folder.objects.get_or_create(name=name, parent=self.folder)
        return folder



    def get_lookup_providers(self):

        providers = []
        for key, name in LOOKUP_PROVIDERS:
            relations = self.relations.filter(service=key)
            relation = None
            if relations.count() == 1:
                relation = relations[0]

            providers.append({'key': key, 'name': name, 'relation': relation})

        return providers


    @models.permalink
    def get_absolute_url(self):
        if self.disable_link:
            return None
        
        return ('alibrary-label-detail', [self.slug])

    @models.permalink
    def get_edit_url(self):
        return ('alibrary-label-edit', [self.pk])

    def get_admin_url(self):
        from lib.util.get_admin_url import change_url
        return change_url(self)


    def get_api_url(self):
        return reverse('api_dispatch_detail', kwargs={
            'api_name': 'v1',
            'resource_name': 'library/label',
            'pk': self.pk
        }) + ''



    def save(self, *args, **kwargs):
        unique_slugify(self, self.name)
        
        # update d_tags
        t_tags = ''
        for tag in self.tags:
            t_tags += '%s, ' % tag    
        
        self.tags = t_tags
        self.d_tags = t_tags
        
        super(Label, self).save(*args, **kwargs)
    
        
try:
    tagging.register(Label)
except:
    pass

# register
post_save.connect(library_post_save, sender=Label)   
arating.enable_voting_on(Label)

from actstream import action
def action_handler(sender, instance, created, **kwargs):
    try:
        action.send(instance.get_last_editor(), verb=_('updated'), target=instance)
    except:
        pass


post_save.connect(action_handler, sender=Label)