from django.core.urlresolvers import reverse


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
                "name": "Approve as MUSIC PROFESSIONAL",
                "url": reverse(
                    "profiles:profile-mentor-approve",
                    kwargs={"pk": profile.pk, "level": "music_pro"},
                ),
            },
            {
                "name": "Approve as RADIO PROFESSIONAL",
                "url": reverse(
                    "profiles:profile-mentor-approve",
                    kwargs={"pk": profile.pk, "level": "radio_pro"},
                ),
            },
            {
                "name": "Cancel mentorship",
                "url": reverse(
                    "profiles:profile-mentor-cancel", kwargs={"pk": profile.pk}
                ),
            },
        ]

    elif not profile.mentor:
        return [
            {
                "name": "Become the mentor",
                "url": reverse(
                    "profiles:profile-mentor-become", kwargs={"pk": profile.pk}
                ),
            },
        ]

    return []
