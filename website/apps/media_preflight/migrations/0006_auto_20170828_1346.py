# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media_preflight', '0005_preflightcheck_preflight_error'),
    ]

    operations = [
        migrations.RenameField(
            model_name='preflightcheck',
            old_name='preflight_error',
            new_name='preflight_ok',
        ),
    ]
