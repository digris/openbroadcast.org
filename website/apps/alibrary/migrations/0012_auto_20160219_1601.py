# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '0011_auto_20160219_1538'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='label',
            name='level',
        ),
        migrations.RemoveField(
            model_name='label',
            name='lft',
        ),
        migrations.RemoveField(
            model_name='label',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='label',
            name='rght',
        ),
        migrations.RemoveField(
            model_name='label',
            name='tree_id',
        ),
    ]
