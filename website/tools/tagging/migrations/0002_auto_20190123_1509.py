# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('tagging', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 23, 15, 9, 10, 627422), auto_now_add=True, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tag',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 23, 15, 9, 15, 22562), auto_now=True, db_index=True),
            preserve_default=False,
        ),
    ]
