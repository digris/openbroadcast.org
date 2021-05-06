# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ("media_preflight", "0002_auto_20210505_1648"),
    ]

    operations = [
        migrations.AddField(
            model_name="preflightcheck",
            name="checks",
            field=jsonfield.fields.JSONField(default={}),
        ),
        migrations.AddField(
            model_name="preflightcheck",
            name="errors",
            field=jsonfield.fields.JSONField(default=[]),
        ),
        migrations.AlterField(
            model_name="preflightcheck",
            name="status",
            field=models.PositiveSmallIntegerField(
                default=0,
                db_index=True,
                verbose_name="Status",
                choices=[(0, "Pending"), (1, "Running"), (2, "Done"), (99, "Error")],
            ),
        ),
    ]
