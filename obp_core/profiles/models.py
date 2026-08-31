import re
import os
import tagging
import arating

from django.db import models
from django.contrib.auth.models import Group
from django.conf import settings
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse

from django_extensions.db.fields import AutoSlugField
from phonenumber_field.modelfields import PhoneNumberField

from tagging.fields import TagField
from tagging.registry import register as tagging_register

from base.fields import extra
from invitation.signals import invitation_accepted
from l10n.models import Country


from base.mixins import TimestampedModelMixin, UUIDModelMixin

DEFAULT_GROUP = "Listener"


class MigrationMixin(models.Model):
    legacy_id = models.IntegerField(null=True, blank=True, editable=False)
    # to find way back to last-last database
    legacy_legacy_id = models.IntegerField(null=True, blank=True, editable=False)
    migrated = models.DateField(null=True, blank=True, editable=False)

    class Meta:
        abstract = True
        app_label = "profiles"
        verbose_name = "MigrationMixin"
        verbose_name_plural = "MigrationMixins"
        ordering = ("pk",)


def filename_by_uuid(instance, filename):
    filename, extension = os.path.splitext(filename)
    path = "profiles/"
    filename = str(instance.uuid).replace("-", "/")[5:] + extension
    return os.path.join(path, filename)


class Profile(TimestampedModelMixin, UUIDModelMixin, MigrationMixin):
    GENDER_CHOICES = (
        (0, "Male"),
        (1, "Female"),
        (2, "Other"),
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        unique=True,
        on_delete=models.CASCADE,
    )
    mentor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name="godchildren",
    )
    gender = models.PositiveSmallIntegerField(
        "gender",
        choices=GENDER_CHOICES,
        blank=True,
        null=True,
    )
    birth_date = models.DateField(
        "Date of birth",
        blank=True,
        null=True,
        help_text="Format: YYYY-MM-DD",
    )
    pseudonym = models.CharField(
        blank=True,
        null=True,
        max_length=250,
        help_text="Will appear instead of your first- & last name",
    )
    description = models.CharField(
        "Disambiguation",
        blank=True,
        null=True,
        max_length=250,
    )
    biography = extra.MarkdownTextField(
        blank=True,
        null=True,
    )
    image = models.ImageField(
        verbose_name="Profile Image",
        upload_to=filename_by_uuid,
        null=True,
        blank=True,
    )
    mobile = PhoneNumberField(
        "mobile",
        blank=True,
        null=True,
    )
    phone = PhoneNumberField(
        "phone",
        blank=True,
        null=True,
    )
    fax = PhoneNumberField(
        "fax",
        blank=True,
        null=True,
    )
    skype = models.CharField(
        "Skype",
        blank=True,
        null=True,
        max_length=100,
    )
    address1 = models.CharField(
        "address",
        null=True,
        blank=True,
        max_length=100,
    )
    address2 = models.CharField(
        "address (secondary)",
        null=True,
        blank=True,
        max_length=100,
    )
    city = models.CharField(
        "city",
        null=True,
        blank=True,
        max_length=100,
    )
    zip = models.CharField(
        "zip",
        null=True,
        blank=True,
        max_length=10,
    )
    country = models.ForeignKey(
        Country,
        blank=True,
        null=True,
    )
    iban = models.CharField(
        "IBAN",
        null=True,
        blank=True,
        max_length=120,
    )
    paypal = models.EmailField(
        "Paypal",
        null=True,
        blank=True,
        max_length=200,
    )
    expertise = models.ManyToManyField(
        "Expertise",
        verbose_name="Fields of expertise",
        blank=True,
    )
    d_tags = TagField(
        max_length=1024,
        verbose_name="Tags",
        blank=True,
        null=True,
    )

    # alpha features / settings
    enable_alpha_features = models.BooleanField(
        verbose_name="Enable experimental features",
        default=False,
    )
    settings_show_media_history = models.BooleanField(
        verbose_name="Show media emission history",
        default=False,
    )
    settings_show_media_appearances = models.BooleanField(
        verbose_name="Show media appearances",
        default=False,
    )
    settings_scheduler_color = models.CharField(
        max_length=7,
        null=True,
        blank=True,
    )

    class Meta:
        app_label = "profiles"
        verbose_name = "user profile"
        verbose_name_plural = "user profiles"
        db_table = "user_profiles"
        ordering = ("-user__last_login",)

        permissions = (
            ("mentor_profiles", "Mentoring profiles"),
            ("view_profiles_private", "View private profile-data."),
        )

    def __str__(self):
        return str(self.get_display_name())

    def get_full_name(self):
        if self.user:
            return self.user.get_full_name()

    @property
    def name(self):
        return self.get_display_name()

    @property
    def main_image(self):
        return self.image

    def get_display_name(self):

        if self.pseudonym:
            return self.pseudonym

        if self.user.get_full_name():
            return self.user.get_full_name()

        return self.user.username

    @property
    def is_approved(self):
        if self.user in Group.objects.get(name="Mentor").user_set.all():
            return True

        return

    def approve(self, mentor, level):

        groups_to_add = []

        if level == "music_pro":
            groups_to_add = ("Music PRO", "Mentor")

        if level == "radio_pro":
            groups_to_add = ("Radio PRO", "Mentor")

        groups = Group.objects.filter(name__in=groups_to_add)

        for group in groups:
            self.user.groups.add(group)

        self.user.groups.remove(Group.objects.get(name=DEFAULT_GROUP))

    def get_ct(self):
        return f"{self._meta.app_label}.{self.__class__.__name__}".lower()

    def get_absolute_url(self):
        return reverse("profiles:profile-detail", kwargs={"uuid": str(self.uuid)})

    def get_edit_url(self):
        return reverse("profiles:profile-edit", kwargs={"uuid": str(self.uuid)})

    # @models.permalink
    # def get_edit_url(self):
    #     return ("profiles:profile-edit",)

    def get_admin_url(self):
        return reverse("admin:profiles_profile_change", args=(self.pk,))

    def get_api_url(self):
        return None
        # return reverse('api_dispatch_detail', kwargs={
        #     'api_name': 'v1',
        #     'resource_name': 'profile',
        #     'pk': self.pk
        # })

    def get_groups(self):
        return self.user.groups

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


try:
    tagging_register(Profile)
except AttributeError:
    pass


arating.enable_voting_on(Profile)


class Community(UUIDModelMixin, MigrationMixin):
    name = models.CharField(
        max_length=200,
        db_index=True,
    )
    slug = AutoSlugField(
        populate_from="name",
        editable=True,
        blank=True,
        overwrite=True,
    )
    group = models.OneToOneField(
        Group,
        unique=True,
        null=True,
        blank=True,
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
    )
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    updated = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    description = extra.MarkdownTextField(
        blank=True,
        null=True,
    )
    image = models.ImageField(
        verbose_name="Profile Image",
        upload_to=filename_by_uuid,
        null=True,
        blank=True,
    )
    mobile = PhoneNumberField(
        "mobile",
        blank=True,
        null=True,
    )
    phone = PhoneNumberField(
        "phone",
        blank=True,
        null=True,
    )
    fax = PhoneNumberField(
        "fax",
        blank=True,
        null=True,
    )
    email = models.EmailField(
        blank=True,
        null=True,
    )
    address1 = models.CharField(
        "address",
        null=True,
        blank=True,
        max_length=100,
    )
    address2 = models.CharField(
        "address (secondary)",
        null=True,
        blank=True,
        max_length=100,
    )
    city = models.CharField(
        "city",
        null=True,
        blank=True,
        max_length=100,
    )
    zip = models.CharField(
        "zip",
        null=True,
        blank=True,
        max_length=10,
    )
    country = models.ForeignKey(
        Country,
        blank=True,
        null=True,
    )
    expertise = models.ManyToManyField(
        "Expertise",
        verbose_name="Fields of expertise",
        blank=True,
    )
    tags = TagField(
        verbose_name="Tags",
        blank=True,
        null=True,
    )

    class Meta:
        app_label = "profiles"
        verbose_name = "Community"
        verbose_name_plural = "Communities"

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)


try:
    tagging.register(Community)
except BaseException:
    pass

arating.enable_voting_on(Community)


def create_profile(sender, instance, created, **kwargs):

    if kwargs["raw"]:
        return

    if created:
        profile, created = Profile.objects.get_or_create(user=instance)

        default_group, created = Group.objects.get_or_create(name=DEFAULT_GROUP)
        instance.groups.add(default_group)
        instance.save()


# TODO: implement in signals.py
post_save.connect(create_profile, sender=settings.AUTH_USER_MODEL)


def add_to_group(sender, instance, **kwargs):
    default_group, created = Group.objects.get_or_create(name=DEFAULT_GROUP)

    if not instance.groups.filter(pk=default_group.pk).exists():
        instance.groups.add(default_group)
        instance.save()


def add_mentor(sender, **kwargs):

    user = kwargs.get("new_user")
    mentor = kwargs.get("inviting_user")
    if user and mentor:
        mentor.godchildren.add(user.profile)
        # send notification to mentor
        from postman.api import pm_write

        pm_write(
            sender=user,
            recipient=mentor,
            subject=f"{user.username} accepted your invitation",
            body="",
        )


invitation_accepted.connect(add_mentor)


class MobileProvider(models.Model):
    """MobileProvider model"""

    title = models.CharField("title", max_length=25)
    domain = models.CharField("domain", max_length=50, unique=True)

    class Meta:
        verbose_name = "mobile provider"
        verbose_name_plural = "mobile providers"
        db_table = "user_mobile_providers"

    def __str__(self):
        return str(self.title)


class ServiceType(models.Model):
    """Service type model"""

    title = models.CharField("title", blank=True, max_length=100)
    url = models.URLField(
        "url",
        blank=True,
        help_text="URL with a single '{user}' placeholder to turn a username into a service URL.",
    )

    class Meta:
        verbose_name = "service type"
        verbose_name_plural = "service types"
        db_table = "user_service_types"

    def __str__(self):
        return str(self.title)


class Service(models.Model):
    service = models.ForeignKey(ServiceType)
    profile = models.ForeignKey(Profile)
    username = models.CharField("Userame / ID", max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "service"
        verbose_name_plural = "services"
        db_table = "user_services"

    def __str__(self):
        return str(self.username)

    def get_url(self):
        return "asdadsd"

    @property
    def service_url(self):
        return re.sub("{user}", self.username, self.service.url)

    @property
    def title(self):
        return str(self.service.title)


class Link(models.Model):
    profile = models.ForeignKey(Profile)
    title = models.CharField("title", max_length=100, null=True, blank=True)
    url = models.URLField("url")

    class Meta:
        verbose_name = "link"
        verbose_name_plural = "links"
        db_table = "user_links"

    def __str__(self):
        return str(self.title)


class Expertise(models.Model):
    name = models.CharField(max_length=512)

    class Meta:
        app_label = "profiles"
        verbose_name = "Expertise"
        verbose_name_plural = "Expertise"
        ordering = ("name",)

    def __str__(self):
        return str(self.name)
