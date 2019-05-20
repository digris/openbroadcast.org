# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '0024_auto_20160526_1618'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apilookup',
            name='content_type',
        ),
        migrations.DeleteModel(
            name='APILookup',
        ),
    ]
