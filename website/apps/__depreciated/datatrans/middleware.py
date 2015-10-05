from django.utils.cache import patch_vary_headers
from django.utils import translation


class MinimalLocaleMiddleware(object):
    """
    This is a minimal version of the LocaleMiddleware from Django.
    It only supports setting the current language from sessions.
    This allows the main site to be in one language while the site
    administrators can switch the language, so they don't experience
    problems while editing original database content when this is not
    in the main site's language.
    """

    def process_request(self, request):
        language = get_language_from_request(request)
        translation.activate(language)
        request.LANGUAGE_CODE = translation.get_language()

    def process_response(self, request, response):
        patch_vary_headers(response, ('Accept-Language',))
        if 'Content-Language' not in response:
            response['Content-Language'] = translation.get_language()
        translation.deactivate()
        return response


def get_language_from_request(request):
    from django.conf import settings
    supported = dict(settings.LANGUAGES)

    if hasattr(request, 'session'):
        lang_code = request.session.get('django_language', None)
        if lang_code in supported and lang_code is not None:
            return lang_code
    return settings.LANGUAGE_CODE
