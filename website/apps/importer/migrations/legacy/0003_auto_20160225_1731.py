# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import importer.models


class Migration(migrations.Migration):

    dependencies = [
        ('importer', '0002_auto_20151126_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='importfile',
            name='file',
            field=models.FileField(max_length=1024, upload_to=importer.models.clean_upload_path),
        ),
        migrations.AlterField(
            model_name='importfile',
            name='filename',
            field=models.CharField(max_length=1024, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='importfile',
            name='status',
            field=models.PositiveIntegerField(default=0, choices=[(0, 'Init'), (1, 'Done'), (2, 'Ready'), (3, 'Working'), (4, 'Warning'), (5, 'Duplicate'), (6, 'Queued'), (7, 'Importing'), (99, 'Error'), (11, 'Other')]),
        ),
    ]
