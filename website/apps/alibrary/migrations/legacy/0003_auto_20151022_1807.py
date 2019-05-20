# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '0002_auto_20151022_1756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='license',
            name='uuid',
            field=models.CharField(default=b'<function uuid4 at 0x10d6becf8>', max_length=36, editable=False),
        ),
    ]
