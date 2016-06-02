# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.db import models


class TimestampedModel(models.Model):
    """ TimestampedModelMixin
    An abstract base class model that provides self-managed "created" and
    "updated" fields.
    """
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    """ UUIDModelMixin
    An abstract base class model that provides a self-managed "uuid" field.
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)

    class Meta:
        abstract = True
