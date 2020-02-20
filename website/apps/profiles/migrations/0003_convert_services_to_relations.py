# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def forwards_func(apps, schema_editor):
    print("forwards_func")
    Profile = apps.get_model("profiles", "Profile")
    Service = apps.get_model("profiles", "Service")
    Link = apps.get_model("profiles", "Link")

    qs = Profile.objects.exclude(service__isnull=True)
    for profile in qs:
        # print("=" * 72)
        # print(profile.user.username)
        for service in Service.objects.filter(profile=profile):
            url = None

            if service.service.title == 'Skype':
                Profile.objects.filter(pk=profile.pk).update(
                    skype=service.username
                )

            elif service.service.title == 'Twitter':
                title = "Twitter"
                url = 'https://twitter.com/{}'.format(service.username)

            elif service.service.title == 'Facebook':
                title = "Facebook"
                if service.username.startswith('http'):
                    url = service.username
                else:
                    url = 'https://www.facebook.com/{}'.format(service.username.replace(" ", "."))

            elif service.service.title == 'GitHub':
                title = "GitHub"
                url = 'https://github.com/{}'.format(service.username)

            if url:
                l, c = Link.objects.get_or_create(
                    profile=profile,
                    title=title,
                    url=url,
                )


def reverse_func(apps, schema_editor):
    print("reverse_func")


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0002_auto_20200220_1430"),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
