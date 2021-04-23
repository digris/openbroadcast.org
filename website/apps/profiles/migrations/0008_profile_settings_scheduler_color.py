# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0007_auto_20210416_0846"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="settings_scheduler_color",
            field=models.CharField(max_length=7, null=True, blank=True),
        ),
    ]
