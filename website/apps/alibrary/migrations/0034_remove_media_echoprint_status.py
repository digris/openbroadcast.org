# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '0033_auto_20170725_1324'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='media',
            name='echoprint_status',
        ),
    ]
