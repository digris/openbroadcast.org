# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '0043_remove_service'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='distributor',
            name='creator',
        ),
        migrations.RemoveField(
            model_name='distributor',
            name='first_placeholder',
        ),
        migrations.RemoveField(
            model_name='distributor',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='distributor',
            name='publisher',
        ),
    ]
