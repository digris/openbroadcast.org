# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iptracker', '0002_auto_20160107_2151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='ip',
            field=models.GenericIPAddressField(null=True),
        ),
    ]
