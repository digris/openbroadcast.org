# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_native_uuids'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='created',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='updated',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
    ]
