# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '0023_auto_20160223_1011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediaartists',
            name='join_phrase',
            field=models.CharField(default=None, choices=[(b'&', '&'), (b',', ','), (b'and', 'and'), (b'feat', 'feat.'), (b'presents', 'presents'), (b'meets', 'meets'), (b'with', 'with'), (b'vs', 'vs.'), (b'-', '-')], max_length=12, blank=True, null=True, verbose_name='join phrase'),
        ),
        migrations.AlterField(
            model_name='releasealbumartists',
            name='join_phrase',
            field=models.CharField(default=None, choices=[(b'&', '&'), (b',', ','), (b'and', 'and'), (b'feat', 'feat.'), (b'presents', 'presents'), (b'meets', 'meets'), (b'with', 'with'), (b'vs', 'vs.'), (b'-', '-')], max_length=12, blank=True, null=True, verbose_name='join phrase'),
        ),
    ]
