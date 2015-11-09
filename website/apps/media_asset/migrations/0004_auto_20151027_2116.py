# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '0006_auto_20151027_2116'),
        ('media_asset', '0003_waveform_media'),
    ]

    operations = [
        migrations.CreateModel(
            name='Format',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)),
                ('status', models.PositiveIntegerField(default=0, choices=[(0, 'initial'), (1, 'completed'), (2, 'processing'), (99, 'error')])),
                ('encoding', models.CharField(default='mp3', max_length=4, db_index=True, choices=[('mp3', 'MP3'), ('aac', 'AAC')])),
                ('quality', models.CharField(default='default', max_length=16, db_index=True, choices=[('default', 'Default'), ('lo', 'Lo-Fi'), ('hi', 'Hi-Fi'), ('preview', 'Preview')])),
                ('media', models.ForeignKey(related_name='formats', to='alibrary.Media', null=True)),
            ],
            options={
                'verbose_name': 'Format',
            },
        ),
        migrations.AlterField(
            model_name='waveform',
            name='media',
            field=models.ForeignKey(related_name='versions', to='alibrary.Media', null=True),
        ),
    ]
