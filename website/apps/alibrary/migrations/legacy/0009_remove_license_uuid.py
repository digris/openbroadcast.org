# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '0008_auto_20151126_0950'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='license',
            name='uuid',
        ),
    ]
