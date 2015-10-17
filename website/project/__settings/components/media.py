# -*- coding: utf-8 -*-
import os
import posixpath

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# media deliver
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# static files (application js/img etc)
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'


ADMIN_MEDIA_PREFIX = posixpath.join(STATIC_URL, "admin/")
ADMIN_MEDIA_PREFIX = '/static/admin/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'site-static'),
)

STATICFILES_FINDERS = (
    'compressor.finders.CompressorFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    #'easy_thumbnails.processors.scale_and_crop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
    'easy_thumbnails.processors.background',
    #'base.thumbnail_processors.custom.scale_and_crop_with_subject_location',
)
THUMBNAIL_QUALITY = 80
THUMBNAIL_BASEDIR = 'thumbnails'
THUMBNAIL_PRESERVE_EXTENSIONS = ('png',)

