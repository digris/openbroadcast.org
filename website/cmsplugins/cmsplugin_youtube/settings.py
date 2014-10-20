"""
YouTube plugin
"""
from django.conf import settings


# Width & Height
CMS_YOUTUBE_DEFAULT_WIDTH = getattr(settings, 'CMS_YOUTUBE_DEFAULT_WIDTH', 830)
CMS_YOUTUBE_DEFAULT_HEIGHT = getattr(settings, 'CMS_YOUTUBE_DEFAULT_HEIGHT', 467)



