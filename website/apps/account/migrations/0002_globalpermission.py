# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="GlobalPermission",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
            ],
            options={
                "default_permissions": (),
                "managed": False,
                "permissions": (
                    ("view_obr_sync_api", "Read from OBR Sync API"),
                    ("edit_obr_sync_api", "Write to OBR Sync API"),
                ),
            },
        ),
    ]
