# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abcast', '0003_auto_20160118_1630'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='broadcast',
            name='playlist',
        ),
        migrations.RemoveField(
            model_name='broadcast',
            name='user',
        ),
        migrations.RemoveField(
            model_name='streamserver',
            name='formats',
        ),
        migrations.RemoveField(
            model_name='channel',
            name='stream_server',
        ),
        migrations.DeleteModel(
            name='Broadcast',
        ),
        migrations.DeleteModel(
            name='StreamFormat',
        ),
        migrations.DeleteModel(
            name='StreamServer',
        ),
    ]
