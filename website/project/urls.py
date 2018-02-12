# -*- coding: utf-8 -*-
from django.conf.urls import include, url

from django.views.defaults import page_not_found, server_error
from django.conf import settings
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
from urls_api import api
from django.contrib import admin
from cms.sitemaps import CMSSitemap
from django.contrib.sitemaps.views import sitemap
from alibrary.sitemap import ReleaseSitemap

DEBUG = getattr(settings, 'DEBUG', False)

def handler500(request):

    from django.template import Context, loader
    from django.http import HttpResponseServerError

    t = loader.get_template('500.html')
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

urlpatterns = [

    url(r"^admin/", include(admin.site.urls)),
    url(r"^vote/", include('arating.urls')),
    url(r'^ac_tagging/', include('ac_tagging.urls')),
    url(r'^api/', include(api.urls)),
    # api v2 patterns
    url(r'^api/v2/', include('project.urls_apiv2', namespace='api')),
    url(r'^oauth2/', include('provider.oauth2.urls', namespace = 'oauth2')),
    url(r'^comments/', include('fluent_comments.urls')),
    url(r'^postman/', include('postman.urls')),
    url(r'^selectable/', include('selectable.urls')),
    url(r'^ip/', include('iptracker.urls')),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),

    # registration
    #url(r'^accounts/', include('invitation.urls')),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r"^accounts/login_as/(?P<user_id>.+)/$", "loginas.views.user_login", name="loginas-user-login"),
    url(r'^sa/', include('social_auth.urls')),
    url(r'^captcha/', include('captcha.urls')),

    url(r"^announcements/", include("announcements.urls")),

    # filer (protected)
    url(r'^', include('filer.server.urls')),
    # only devel
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }),

    # massimporter / maintainer extra urls
    url(r'^admin-extra/', include('massimporter.urls')),


    url(r'^collection/', include('collection.urls', namespace='collection')),

    url(r'^search/', include('search.urls')),
    url(r'^search-hs/', include('haystack.urls')),
    url(r'^sitemap.xml$', sitemap, {'sitemaps': sitemaps}),

    url(r'^player/', include('aplayer.urls')),
    url(r'^media-asset/', include('media_asset.urls')),

    url(r'^webhooks/import/', include('massimporter.webhook.urls')),

]


if settings.SERVE_MEDIA:
    urlpatterns += [
        url(r"", include("staticfiles.urls")),
    ]

if DEBUG:

    try:
        import debug_toolbar
        urlpatterns += [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ]
    except Exception as e:
        pass

    from django.views.static import serve

    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]

urlpatterns += [
    url(r'^', include('cms.urls')),
]
