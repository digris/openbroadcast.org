# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '0028_auto_20170418_1359'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='media',
            name='conversion_status',
        ),
        migrations.RemoveField(
            model_name='media',
            name='processed',
        ),
    ]
