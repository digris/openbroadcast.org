# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url, include
from profiles import views

urlpatterns = [
    url(r"^$", views.ProfileListView.as_view(), name="profiles-profile-list"),
    url(
        r"^login-credentials/$",
        views.UserCredentialsView.as_view(),
        name="profiles-credentials-edit",
    ),
    url(r"^", include("invitation.urls")),
    url(
        r"^invitations/$",
        views.InvitationListView.as_view(),
        name="profiles-invitations",
    ),
    url(
        r"^invitations/(?P<pk>\d+)/delete/$",
        views.InvitationDeleteView.as_view(),
        name="profiles-invitation-delete",
    ),
    url(
        r"^force-login/(?P<username>[-\w.-_@]+)/$",
        views.profile_force_login,
        name="profiles-profile-force-login",
    ),
    url(
        r"^(?P<pk>\d+)/mentor/become/$",
        views.profile_mentor,
        {"cancel": False},
        name="profiles-profile-mentor-become",
    ),
    url(
        r"^(?P<pk>\d+)/mentor/cancel/$",
        views.profile_mentor,
        {"cancel": True},
        name="profiles-profile-mentor-cancel",
    ),
    url(
        r"^(?P<pk>\d+)/mentor/approve/(?P<level>[-\w]+)/$",
        views.profile_approve,
        name="profiles-profile-mentor-approve",
    ),
    url(
        r"^(?P<uuid>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/edit/$",
        views.ProfileEditView.as_view(),
        name="profiles-profile-edit",
    ),
    url(
        r"^(?P<uuid>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/(?:(?P<section>[-\w]+)/)?$",
        views.ProfileDetailView.as_view(),
        name="profiles-profile-detail",
    ),
]
