# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '0030_auto_20170524_1925'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='fprint_ingested',
            field=models.DateTimeField(null=True, editable=False, blank=True),
        ),
    ]
