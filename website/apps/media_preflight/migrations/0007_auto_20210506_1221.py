# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("media_preflight", "0006_auto_20210506_1133"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="preflightcheck",
            name="preflight_ok",
        ),
        migrations.RemoveField(
            model_name="preflightcheck",
            name="result",
        ),
    ]
