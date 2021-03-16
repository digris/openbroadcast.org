# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


def get_mentoring_actions_for_profile(profile, mentor):

    if not (
        mentor
        and mentor.is_authenticated()
        and mentor.has_perm("profiles.mentor_profiles")
    ):
        return []

    if profile.mentor == mentor and not profile.is_approved:

        return [
            {
                "name": _("Approve as MUSIC PROFESSIONAL"),
                "url": reverse(
                    "profiles-profile-mentor-approve",
                    kwargs={"pk": profile.pk, "level": "music_pro"},
                ),
            },
            {
                "name": _("Approve as RADIO PROFESSIONAL"),
                "url": reverse(
                    "profiles-profile-mentor-approve",
                    kwargs={"pk": profile.pk, "level": "radio_pro"},
                ),
            },
            {
                "name": _("Cancel mentorship"),
                "url": reverse(
                    "profiles-profile-mentor-cancel", kwargs={"pk": profile.pk}
                ),
            },
        ]

    elif not profile.mentor:

        return [
            {
                "name": _("Become the mentor"),
                "url": reverse(
                    "profiles-profile-mentor-become", kwargs={"pk": profile.pk}
                ),
            },
        ]

    return []
