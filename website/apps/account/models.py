# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"
        db_table = "auth_user"

    def get_ct(self):
        return "{}.{}".format(self._meta.app_label, self.__class__.__name__).lower()


class GlobalPermission(models.Model):
    class Meta:
        managed = False
        default_permissions = ()

        permissions = (
            ("view_obr_sync_api", "Read from OBR Sync API"),
            ("edit_obr_sync_api", "Write to OBR Sync API"),
        )
