# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('importer', '0003_auto_20160225_1731'),
        ('massimporter', '0003_auto_20160225_1730'),
    ]

    operations = [
        migrations.AddField(
            model_name='massimportfile',
            name='import_file',
            field=models.ForeignKey(to='importer.ImportFile', null=True),
        ),
    ]
