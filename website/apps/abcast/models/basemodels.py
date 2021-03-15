# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import arating
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _
from django_extensions.db.fields import AutoSlugField
from l10n.models import Country
from base.fields import extra
from base.mixins import TimestampedModelMixin, UUIDModelMixin
from phonenumber_field.modelfields import PhoneNumberField


@python_2_unicode_compatible
class Station(TimestampedModelMixin, UUIDModelMixin, models.Model):

    TYPE_CHOICES = (("stream", _("Stream")), ("djmon", _("DJ-Monitor")))
    type = models.CharField(
        verbose_name=_("Type"), max_length=12, default="stream", choices=TYPE_CHOICES
    )

    name = models.CharField(max_length=256, null=True, blank=True)
    slug = AutoSlugField(populate_from="name")
    teaser = models.CharField(max_length=512, null=True, blank=True)
    main_image = models.ImageField(
        verbose_name=_("Image"), upload_to="abcast/station", null=True, blank=True
    )
    description = extra.MarkdownTextField(blank=True, null=True)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through="StationMembers", blank=True
    )
    website = models.URLField(max_length=256, null=True, blank=True)
    phone = PhoneNumberField(_("phone"), blank=True, null=True)
    fax = PhoneNumberField(_("fax"), blank=True, null=True)
    address1 = models.CharField(_("address"), null=True, blank=True, max_length=100)
    address2 = models.CharField(
        _("address (secondary)"), null=True, blank=True, max_length=100
    )
    city = models.CharField(_("city"), null=True, blank=True, max_length=100)
    zip = models.CharField(_("zip"), null=True, blank=True, max_length=10)
    country = models.ForeignKey(Country, blank=True, null=True)

    class Meta:
        app_label = "abcast"
        verbose_name = _("Station")
        verbose_name_plural = _("Stations")
        ordering = ("name",)

    def __str__(self):
        return "%s" % self.name

    # @models.permalink
    # def get_absolute_url(self):
    #     return "abcast-station-detail", [self.uuid]

    def get_absolute_url(self):
        try:
            url = reverse("abcast-station-detail", kwargs={"uuid": str(self.uuid)})
        except:
            url = ""
        return url

    def get_admin_url(self):
        return reverse("admin:abcast_station_change", args=(self.pk,))


arating.enable_voting_on(Station)


@python_2_unicode_compatible
class Role(models.Model):

    name = models.CharField(max_length=200)

    class Meta:
        app_label = "abcast"
        verbose_name = _("Role")
        verbose_name_plural = _("Roles")
        ordering = ("name",)

    def __str__(self):
        return self.name


class StationMembers(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="station_membership"
    )
    station = models.ForeignKey(Station)
    roles = models.ManyToManyField(Role, blank=True, related_name="memgership_roles")

    class Meta:
        app_label = "abcast"
        verbose_name = _("Role")
        verbose_name_plural = _("Roles")


@python_2_unicode_compatible
class OnAirItem(TimestampedModelMixin, UUIDModelMixin, models.Model):

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        app_label = "abcast"
        verbose_name = _("On Air")
        verbose_name_plural = _("On Air")
        unique_together = ("content_type", "object_id")

    def __str__(self):
        return "%s : %s" % (self.channel.pk, self.channel.pk)


@python_2_unicode_compatible
class Channel(TimestampedModelMixin, UUIDModelMixin, models.Model):

    name = models.CharField(max_length=256, null=True, blank=True)
    teaser = models.CharField(max_length=512, null=True, blank=True)
    slug = AutoSlugField(populate_from="name")

    TYPE_CHOICES = (("stream", _("Stream")), ("djmon", _("DJ-Monitor")))
    type = models.CharField(
        verbose_name=_("Type"), max_length=12, default="stream", choices=TYPE_CHOICES
    )
    stream_url = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        help_text=_("setting the stream-url overrides server settings"),
    )
    description = extra.MarkdownTextField(blank=True, null=True)
    station = models.ForeignKey(
        "Station", null=True, blank=True, on_delete=models.SET_NULL
    )
    rtmp_app = models.CharField(max_length=256, null=True, blank=True)
    rtmp_path = models.CharField(max_length=256, null=True, blank=True)
    has_scheduler = models.BooleanField(default=False)
    mount = models.CharField(max_length=64, null=True, blank=True)

    # credentials for tunein api
    tunein_station_id = models.CharField(max_length=16, null=True, blank=True)
    tunein_partner_id = models.CharField(max_length=16, null=True, blank=True)
    tunein_partner_key = models.CharField(max_length=16, null=True, blank=True)

    # credentials for icecast2 metadata
    icecast2_server = models.CharField(max_length=256, null=True, blank=True)
    icecast2_mountpoint = models.CharField(max_length=128, null=True, blank=True)
    icecast2_admin_user = models.CharField(max_length=128, null=True, blank=True)
    icecast2_admin_pass = models.CharField(max_length=128, null=True, blank=True)

    on_air_type = models.ForeignKey(ContentType, null=True, blank=True)
    on_air_id = models.PositiveIntegerField(null=True, blank=True)
    on_air = GenericForeignKey("on_air_type", "on_air_id")

    class Meta:
        app_label = "abcast"
        verbose_name = _("Channel")
        verbose_name_plural = _("Channels")
        ordering = ("name",)
        unique_together = ("on_air_type", "on_air_id")

    def __str__(self):
        return "%s" % self.name

    def get_absolute_url(self):
        return reverse("abcast-station-detail", kwargs={"uuid": str(self.station.uuid)})

    def get_api_url(self):
        return (
            reverse(
                "api_dispatch_detail",
                kwargs={
                    "api_name": "v1",
                    "resource_name": "abcast/channel",
                    "pk": self.pk,
                },
            )
            + ""
        )

    def get_dayparts(self, day):
        dayparts = []
        daypart_sets = self.daypartsets.filter(
            time_start__lte=day, time_end__gte=day, channel=self
        )
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
        emissions = self.scheduler_emissions.filter(
            channel__pk=self.pk, time_start__lte=now, time_end__gte=now
        )
        if emissions.count() > 0:

            emission_url = emissions.first().get_api_url()

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
            "item": item_url,
            "emission": emission_url,
            "emission_items": emission_items,
        }

        return on_air
