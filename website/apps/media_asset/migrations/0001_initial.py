# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Format',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)),
                ('status', models.PositiveIntegerField(default=0, db_index=True, choices=[(0, 'initial'), (1, 'completed'), (2, 'processing'), (99, 'error')])),
                ('encoding', models.CharField(default='mp3', max_length=4, db_index=True, choices=[('mp3', 'MP3'), ('aac', 'AAC')])),
                ('quality', models.CharField(default='default', max_length=16, db_index=True, choices=[('default', 'Default'), ('lo', 'Lo-Fi'), ('hi', 'Hi-Fi'), ('preview', 'Preview')])),
                ('filesize', models.PositiveIntegerField(null=True, verbose_name='Filesize', blank=True)),
                ('accessed', models.DateTimeField(auto_now_add=True)),
                ('media_uuid', models.UUIDField(null=True, blank=True)),
                ('media', models.ForeignKey(related_name='formats', to='alibrary.Media', null=True)),
            ],
            options={
                'verbose_name': 'Format',
            },
        ),
        migrations.CreateModel(
            name='Waveform',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)),
                ('status', models.PositiveIntegerField(default=0, choices=[(0, 'initial'), (1, 'completed'), (2, 'processing'), (99, 'error')])),
                ('type', models.CharField(default='w', max_length=64, db_index=True, choices=[('w', 'Waveform'), ('s', 'Spectrogram')])),
                ('accessed', models.DateTimeField(auto_now_add=True)),
                ('media_uuid', models.UUIDField(null=True, blank=True)),
                ('media', models.ForeignKey(related_name='waveforms', to='alibrary.Media', null=True)),
            ],
            options={
                'verbose_name': 'Waveform',
            },
        ),
        migrations.AlterUniqueTogether(
            name='waveform',
            unique_together=set([('media', 'type')]),
        ),
        migrations.AlterUniqueTogether(
            name='format',
            unique_together=set([('media', 'encoding', 'quality')]),
        ),
    ]
