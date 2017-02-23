# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('massimporter', '0005_auto_20161013_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='massimportfile',
            name='status',
            field=models.PositiveIntegerField(default=0, db_index=True, choices=[(0, 'Init'), (1, 'Done'), (2, 'Ready'), (3, 'Working'), (4, 'Warning'), (5, 'Duplicate'), (6, 'Queued'), (7, 'Importing'), (99, 'Error'), (11, 'Other')]),
        ),
    ]
