# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0005_profile_settings_show_appearances"),
    ]

    operations = [
        migrations.RenameField(
            model_name="profile",
            old_name="settings_show_appearances",
            new_name="settings_show_media_appearances",
        ),
        migrations.AddField(
            model_name="profile",
            name="settings_show_media_history",
            field=models.BooleanField(
                default=True, verbose_name="Show media emission history"
            ),
        ),
    ]
