# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('massimporter', '0002_auto_20160225_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='massimport',
            name='directory',
            field=models.CharField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='massimportfile',
            name='path',
            field=models.CharField(max_length=1024),
        ),
    ]
