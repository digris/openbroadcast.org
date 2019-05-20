# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '0042_remove_agency'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Service',
        ),
    ]
