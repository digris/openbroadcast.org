# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media_preflight', '0003_preflightcheck_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='preflightcheck',
            name='status',
            field=models.PositiveSmallIntegerField(default=0, db_index=True, verbose_name='Status', choices=[(0, 'Initialized'), (1, 'Processing'), (2, 'Done'), (99, 'Error')]),
        ),
    ]
