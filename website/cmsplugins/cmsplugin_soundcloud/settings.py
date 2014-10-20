"""
Convenience module for access of custom soundcloud application settings,
which enforces default settings when the main settings module does not
contain the appropriate settings.
"""
from django.conf import settings

# Autoplay
CMS_SOUNDCLOUD_DEFAULT_AUTOPLAY = getattr(settings,
                                       'CMS_SOUNDCLOUD_DEFAULT_AUTOPLAY', False)

# Width & Height
CMS_SOUNDCLOUD_DEFAULT_WIDTH = getattr(settings, 'CMS_SOUNDCLOUD_DEFAULT_WIDTH', 425)
CMS_SOUNDCLOUD_DEFAULT_HEIGHT = getattr(settings, 'CMS_SOUNDCLOUD_DEFAULT_HEIGHT', 
                                     344)

# Border
CMS_SOUNDCLOUD_DEFAULT_BORDER = getattr(settings, 'CMS_SOUNDCLOUD_DEFAULT_BORDER',
                                     False)

# Full Screen
CMS_SOUNDCLOUD_DEFAULT_FULLSCREEN = getattr(settings,
                                         'CMS_SOUNDCLOUD_DEFAULT_FULLSCREEN',
                                         True)

# Loop
CMS_SOUNDCLOUD_DEFAULT_LOOP = getattr(settings, 'CMS_SOUNDCLOUD_DEFAULT_LOOP', False)

# Display Related Videos
CMS_SOUNDCLOUD_DEFAULT_RELATED = getattr(settings, 'CMS_SOUNDCLOUD_DEFAULT_RELATED',
                                      False)

# High Quality
CMS_SOUNDCLOUD_DEFAULT_HIGHQUALITY = getattr(settings,
                                          'CMS_SOUNDCLOUD_DEFAULT_HIGHQUALITY',
                                          False)

