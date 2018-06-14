# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '0046_fix_postgres_types'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profession',
            name='created',
        ),
        migrations.RemoveField(
            model_name='profession',
            name='updated',
        ),
    ]
