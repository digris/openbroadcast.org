# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings
from django.db.models.signals import post_save
from django.utils.translation import ugettext as _
from django.utils.encoding import python_2_unicode_compatible
from base.mixins import TimestampedModelMixin, UUIDModelMixin

VOTE_CHOICES = ((+1, "+1"), (-1, "-1"))


@python_2_unicode_compatible
class Vote(TimestampedModelMixin, UUIDModelMixin, models.Model):

    vote = models.SmallIntegerField(choices=VOTE_CHOICES, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="votes")

    # generic foreign key to the model being voted upon
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        app_label = "arating"
        verbose_name = _("Vote")
        verbose_name_plural = _("Votes")
        unique_together = (("user", "content_type", "object_id"),)

        permissions = (("vote_for_user", "Can vote in behalf of other user"),)

    def __str__(self):
        return "%s from %s on %s" % (
            self.get_vote_display(),
            self.user,
            self.content_object,
        )

    def get_ct(self):
        return "{}.{}".format(self._meta.app_label, self.__class__.__name__).lower()


def post_save_vote(sender, **kwargs):
    obj = kwargs["instance"]
    try:
        from pushy.util import pushy_custom

        pushy_custom(obj.content_object.get_api_url(), type="update")
    except Exception as e:
        pass


post_save.connect(post_save_vote, sender=Vote)
