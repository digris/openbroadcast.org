# -*- coding: utf-8 -*-
import autocomplete_light
from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.views.defaults import page_not_found, server_error
from django.conf import settings
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
from urls_api import api
from django.contrib import admin
from cms.sitemaps import CMSSitemap
from alibrary.sitemap import ReleaseSitemap

DEBUG = getattr(settings, 'DEBUG', False)

def handler500(request):

    from django.template import Context, loader
    from django.http import HttpResponseServerError

    t = loader.get_template('500.html') # You need to create a 500.html template.
    return HttpResponseServerError(t.render(Context({
        'request': request,
    })))


sitemaps = {
    'releases': ReleaseSitemap,
    'pages': CMSSitemap,
}

admin.autodiscover()
admin.site.site_header = "Open Broadcast"
admin.site.site_title = "Open Broadcast"


dajaxice_autodiscover()
autocomplete_light.autodiscover()

urlpatterns = patterns('',

    # django-su
    #url(r"^admin/su/", include("django_su.urls")),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r"^admin/", include(admin.site.urls)),
    url(r'^backfeed/', include('backfeed.urls')),
    url(r"^vote/", include('arating.urls')),
    url(r'^ac_tagging/', include('ac_tagging.urls')),
    url(r'^autocomplete/', include('autocomplete_light.urls')),
    url(r'^api/', include(api.urls)),
    url(r'^oauth2/', include('provider.oauth2.urls', namespace = 'oauth2')),
    url(r'^comments/', include('fluent_comments.urls')),
    url(r'^postman/', include('postman.urls')),
    url(r'^selectable/', include('selectable.urls')),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),

    # registration
    #url(r'^accounts/', include('invitation.urls')),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r"^accounts/login_as/(?P<user_id>.+)/$", "loginas.views.user_login", name="loginas-user-login"),
    url(r'^sa/', include('social_auth.urls')),

    url(r"^announcements/", include("announcements.urls")),

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
    (r'^media-asset/', include('media_asset.urls')),

    #url(r'^bb/', include('django_badbrowser.urls')),

)


if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
        url(r"", include("staticfiles.urls")),
)

if DEBUG:

    try:
        import debug_toolbar
        urlpatterns += patterns('',
            url(r'^__debug__/', include(debug_toolbar.urls)),
        )
    except Exception as e:
        pass

    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
)

#urlpatterns += i18n_patterns('',
urlpatterns += patterns('',
    url(r'^', include('cms.urls')),
)