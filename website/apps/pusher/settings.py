from django.conf import settings
from django.db.models import get_model


SETTINGS = getattr(settings, 'PUSHER_SETTINGS', {})

def get_models():

    models = {}

    try:
        for model in SETTINGS.get('MODELS', None):
            models[model.lower()] = get_model(*model.split('.'))
    except Exception, e:
        print e

    return models