# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('media_asset', '0006_format_filesize'),
    ]

    operations = [
        migrations.AddField(
            model_name='format',
            name='accessed',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 24, 11, 44, 44, 372319), auto_now_add=True),
            preserve_default=False,
        ),
    ]
