# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('massimporter', '0004_massimportfile_import_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='massimport',
            name='collection_name',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='massimport',
            name='status',
            field=models.PositiveIntegerField(default=0, choices=[(0, 'Init'), (1, 'Done'), (2, 'Queued'), (99, 'Error')]),
        ),
        migrations.AlterField(
            model_name='massimportfile',
            name='status',
            field=models.PositiveIntegerField(default=0, choices=[(0, 'Init'), (1, 'Done'), (2, 'Ready'), (3, 'Working'), (4, 'Warning'), (5, 'Duplicate'), (6, 'Queued'), (7, 'Importing'), (99, 'Error'), (11, 'Other')]),
        ),
    ]
