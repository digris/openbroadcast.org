# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '0005_auto_20151027_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='license',
            name='uuid',
            field=models.CharField(default=b'<function uuid4 at 0x104169cf8>', max_length=36, editable=False),
        ),
    ]
