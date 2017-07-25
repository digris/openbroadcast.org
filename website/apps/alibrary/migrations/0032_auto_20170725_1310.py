# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '0031_media_fprint_ingested'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='media',
            name='base_bitrate',
        ),
        migrations.RemoveField(
            model_name='media',
            name='base_duration',
        ),
        migrations.RemoveField(
            model_name='media',
            name='base_filesize',
        ),
        migrations.RemoveField(
            model_name='media',
            name='base_format',
        ),
        migrations.RemoveField(
            model_name='media',
            name='base_samplerate',
        ),
        migrations.AlterField(
            model_name='media',
            name='fprint_ingested',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
