# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '0032_auto_20170725_1310'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='media',
            name='danceability',
        ),
        migrations.RemoveField(
            model_name='media',
            name='echonest_duration',
        ),
        migrations.RemoveField(
            model_name='media',
            name='echonest_id',
        ),
        migrations.RemoveField(
            model_name='media',
            name='energy',
        ),
        migrations.RemoveField(
            model_name='media',
            name='key',
        ),
        migrations.RemoveField(
            model_name='media',
            name='liveness',
        ),
        migrations.RemoveField(
            model_name='media',
            name='loudness',
        ),
        migrations.RemoveField(
            model_name='media',
            name='sections',
        ),
        migrations.RemoveField(
            model_name='media',
            name='speechiness',
        ),
        migrations.RemoveField(
            model_name='media',
            name='start_of_fade_out',
        ),
    ]
