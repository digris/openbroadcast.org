# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '0016_auto_20160219_1711'),
    ]

    operations = [
        # migrations.DeleteModel(
        #     name='Format',
        # ),
        migrations.RemoveField(
            model_name='artist',
            name='folder',
        ),
        migrations.RemoveField(
            model_name='label',
            name='folder',
        ),
        migrations.RemoveField(
            model_name='release',
            name='cover_image',
        ),
        migrations.RemoveField(
            model_name='release',
            name='folder',
        ),
        migrations.RemoveField(
            model_name='release',
            name='main_format',
        ),
        migrations.DeleteModel(
            name='Mediaformat',
        ),
    ]
