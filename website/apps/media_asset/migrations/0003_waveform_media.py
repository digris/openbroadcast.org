# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '0005_auto_20151027_1418'),
        ('media_asset', '0002_auto_20151022_1754'),
    ]

    operations = [
        migrations.AddField(
            model_name='waveform',
            name='media',
            field=models.ForeignKey(to='alibrary.Media', null=True),
        ),
    ]
