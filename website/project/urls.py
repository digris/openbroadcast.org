# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from django.conf.urls import include, url

from django.conf import settings
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
from django.contrib import admin
from cms.sitemaps import CMSSitemap
from django.contrib.sitemaps.views import sitemap
from alibrary.sitemap import ReleaseSitemap

from .urls_api import api

from loginas.views import user_login as loginas_user

DEBUG = getattr(settings, "DEBUG", False)


def handler500(request):

    from django.template import Context, loader
    from django.http import HttpResponseServerError

    t = loader.get_template("500.html")
    return HttpResponseServerError(t.render(Context({"request": request})))


sitemaps = {"releases": ReleaseSitemap, "pages": CMSSitemap}

admin.autodiscover()
admin.site.site_header = "open broadcast"
admin.site.site_title = "open broadcast"

dajaxice_autodiscover()

urlpatterns = [
    url(r"^admin/", include(admin.site.urls)),
    url(r"^vote/", include("arating.urls")),
    url(r"^ac_tagging/", include("ac_tagging.urls")),
    url(r"^api/", include(api.urls)),
    # api v2 patterns
    url(r"^api/v2/", include("project.urls_apiv2", namespace="api")),
    url(r"^postman/", include("postman.urls")),
    url(dajaxice_config.dajaxice_url, include("dajaxice.urls")),
    # registration
    # url(r'^accounts/', include('invitation.urls')),
    url(r"^accounts/", include("registration.backends.simple.urls")),
    # refactoring account (login/registration/logout)
    url("^account/", include("account.urls", namespace="account")),
    url(r"^s/", include("social_django.urls", namespace="social")),
    # url("^account/", include("django.contrib.auth.urls")),
    # url(r"^accounts/login_as/(?P<user_id>.+)/$", "loginas.views.user_login", name="loginas-user-login"),
    url(
        r"^accounts/login_as/(?P<user_id>.+)/$", loginas_user, name="loginas-user-login"
    ),
    url(r"^captcha/", include("captcha.urls")),
    # massimporter / maintainer extra urls
    url(r"^admin-extra/", include("massimporter.urls")),
    url(r"^collection/", include("collection.urls", namespace="collection")),
    # url(r'^search/', include('search.urls')),
    url(r"^sitemap.xml$", sitemap, {"sitemaps": sitemaps}),
    url(r"^player-ng/", include("player.urls", namespace="player")),
    url(r"^media-asset/", include("media_asset.urls")),
    url(r"^webhooks/import/", include("massimporter.webhook.urls")),
]


if settings.SERVE_MEDIA:
    urlpatterns += [url(r"", include("staticfiles.urls"))]

if DEBUG:

    try:
        import debug_toolbar

        urlpatterns += [url(r"^__debug__/", include(debug_toolbar.urls))]
    except Exception as e:
        pass

    from django.views.static import serve

    urlpatterns += [
        url(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT})
    ]

urlpatterns += [url(r"^", include("cms.urls"))]
