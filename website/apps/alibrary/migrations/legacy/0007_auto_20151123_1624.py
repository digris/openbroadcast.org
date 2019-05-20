# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '0006_auto_20151027_2116'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='master_bitrate',
            field=models.PositiveIntegerField(null=True, verbose_name='Bitrate', blank=True),
        ),
        migrations.AddField(
            model_name='media',
            name='master_duration',
            field=models.FloatField(null=True, verbose_name='Duration', blank=True),
        ),
        migrations.AddField(
            model_name='media',
            name='master_encoding',
            field=models.CharField(max_length=16, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='media',
            name='master_filesize',
            field=models.PositiveIntegerField(null=True, verbose_name='Filesize', blank=True),
        ),
        migrations.AddField(
            model_name='media',
            name='master_samplerate',
            field=models.PositiveIntegerField(null=True, verbose_name='Samplerate', blank=True),
        ),
        migrations.AlterField(
            model_name='license',
            name='uuid',
            field=models.CharField(default=b'<function uuid4 at 0x104fd2ed8>', max_length=36, editable=False),
        ),
    ]
