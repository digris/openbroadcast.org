from django.conf import settings

DEBUG = getattr(settings, 'NUNJUCKS_DEBUG', False)

def get_channel():
    return '%s' % SETTINGS.get('CHANNEL_PREFIX', 'nunjucks_')

