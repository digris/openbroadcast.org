# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Waveform',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)),
                ('status', models.PositiveIntegerField(default=0, choices=[(0, 'initial'), (1, 'completed'), (2, 'processing'), (99, 'error')])),
                ('type', models.CharField(default='waveform', max_length=64, choices=[('waveform', 'Waveform'), ('spectrogram', 'Spectrogram')])),
                ('media', models.ForeignKey(to='alibrary.Media')),
            ],
            options={
                'verbose_name': 'Waveform',
            },
        ),
    ]
