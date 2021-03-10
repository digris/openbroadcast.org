# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0004_profile_d_tags"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="settings_show_appearances",
            field=models.BooleanField(
                default=True, verbose_name="Show media appearances"
            ),
        ),
    ]
