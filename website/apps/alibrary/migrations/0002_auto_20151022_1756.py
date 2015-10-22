# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='license',
            name='uuid',
            field=models.CharField(default=b'2aa90796-c3a5-4a80-b024-f96a4661d099', max_length=36, editable=False),
        ),
    ]
