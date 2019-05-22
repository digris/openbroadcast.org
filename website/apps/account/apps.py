# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class AccountConfig(AppConfig):
    name = "account"
    verbose_name = _("User Accounts")
