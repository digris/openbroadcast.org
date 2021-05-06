# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ("media_preflight", "0003_auto_20210505_1842"),
    ]

    operations = [
        migrations.AddField(
            model_name="preflightcheck",
            name="warnings",
            field=jsonfield.fields.JSONField(default=[], editable=False),
        ),
        migrations.AlterField(
            model_name="preflightcheck",
            name="checks",
            field=jsonfield.fields.JSONField(default={}, editable=False),
        ),
        migrations.AlterField(
            model_name="preflightcheck",
            name="errors",
            field=jsonfield.fields.JSONField(default=[], editable=False),
        ),
    ]
