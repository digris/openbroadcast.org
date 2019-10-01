# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid
from django.db import models


class TimestampedModelMixin(models.Model):
    """ TimestampedModelMixin
    An abstract base class model that provides self-managed "created" and
    "updated" fields.
    """

    created = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)
    updated = models.DateTimeField(auto_now=True, editable=False, db_index=True)

    class Meta:
        abstract = True


class UUIDModelMixin(models.Model):
    """ UUIDModelMixin
    An abstract base class model that provides a self-managed "uuid" field.
    """

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)

    class Meta:
        abstract = True


class StripWhitespaceFormMixin(object):
    # seen heere: http://stackoverflow.com/a/31248409/469111
    def full_clean(self):
        # self.data can be dict (usually empty) or QueryDict here.
        self.data = self.data.copy()
        is_querydict = hasattr(self.data, "setlist")
        strip = lambda val: val.strip()
        for k in list(self.data.keys()):
            if is_querydict:
                self.data.setlist(k, map(strip, self.data.getlist(k)))
            else:
                self.data[k] = strip(self.data[k])
        super(StripWhitespaceFormMixin, self).full_clean()
