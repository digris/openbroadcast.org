# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '0014_auto_20160219_1708'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='distributor',
            name='level',
        ),
        migrations.RemoveField(
            model_name='distributor',
            name='lft',
        ),
        migrations.RemoveField(
            model_name='distributor',
            name='rght',
        ),
        migrations.RemoveField(
            model_name='distributor',
            name='tree_id',
        ),
        migrations.AlterField(
            model_name='distributor',
            name='parent',
            field=models.ForeignKey(related_name='children', blank=True, to='alibrary.Distributor', null=True),
        ),
    ]
