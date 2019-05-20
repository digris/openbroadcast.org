# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media_asset', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='waveform',
            name='media',
        ),
        migrations.AlterField(
            model_name='waveform',
            name='type',
            field=models.CharField(default='w', max_length=64, choices=[('w', 'Waveform'), ('s', 'Spectrogram')]),
        ),
    ]
