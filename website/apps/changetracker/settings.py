import logging
from django.conf import settings
from django.apps import apps
log = logging.getLogger(__name__)

TRACKED_MODELS = getattr(settings, 'CHANGETRACKER_TRACKED_MODELS', {})

def get_tracked_models():
    
    models = {}
    try:
        for model in TRACKED_MODELS:
            models[model.lower()] = apps.get_model(*model.lower().split('.'))
    except Exception, e:
        log.warning('Unable to resolve models: %s' % e)

    return models
