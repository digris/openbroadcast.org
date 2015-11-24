# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media_asset', '0009_auto_20151124_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='format',
            name='media_uuid',
            field=models.UUIDField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='waveform',
            name='media_uuid',
            field=models.UUIDField(null=True, blank=True),
        ),
    ]
