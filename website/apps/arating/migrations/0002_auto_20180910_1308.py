# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("arating", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="vote",
            name="created",
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name="vote",
            name="updated",
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.AlterField(
            model_name="vote",
            name="vote",
            field=models.SmallIntegerField(
                db_index=True, choices=[(1, b"+1"), (-1, b"-1")]
            ),
        ),
    ]
