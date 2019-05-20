# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '0013_label_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='label',
            name='parent',
            field=models.ForeignKey(related_name='children', blank=True, to='alibrary.Label', null=True),
        ),
    ]
