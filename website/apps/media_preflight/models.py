# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

import json
import logging

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from jsonfield import JSONField

from base.mixins import TimestampedModelMixin

from .tasks import (
    run_preflight_check_task,
)

SITE_URL = getattr(settings, "SITE_URL")

log = logging.getLogger(__name__)


@python_2_unicode_compatible
class PreflightCheck(TimestampedModelMixin, models.Model):

    STATUS_PENDING = "pending"
    STATUS_RUNNING = "running"
    STATUS_COMPLETED = "completed"
    STATUS_ERROR = "error"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_RUNNING, "Running"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_ERROR, "Error"),
    )

    status = models.CharField(
        _("Status"),
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        max_length=16,
        blank=False,
        null=False,
        db_index=True,
    )

    media = models.OneToOneField(
        "alibrary.Media",
        related_name="preflight_check",
        null=True,
        blank=False,
        on_delete=models.CASCADE,
    )

    checks = JSONField(
        default={},
        editable=False,
    )

    warnings = JSONField(
        default=[],
        editable=False,
    )

    errors = JSONField(
        default=[],
        editable=False,
    )

    def __str__(self):
        return "{}".format(self.pk)

    @property
    def has_warnings(self):
        return bool(self.warnings)

    @property
    def has_errors(self):
        return bool(self.errors)


@receiver(post_save, sender=PreflightCheck)
def preflight_check_post_save(sender, instance, created, **kwargs):
    """
    run preflight check (intermediate step here to handle async / celery)
    """

    if instance.status == PreflightCheck.STATUS_PENDING:
        PreflightCheck.objects.filter(pk=instance.pk).update(
            status=PreflightCheck.STATUS_RUNNING
        )

        run_preflight_check_task.apply_async((instance.id,))
        # run_preflight_check_task(instance.id)
