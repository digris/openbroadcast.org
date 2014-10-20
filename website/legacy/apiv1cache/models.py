# -*- coding: utf-8 -*-
import os
import sys
import shutil
import hashlib
import magic
import logging
import gzip
from random import randrange
import datetime
import requests

from django.db import models
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
from django.conf import settings


log = logging.getLogger(__name__)

USER_AGENT_STRING = 'Cache Fetcher'
API_BASE_URL = 'http://api.discogs.com/'
WEB_BASE_URL = 'http://www.discogs.com/'

INIT = 0
DONE = 1
QUEUED = 2
ERROR = 99
STATUS_CHOICES = (
    (INIT, 'Init'),
    (DONE, 'Done'),
    (QUEUED, 'Queued'),
    (ERROR, 'Error'),
)

class ResourceMap(models.Model):

    type = models.CharField(max_length=56, blank=False, null=True)
    status = models.PositiveIntegerField(default=0, choices=STATUS_CHOICES)
    v1_id = models.CharField(max_length=512, blank=True, null=True)
    v2_id = models.PositiveIntegerField(blank=True, null=True)

    v1_url = models.CharField(max_length=512, blank=True, null=True)
    v2_url = models.CharField(max_length=512, blank=True, null=True)


    class Meta(object):
        app_label = 'apiv1cache'
        verbose_name = 'Mapped Resource'
        verbose_name_plural = 'Mapped Resources'

    def __unicode__(self):

        return '%s - %s : %s' % (self.type, self.v1_id, self.v2_id)



