# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('massimporter', '0006_auto_20170127_1504'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='massimport',
            options={'ordering': ('-created',), 'verbose_name': 'Import', 'verbose_name_plural': 'Imports', 'permissions': (('massimport_manage', 'Manage Massimporter Sessions'),)},
        ),
    ]
