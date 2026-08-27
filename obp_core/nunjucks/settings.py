from django.conf import settings

DEBUG = getattr(settings, "NUNJUCKS_DEBUG", settings.DEBUG)
NUNJUCKS_BIN = getattr(settings, "NUNJUCKS_BIN", "nunjucks-precompile")
