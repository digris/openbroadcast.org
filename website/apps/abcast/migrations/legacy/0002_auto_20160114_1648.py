# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abcast', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='tunein_partner_id',
            field=models.CharField(max_length=16, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='channel',
            name='tunein_partner_key',
            field=models.CharField(max_length=16, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='channel',
            name='tunein_station_id',
            field=models.CharField(max_length=16, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='streamserver',
            name='host',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
    ]
