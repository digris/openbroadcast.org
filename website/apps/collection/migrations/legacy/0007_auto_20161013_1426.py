# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0006_collection_owner'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='collectionmember',
            unique_together=set([('collection', 'item')]),
        ),
    ]
