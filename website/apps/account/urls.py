# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy

from . import views

app_name = "account"
urlpatterns = [
    # login/logout flow
    # url(r"^$", RedirectView.as_view(url=reverse_lazy('account:login')), name="login"),
    url(r"^login/$", views.LoginView.as_view(), name="login"),
    url(r"^login/p/$", views.LoginPickupView.as_view(), name="login-pickup"),
    url(r"^logout/$", views.LogoutView.as_view(), name="logout"),
    # # registration flow
    url(r"^sign-up/$", views.RegistrationView.as_view(), name="register"),
    # # password reset flow
    url(
        r"^password/reset/$",
        views.PasswordRecoverView.as_view(),
        name="password-recover",
    ),
    url(
        r"^password/reset-sent/$",
        views.PasswordRecoverSentView.as_view(),
        name="password-recover-sent",
    ),
    url(
        r"^password/reset/(?P<uidb64>[\w:-]+)/(?P<token>[\w:-]+)/$",
        views.PasswordRecoverResetView.as_view(),
        name="password-recover-reset",
    ),
    # url(
    #     r"^password/reset-done/$",
    #     views.PasswordResetDoneView.as_view(),
    #     name="password-recover-reset-done",
    # ),
]
