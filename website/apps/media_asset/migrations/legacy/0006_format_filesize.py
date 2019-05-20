# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media_asset', '0005_auto_20151124_1046'),
    ]

    operations = [
        migrations.AddField(
            model_name='format',
            name='filesize',
            field=models.PositiveIntegerField(null=True, verbose_name='Filesize', blank=True),
        ),
    ]
