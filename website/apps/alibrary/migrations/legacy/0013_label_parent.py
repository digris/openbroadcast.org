# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '0012_auto_20160219_1601'),
    ]

    operations = [
        migrations.AddField(
            model_name='label',
            name='parent',
            field=models.ForeignKey(blank=True, to='alibrary.Label', null=True),
        ),
    ]
