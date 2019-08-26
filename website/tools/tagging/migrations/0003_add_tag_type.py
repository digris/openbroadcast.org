# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tagging', '0002_auto_20190123_1509'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='type',
            field=models.CharField(default=b'genre', choices=[(b'genre', b'Genre'), (b'sub-genre', b'Sub-Genre'), (b'mood', b'Mood')], max_length=32, blank=True, null=True, db_index=True),
        ),
    ]
