from django.conf import settings
from django.db.models import get_model, get_app
from django.db.models import get_models as get_models_debug

SETTINGS = getattr(settings, 'PUSHY_SETTINGS', {})

def get_channel():
    return '%s' % SETTINGS.get('CHANNEL_PREFIX', 'pushy_')

def get_redis_host():
    return '%s' % SETTINGS.get('REDIS_HOST', '127.0.0.1')

def get_models():
    
    models = {}
    try:
        for model in SETTINGS.get('MODELS', None):
            models[model.lower()] = get_model(*model.lower().split('.'))
    except Exception, e:
        print e

    return models