from django.conf.urls import *
from django.views.defaults import page_not_found, server_error
from django.conf import settings



def handler500(request):

    from django.template import Context, loader
    from django.http import HttpResponseServerError

    t = loader.get_template('500.html') # You need to create a 500.html template.
    return HttpResponseServerError(t.render(Context({
        'request': request,
    })))


# error handlers
#handler403 = 'lib.errors.views.handler403'

import autocomplete_light
autocomplete_light.autodiscover()

from django.contrib import admin

from cms.sitemaps import CMSSitemap

from alibrary.sitemap import ReleaseSitemap

sitemaps = {
    'releases': ReleaseSitemap,
    'pages': CMSSitemap,
}

admin.autodiscover()

from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()


from urls_api import api
import debug_toolbar

urlpatterns = patterns('',

    # django-su
    #url(r"^admin/su/", include("django_su.urls")),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r"^admin/", include(admin.site.urls)),

    url(r'^backfeed/', include('backfeed.urls')),

    url(r'uploader/', include('multiuploader.urls')),


    url(r"^vote/", include('arating.urls')),
    url(r'^ac_tagging/', include('ac_tagging.urls')),
    url(r'^autocomplete/', include('autocomplete_light.urls')),

    url(r'^api/', include(api.urls)),

    url(r'^oauth2/', include('provider.oauth2.urls', namespace = 'oauth2')),
    url(r'^comments/', include('fluent_comments.urls')),
    url(r'^postman/', include('postman.urls')),

    url(r'^selectable/', include('selectable.urls')),
    
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    
    # varnish / ESI
    #url(r'^esi/', include('esi.urls')),
    
    # registration
    #url(r'^accounts/', include('invitation.urls')),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r"^accounts/login_as/(?P<user_id>.+)/$", "loginas.views.user_login", name="loginas-user-login"),
    url(r'^sa/', include('social_auth.urls')),

    # filer (protected)
    (r'^', include('filer.server.urls')),
    
    # only devel
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }),
    
    url(r'^search/', include('asearch.urls')),
    url(r'^search/', include('haystack.urls')),
    
    url(r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),

    (r'^player/', include('aplayer.urls')),
    
    #url(r'^bb/', include('django_badbrowser.urls')),
    #url(r'^translate/', include('datatrans.urls')),

    url(r'^__debug__/', include(debug_toolbar.urls)),
    
    # cms base
    url(r'^', include('cms.urls')),
)


if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
        url(r"", include("staticfiles.urls")),
)

if settings.DEBUG:

    urlpatterns += patterns('',

        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
)