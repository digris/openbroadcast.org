# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('tagging', '0003_add_tag_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='taggeditem',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 1, 0, 0, 0, 0), auto_now_add=True, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='taggeditem',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 1, 0, 0, 0, 0), auto_now=True, db_index=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tag',
            name='type',
            field=models.CharField(default=b'genre', choices=[(b'genre', b'Genre'), (b'mood', b'Mood'), (b'descriptive', b'Descriptive'), (b'event', b'Event'), (b'instrument', b'Instrument'), (b'profession', b'Profession')], max_length=32, blank=True, null=True, db_index=True),
        ),
    ]
