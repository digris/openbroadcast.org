# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('importer', '0003_auto_20160225_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='import',
            name='notes',
            field=models.TextField(null=True, blank=True),
        ),
    ]
