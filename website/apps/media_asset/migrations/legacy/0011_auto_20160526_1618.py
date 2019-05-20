# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media_asset', '0010_auto_20151124_1348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='format',
            name='status',
            field=models.PositiveIntegerField(default=0, db_index=True, choices=[(0, 'initial'), (1, 'completed'), (2, 'processing'), (99, 'error')]),
        ),
        migrations.AlterField(
            model_name='waveform',
            name='media',
            field=models.ForeignKey(related_name='waveforms', to='alibrary.Media', null=True),
        ),
        migrations.AlterField(
            model_name='waveform',
            name='type',
            field=models.CharField(default='w', max_length=64, db_index=True, choices=[('w', 'Waveform'), ('s', 'Spectrogram')]),
        ),
    ]
