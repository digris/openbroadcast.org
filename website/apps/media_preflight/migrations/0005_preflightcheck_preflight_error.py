# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media_preflight', '0004_preflightcheck_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='preflightcheck',
            name='preflight_error',
            field=models.BooleanField(default=False),
        ),
    ]
