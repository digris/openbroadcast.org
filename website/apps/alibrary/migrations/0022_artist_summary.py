# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_extensions.db.fields.json


class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '0021_auto_20160220_1737'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='summary',
            field=django_extensions.db.fields.json.JSONField(null=True, blank=True),
        ),
    ]
