# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.core.urlresolvers import reverse

log = logging.getLogger(__name__)


def _get_profile_actions(obj, user):

    actions = []

    if user.has_perm("alibrary.play_media"):
        pass

        # TODO: highly experimental... play user's recent "likes"
        vote_qs = (
            obj.user.votes.filter(vote__gt=0)
            .order_by("-created")
            .prefetch_related("content_object")
        )

        if vote_qs.exists():
            actions.append({"key": "play", "title": "Play"})

    if user == obj.user:
        actions.append(
            {"key": "edit", "title": "Edit", "url": obj.get_edit_url(),}
        )

    if user.is_authenticated() and not user == obj.user:
        actions.append(
            {
                "key": "message",
                "title": "Send Message",
                "url": reverse(
                    "postman_write", kwargs={"recipients": obj.user.username}
                ),
            }
        )

    if user.is_staff:
        actions.append(
            {"key": "admin", "title": "Admin view", "url": obj.get_admin_url(),}
        )
        actions.append(
            {
                "key": "loginas",
                "title": "Login as user",
                "url": reverse("loginas-user-login", kwargs={"user_id": obj.user.pk}),
            }
        )

    return actions


def _get_playlist_actions(obj, user):

    actions = []

    if user.has_perm("alibrary.play_media"):
        actions.append({"key": "play", "title": "Play"})
        actions.append({"key": "queue", "title": "Queue"})

    if user.has_perm("alibrary.downoad_media"):
        actions.append({"key": "download", "title": "Download"})

    if user == obj.user:
        actions.append({"key": "edit", "title": "Edit", "url": obj.get_edit_url()})

    if user.has_perm("alibrary.schedule_playlist") and obj.type == "broadcast":
        actions.append({"key": "schedule", "title": "Schedule for playout"})

    if user.is_staff:
        actions.append(
            {"key": "admin", "title": "Admin view", "url": obj.get_admin_url()}
        )

    return actions


def _get_release_actions(obj, user):

    actions = []

    if user.has_perm("alibrary.play_media"):
        actions.append({"key": "play", "title": "Play"})
        actions.append({"key": "queue", "title": "Queue"})

    if user.has_perm("alibrary.downoad_media"):
        actions.append({"key": "download", "title": "Download"})

    if user.has_perm("alibrary.edit_release"):
        actions.append({"key": "edit", "title": "Edit", "url": obj.get_edit_url()})

    if user.is_staff:
        actions.append(
            {"key": "admin", "title": "Admin view", "url": obj.get_admin_url()}
        )

    return actions


def _get_media_actions(obj, user):

    actions = []

    if user.has_perm("alibrary.play_media"):
        actions.append({"key": "play", "title": "Play"})
        actions.append({"key": "queue", "title": "Queue"})

    if user.has_perm("alibrary.downoad_media"):
        actions.append({"key": "download", "title": "Download"})

    if user.has_perm("alibrary.edit_media"):
        actions.append({"key": "edit", "title": "Edit", "url": obj.get_edit_url()})

    if user.is_staff:
        actions.append(
            {"key": "admin", "title": "Admin view", "url": obj.get_admin_url()}
        )

    return actions


def _get_artist_actions(obj, user):

    actions = []

    if user.has_perm("alibrary.play_media"):
        actions.append({"key": "play", "title": "Play"})
        actions.append({"key": "queue", "title": "Queue"})

    # if user.has_perm("alibrary.downoad_media"):
    #     actions.append({"key": "download", "title": "Download"})

    if user.has_perm("alibrary.edit_artist"):
        actions.append({"key": "edit", "title": "Edit", "url": obj.get_edit_url()})

    if user.is_staff:
        actions.append(
            {"key": "admin", "title": "Admin view", "url": obj.get_admin_url()}
        )

    return actions


def _get_label_actions(obj, user):

    actions = []

    # if user.has_perm("alibrary.play_media"):
    #     actions.append({"key": "play", "title": "Play"})
    #     actions.append({"key": "queue", "title": "Queue"})

    if user.has_perm("alibrary.edit_label"):
        actions.append({"key": "edit", "title": "Edit", "url": obj.get_edit_url()})

    if user.is_staff:
        actions.append(
            {"key": "admin", "title": "Admin view", "url": obj.get_admin_url()}
        )

    return actions


ACTION_LOOKUP_FUNCTIONS = {
    "profiles.profile": _get_profile_actions,
    "alibrary.playlist": _get_playlist_actions,
    "alibrary.release": _get_release_actions,
    "alibrary.media": _get_media_actions,
    "alibrary.artist": _get_artist_actions,
    "alibrary.label": _get_label_actions,
}


def get_object_actions_for_user(obj, user=None):

    ct = obj.get_ct()

    # log.debug("getting object permissions for {}".format(ct))

    if not ct in ACTION_LOOKUP_FUNCTIONS:
        raise Exception("no lookup function for {}".format(ct))

    return ACTION_LOOKUP_FUNCTIONS[ct](obj, user)

    # if ct == 'profiles.profile':
    #     return _get_profile_actions(obj, user)
    #
    # return []
