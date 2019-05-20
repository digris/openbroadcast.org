# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import alibrary.models.playlistmodels
import alibrary.util.storage


class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '0022_artist_summary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='main_image',
            field=models.ImageField(storage=alibrary.util.storage.OverwriteStorage(), upload_to=alibrary.models.playlistmodels.upload_image_to, null=True, verbose_name='Image', blank=True),
        ),
    ]
