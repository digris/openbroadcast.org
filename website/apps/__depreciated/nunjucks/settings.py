from django.conf import settings
DEBUG = getattr(settings, 'NUNJUCKS_DEBUG', False)