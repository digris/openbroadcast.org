# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from jsonfield import JSONField


class Migration(migrations.Migration):

    dependencies = [
        ('media_preflight', '0002_remove_preflightcheck_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='preflightcheck',
            name='result',
            field=JSONField(null=True, blank=True),
        ),
    ]
