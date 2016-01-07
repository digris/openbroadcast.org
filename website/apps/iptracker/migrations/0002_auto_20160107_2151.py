# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iptracker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='ip',
            field=models.IPAddressField(null=True),
        ),
    ]
