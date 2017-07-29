# -*- coding: utf-8 -*-
from __future__ import absolute_import
import logging
import os
from django.conf import settings
from project.celery import app

log = logging.getLogger(__name__)

# from .models import Waveform, Format
#
# @app.task
# def process_waveform(media, type):
#     Waveform.objects.get_or_create_for_media(media=media, type=type)
#
# @app.task
# def process_format(media, encoding, quality):
#     Format.objects.get_or_create_for_media(media=media, encoding=encoding, quality=quality)
