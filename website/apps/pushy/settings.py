import logging
from django.conf import settings
from django.db.models import get_model, get_app
from django.db.models import get_models as get_models_debug
log = logging.getLogger(__name__)
PUSHY_SETTINGS = getattr(settings, 'PUSHY_SETTINGS', {})

def get_channel():
    return '%s' % PUSHY_SETTINGS.get('CHANNEL_PREFIX', 'pushy_')

def get_redis_host():
    return '%s' % PUSHY_SETTINGS.get('REDIS_HOST', '127.0.0.1')

def get_models():
    
    models = {}
    try:
        for model in PUSHY_SETTINGS.get('MODELS', None):
            models[model.lower()] = get_model(*model.lower().split('.'))
    except Exception, e:
        log.warning('Unable to register models: %s' % e)

    return models