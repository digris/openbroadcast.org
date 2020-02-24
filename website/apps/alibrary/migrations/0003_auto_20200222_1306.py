# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '0002_auto_20200221_1825'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='media',
            options={'ordering': ('medianumber', 'tracknumber', 'name'), 'verbose_name': 'Track', 'verbose_name_plural': 'Tracks', 'permissions': (('play_media', 'Play Track'), ('downoad_media', 'Download Track'), ('download_master', 'Download Master'), ('merge_media', 'Merge Tracks'), ('reassign_media', 'Re-assign Tracks'), ('admin_media', 'Edit Track (extended)'), ('upload_media', 'Upload Track'))},
        ),
    ]
