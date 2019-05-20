# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0007_auto_20161013_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collectionmember',
            name='collection',
            field=models.ForeignKey(related_name='members', to='collection.Collection'),
        ),
    ]
