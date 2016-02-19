# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '0015_auto_20160219_1709'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agency',
            name='level',
        ),
        migrations.RemoveField(
            model_name='agency',
            name='lft',
        ),
        migrations.RemoveField(
            model_name='agency',
            name='rght',
        ),
        migrations.RemoveField(
            model_name='agency',
            name='tree_id',
        ),
        migrations.RemoveField(
            model_name='license',
            name='level',
        ),
        migrations.RemoveField(
            model_name='license',
            name='lft',
        ),
        migrations.RemoveField(
            model_name='license',
            name='rght',
        ),
        migrations.RemoveField(
            model_name='license',
            name='tree_id',
        ),
        migrations.AlterField(
            model_name='agency',
            name='parent',
            field=models.ForeignKey(related_name='children', blank=True, to='alibrary.Agency', null=True),
        ),
        migrations.AlterField(
            model_name='license',
            name='parent',
            field=models.ForeignKey(related_name='license_children', blank=True, to='alibrary.License', null=True),
        ),
    ]
