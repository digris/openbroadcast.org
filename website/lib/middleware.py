from django.core.urlresolvers import reverse

import settings


PRETTIFY = False
try:
    PRETTIFY = settings.PRETTIFY
except Exception:
    pass

try:
    from BeautifulSoup import BeautifulSoup
except Exception:
    PRETTIFY = False
    

class PrettifyMiddlewareBS(object):
    """HTML code prettification middleware."""
    def process_response(self, request, response):
        if request.path.startswith(reverse('admin:index')):
            return response
        if PRETTIFY and response['Content-Type'].split(';', 1)[0] == 'text/html':
            response.content = BeautifulSoup(response.content).prettify()
        return response
    
    
import sys
import tempfile
import hotshot
import hotshot.stats
from cStringIO import StringIO

class ProfileMiddleware(object):
    """
    Displays hotshot profiling for any view.
    http://yoursite.com/yourview/?prof

    Add the "prof" key to query string by appending ?prof (or &prof=)
    and you'll see the profiling results in your browser.
    It's set up to only be available in django's debug mode,
    but you really shouldn't add this middleware to any production configuration.
    * Only tested on Linux
    """
    def process_request(self, request):
        if settings.DEBUG and request.GET.has_key('prof'):
            self.tmpfile = tempfile.NamedTemporaryFile()
            self.prof = hotshot.Profile(self.tmpfile.name)

    def process_view(self, request, callback, callback_args, callback_kwargs):
        if settings.DEBUG and request.GET.has_key('prof'):
            return self.prof.runcall(callback, request, *callback_args, **callback_kwargs)

    def process_response(self, request, response):
        if settings.DEBUG and request.GET.has_key('prof'):
            self.prof.close()

            out = StringIO()
            old_stdout = sys.stdout
            sys.stdout = out

            stats = hotshot.stats.load(self.tmpfile.name)
            #stats.strip_dirs()
            stats.sort_stats('time', 'calls')
            stats.print_stats()

            sys.stdout = old_stdout
            stats_str = out.getvalue()

            if response and response.content and stats_str:
                response.content = response.content + "<pre>" + stats_str + "</pre>"

        return response
