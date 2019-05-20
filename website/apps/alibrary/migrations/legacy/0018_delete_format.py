# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '0017_auto_20160220_1644'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Format',
        ),
    ]
