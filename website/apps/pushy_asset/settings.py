from django.conf import settings

DEBUG = getattr(settings, 'PUSHY_ASSET_DEBUG', True)

def get_channel():
    return '%s' % SETTINGS.get('CHANNEL_PREFIX', 'pushy_asset_')

