# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0006_auto_20210311_2030"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="enable_alpha_features",
            field=models.BooleanField(
                default=False, verbose_name="Enable experimental features"
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="settings_show_media_appearances",
            field=models.BooleanField(
                default=False, verbose_name="Show media appearances"
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="settings_show_media_history",
            field=models.BooleanField(
                default=False, verbose_name="Show media emission history"
            ),
        ),
    ]
