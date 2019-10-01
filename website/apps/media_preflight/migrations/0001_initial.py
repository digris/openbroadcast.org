# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [("alibrary", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="PreflightCheck",
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
                (
                    "status",
                    models.PositiveSmallIntegerField(
                        default=0,
                        db_index=True,
                        verbose_name="Status",
                        choices=[
                            (0, "Initialized"),
                            (1, "Processing"),
                            (2, "Done"),
                            (99, "Error"),
                        ],
                    ),
                ),
                ("result", jsonfield.fields.JSONField(null=True, blank=True)),
                ("preflight_ok", models.BooleanField(default=False)),
                (
                    "media",
                    models.OneToOneField(
                        related_name="preflight_check", null=True, to="alibrary.Media"
                    ),
                ),
            ],
        )
    ]
