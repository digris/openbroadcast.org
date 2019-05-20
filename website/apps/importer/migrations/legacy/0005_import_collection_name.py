# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('importer', '0004_auto_20160526_1618'),
    ]

    operations = [
        migrations.AddField(
            model_name='import',
            name='collection_name',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
    ]
