# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"
        db_table = "auth_user"

    def get_ct(self):
        return "{}.{}".format(self._meta.app_label, self.__class__.__name__).lower()
