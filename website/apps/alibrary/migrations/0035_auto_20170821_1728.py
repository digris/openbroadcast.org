# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import alibrary.models.playlistmodels


class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '0034_remove_media_echoprint_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playlistmedia',
            name='media',
        ),
        migrations.RemoveField(
            model_name='playlistmedia',
            name='playlist',
        ),
        migrations.AlterField(
            model_name='playlist',
            name='mixdown_file',
            field=models.FileField(null=True, upload_to=alibrary.models.playlistmodels.upload_mixdown_to, blank=True),
        ),
        migrations.DeleteModel(
            name='PlaylistMedia',
        ),
    ]
