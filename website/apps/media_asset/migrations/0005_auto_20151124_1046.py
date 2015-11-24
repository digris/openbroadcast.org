# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('media_asset', '0004_auto_20151027_2116'),
    ]

    operations = [
        migrations.AddField(
            model_name='format',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 24, 10, 45, 47, 42434), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='format',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 24, 10, 45, 51, 578956), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='waveform',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 24, 10, 46, 22, 213645), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='waveform',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 24, 10, 46, 25, 366069), auto_now=True),
            preserve_default=False,
        ),
    ]
