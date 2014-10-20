import re
import datetime
import os

from dateutil import relativedelta
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse
import tagging
from django_extensions.db.fields import AutoSlugField, UUIDField
from phonenumber_field.modelfields import PhoneNumberField

import arating
from postman.api import pm_write
from lib.fields import extra
from invitation.signals import invitation_accepted
from l10n.models import Country


DEFAULT_GROUP = 'Listener'

class MigrationMixin(models.Model):
    
    legacy_id = models.IntegerField(null=True, blank=True, editable=False)
    # to find way back to last-last database
    legacy_legacy_id = models.IntegerField(null=True, blank=True, editable=False)
    migrated = models.DateField(null=True, blank=True, editable=False)
    
    class Meta:
        abstract = True
        app_label = 'profiles'
        verbose_name = _('MigrationMixin')
        verbose_name_plural = _('MigrationMixins')
        ordering = ('pk', )


def filename_by_uuid(instance, filename):
    filename, extension = os.path.splitext(filename)
    path = "profiles/"
    
    # splitted
    filename = instance.uuid.replace('-', '/')[5:] + extension
    
    return os.path.join(path, filename)


class Profile(MigrationMixin):
    """Profile model"""
    GENDER_CHOICES = (
        (0, _('Male')),
        (1, _('Female')),
        (2, _('Other')),
    )
    #user = models.ForeignKey(User, unique=True)
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    
    #
    uuid = UUIDField()
    
    # auto-update
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)
    
    #
    mentor = models.ForeignKey(User, blank=True, null=True, related_name="godchildren")
    
    #Personal
    gender = models.PositiveSmallIntegerField(_('gender'), choices=GENDER_CHOICES, blank=True, null=True)
    birth_date = models.DateField(_('Date of birth'), blank=True, null=True, help_text=_('Format: YYYY-MM-DD'))
    
    # Profile
    pseudonym = models.CharField(blank=True, null=True, max_length=250)
    description = models.CharField(_('Disambiguation'), blank=True, null=True, max_length=250)
    biography = extra.MarkdownTextField(blank=True, null=True)

    image = models.ImageField(verbose_name=_('Profile Image'), upload_to=filename_by_uuid, null=True, blank=True)

    # Contact (personal)
    mobile = PhoneNumberField(_('mobile'), blank=True, null=True)
    phone = PhoneNumberField(_('phone'), blank=True, null=True)
    fax = PhoneNumberField(_('fax'), blank=True, null=True)
    
    address1 = models.CharField(_('address'), null=True, blank=True, max_length=100)
    address2 = models.CharField(_('address (secondary)'), null=True, blank=True, max_length=100)
    city = models.CharField(_('city'), null=True, blank=True, max_length=100)
    zip = models.CharField(_('zip'), null=True, blank=True, max_length=10)
    country = models.ForeignKey(Country, blank=True, null=True)
    
    iban = models.CharField(_('IBAN'), null=True, blank=True, max_length=120)
    paypal = models.EmailField(_('Paypal'), null=True, blank=True, max_length=200)
    
    # relations
    expertise = models.ManyToManyField('Expertise', verbose_name=_('Fields of expertise'), null=True, blank=True)

    # tagging (d_tags = "display tags")
    d_tags = tagging.fields.TagField(max_length=1024, verbose_name="Tags", blank=True, null=True)

    class Meta:
        app_label = 'profiles'
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')
        db_table = 'user_profiles'
        ordering = ('-user__last_login',)
        
        permissions = (
            ('mentor_profiles', _('Mentoring profiles')),
            ('view_profiles_private', _('View private profile-data.')),
        )

    def __unicode__(self):
        return u"%s" % self.user.get_full_name()

    @property
    def is_approved(self):
        if self.user in Group.objects.get(name='Mentor').user_set.all():
            return True

        return
    
    def approve(self, mentor, level):

        groups_to_add = []

        if level == 'music_pro':
            groups_to_add = ('Music PRO', 'Mentor',)

        if level == 'radio_pro':
            groups_to_add = ('Radio PRO', 'Mentor',)


        groups = Group.objects.filter(name__in=groups_to_add)
        
        for group in groups:
            self.user.groups.add(group)

        self.user.groups.remove(Group.objects.get(name=DEFAULT_GROUP))


    @property
    def age(self):
        TODAY = datetime.date.today()
        if self.birth_date:
            return u"%s" % relativedelta.relativedelta(TODAY, self.birth_date).years
        else:
            return None

    @permalink
    def get_absolute_url(self):
        return ('profiles-profile-detail', None, { 'slug': self.user.username })


    @models.permalink
    def get_edit_url(self):
        return ('profiles-profile-edit',)

    def get_admin_url(self):
        from lib.util.get_admin_url import change_url
        return change_url(self)

    def get_api_url(self):
        return reverse('api_dispatch_detail', kwargs={
            'api_name': 'v1',
            'resource_name': 'profile',
            'pk': self.pk
        }) + ''



    @property
    def sms_address(self):
        if (self.mobile and self.mobile_provider):
            return u"%s@%s" % (re.sub('-', '', self.mobile), self.mobile_provider.domain)
        
        
    def get_groups(self):
        return self.user.groups
        

    def save(self, *args, **kwargs):
        t_tags = ''
        """"""
        for tag in self.tags:
            t_tags += '%s, ' % tag    
        
        self.tags = t_tags
        self.d_tags = t_tags[:1000]

        super(Profile, self).save(*args, **kwargs)

try:
    tagging.register(Profile)
except:
    pass

arating.enable_voting_on(Profile)


class Community(MigrationMixin):
    
    uuid = UUIDField(primary_key=False)
    name = models.CharField(max_length=200, db_index=True)
    slug = AutoSlugField(populate_from='name', editable=True, blank=True, overwrite=True)
    
    group = models.OneToOneField(Group, unique=True, null=True, blank=True)
    members = models.ManyToManyField(User, null=True, blank=True)
    
    # auto-update
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    # Profile
    description = extra.MarkdownTextField(blank=True, null=True)
    image = models.ImageField(verbose_name=_('Profile Image'), upload_to=filename_by_uuid, null=True, blank=True)
    
    # Contact
    mobile = PhoneNumberField(_('mobile'), blank=True, null=True)
    phone = PhoneNumberField(_('phone'), blank=True, null=True)
    fax = PhoneNumberField(_('fax'), blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    
    address1 = models.CharField(_('address'), null=True, blank=True, max_length=100)
    address2 = models.CharField(_('address (secondary)'), null=True, blank=True, max_length=100)
    city = models.CharField(_('city'), null=True, blank=True, max_length=100)
    zip = models.CharField(_('zip'), null=True, blank=True, max_length=10)
    #country = CountryField(blank=True, null=True)
    country = models.ForeignKey(Country, blank=True, null=True)
    # relations
    expertise = models.ManyToManyField('Expertise', verbose_name=_('Fields of expertise'), null=True, blank=True)
    
    # tagging (d_tags = "display tags")
    d_tags = tagging.fields.TagField(verbose_name="Tags", blank=True, null=True)

    class Meta:
        app_label = 'profiles'
        verbose_name = _('Community')
        verbose_name_plural = _('Communities')
        """
        permissions = (
            ('mentor_profiles', 'Mentoring profiles'),
        )
        """

    def __unicode__(self):
        return u"%s" % self.name

    """
    @permalink
    def get_absolute_url(self):
        return ('profiles-profile-detail', None, { 'slug': self.user.username })
    """
    def save(self, *args, **kwargs):
        t_tags = ''
        """"""
        for tag in self.tags:
            t_tags += '%s, ' % tag    
        
        self.tags = t_tags;
        self.d_tags = t_tags[:245];
        
        super(Community, self).save(*args, **kwargs)

try:
    tagging.register(Community)
except:
    pass

arating.enable_voting_on(Community)





def create_profile(sender, instance, created, **kwargs):
    
    if created:  
       profile, created = Profile.objects.get_or_create(user=instance)
       
       default_group, created = Group.objects.get_or_create(name=DEFAULT_GROUP)
       instance.groups.add(default_group)
       instance.save()
       
post_save.connect(create_profile, sender=User) 


def add_to_group(sender, instance, **kwargs):
    default_group, created = Group.objects.get_or_create(name=DEFAULT_GROUP)
    
    if not instance.groups.filter(pk=default_group.pk).exists():
        instance.groups.add(default_group)
        instance.save()

       
#post_save.connect(add_to_group, sender=User) 




def add_mentor(sender, **kwargs):
    
    user = kwargs.get('new_user', None)
    mentor = kwargs.get('inviting_user', None)
    if user and mentor:    
        mentor.godchildren.add(user.profile)
        # send notification to mentor
        pm_write(
                sender = user,
                recipient = mentor,
                subject = _('%(username)s accepted your invitation' % {'username': user.username}),
                body = '')
        

    
invitation_accepted.connect(add_mentor)



class MobileProvider(models.Model):
    """MobileProvider model"""
    title = models.CharField(_('title'), max_length=25)
    domain = models.CharField(_('domain'), max_length=50, unique=True)

    class Meta:
        verbose_name = _('mobile provider')
        verbose_name_plural = _('mobile providers')
        db_table = 'user_mobile_providers'

    def __unicode__(self):
        return u"%s" % self.title


class ServiceType(models.Model):
    """Service type model"""
    title = models.CharField(_('title'), blank=True, max_length=100)
    url = models.URLField(_('url'), blank=True, help_text='URL with a single \'{user}\' placeholder to turn a username into a service URL.', verify_exists=False)

    class Meta:
        verbose_name = _('service type')
        verbose_name_plural = _('service types')
        db_table = 'user_service_types'

    def __unicode__(self):
        return u"%s" % self.title


class Service(models.Model):
    """Service model"""
    service = models.ForeignKey(ServiceType)
    profile = models.ForeignKey(Profile)
    username = models.CharField(_('Userame / ID'), max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('service')
        verbose_name_plural = _('services')
        db_table = 'user_services'

    def __unicode__(self):
        return u"%s" % self.username

    @property
    def service_url(self):
        return re.sub('{user}', self.username, self.service.url)

    @property
    def title(self):
        return u"%s" % self.service.title


class Link(models.Model):

    profile = models.ForeignKey(Profile)
    title = models.CharField(_('title'), max_length=100, null=True, blank=True)
    url = models.URLField(_('url'), verify_exists=True)

    class Meta:
        verbose_name = _('link')
        verbose_name_plural = _('links')
        db_table = 'user_links'

    def __unicode__(self):
        return u"%s" % self.title
    
    

    
class Expertise(models.Model):
    
    name = models.CharField(max_length=512)
    
    class Meta:
        app_label = 'profiles'
        verbose_name = _('Expertise')
        verbose_name_plural = _('Expertise')
        ordering = ('name', )
        
    def __unicode__(self):
        return u"%s" % self.name
        
        
        
        
        
        
        
        
        
        
        