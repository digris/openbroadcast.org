# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abcast', '0004_auto_20160606_1441'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='channel',
            name='description_html',
        ),
        migrations.RemoveField(
            model_name='station',
            name='description_html',
        ),
        migrations.AddField(
            model_name='channel',
            name='icecast2_admin_pass',
            field=models.CharField(max_length=128, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='channel',
            name='icecast2_admin_user',
            field=models.CharField(max_length=128, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='channel',
            name='icecast2_mountpoint',
            field=models.CharField(max_length=128, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='channel',
            name='icecast2_server',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
    ]
