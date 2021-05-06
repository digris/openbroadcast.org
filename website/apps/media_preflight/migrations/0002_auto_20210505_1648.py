# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ("media_preflight", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="preflightcheck",
            name="created",
            field=models.DateTimeField(
                default=datetime.datetime(2021, 5, 5, 16, 48, 16, 582052),
                auto_now_add=True,
                db_index=True,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="preflightcheck",
            name="updated",
            field=models.DateTimeField(
                default=datetime.datetime(2021, 5, 5, 16, 48, 18, 679990),
                auto_now=True,
                db_index=True,
            ),
            preserve_default=False,
        ),
    ]
