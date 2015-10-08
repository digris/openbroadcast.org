#-*- coding: utf-8 -*-
from __future__ import absolute_import
from django.conf import settings

DEBUG = getattr(settings, 'NUNJUCKS_DEBUG', settings.DEBUG)
NUNJUCKS_BIN = getattr(settings, 'NUNJUCKS_BIN', 'nunjucks-precompile')
