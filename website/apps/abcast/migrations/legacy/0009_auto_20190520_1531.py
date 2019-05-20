# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abcast', '0008_refactoring_to_native_uuid'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='emission',
            options={'ordering': ('-time_start',), 'verbose_name': 'Emission', 'verbose_name_plural': 'Emissions', 'permissions': (('schedule_emission', 'Schedule Emission'),)},
        ),
        migrations.DeleteModel(
            name='Jingle',
        ),
        migrations.DeleteModel(
            name='JingleSet',
        ),
    ]
