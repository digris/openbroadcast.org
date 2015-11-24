# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('media_asset', '0007_format_accessed'),
    ]

    operations = [
        migrations.AddField(
            model_name='waveform',
            name='accessed',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 24, 11, 45, 15, 656346), auto_now_add=True),
            preserve_default=False,
        ),
    ]
