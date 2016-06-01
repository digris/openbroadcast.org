# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django.db import models

class Host(models.Model):

    hostname = models.CharField(max_length=254)
    ip = models.GenericIPAddressField(null=True)

    class Meta:
        app_label = 'iptracker'
        verbose_name = _('Host')
        ordering = ['hostname', ]


    def __unicode__(self):
        return "%s - %s" % (self.hostname, self.ip)