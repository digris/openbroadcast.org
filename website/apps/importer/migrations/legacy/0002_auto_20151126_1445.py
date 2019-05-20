# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('importer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='import',
            name='type',
            field=models.CharField(default='web', max_length=10, choices=[('web', 'Web Interface'), ('api', 'API'), ('fs', 'Filesystem')]),
        ),
        migrations.AlterField(
            model_name='importfile',
            name='filename',
            field=models.CharField(db_index=True, max_length=250, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='importfile',
            name='status',
            field=models.PositiveIntegerField(default=0, choices=[(0, 'Init'), (1, 'Done'), (2, 'Ready'), (3, 'Progress'), (4, 'Warning'), (5, 'Dulicate'), (6, 'Queued'), (7, 'Importing'), (99, 'Error'), (11, 'Other')]),
        ),
    ]
