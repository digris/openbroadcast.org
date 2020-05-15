# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '0003_auto_20200222_1306'),
    ]

    operations = [
        migrations.AddField(
            model_name='label',
            name='founding_artist',
            field=models.ForeignKey(related_name='labels_founded', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Founder', blank=True, to='alibrary.Artist', null=True),
        ),
        migrations.AlterField(
            model_name='mediaartists',
            name='join_phrase',
            field=models.CharField(default=None, choices=[(b'&', '&'), (b',', ','), (b'and', 'and'), (b'feat', 'feat.'), (b'feat.', 'feat.'), (b'presents', 'presents'), (b'meets', 'meets'), (b'with', 'with'), (b'vs', 'vs.'), (b'x', 'X'), (b'-', '-')], max_length=12, blank=True, null=True, verbose_name='join phrase'),
        ),
        migrations.AlterField(
            model_name='releasealbumartists',
            name='join_phrase',
            field=models.CharField(default=None, choices=[(b'&', '&'), (b',', ','), (b'and', 'and'), (b'feat', 'feat.'), (b'feat.', 'feat.'), (b'presents', 'presents'), (b'meets', 'meets'), (b'with', 'with'), (b'vs', 'vs.'), (b'x', 'X'), (b'-', '-')], max_length=12, blank=True, null=True, verbose_name='join phrase'),
        ),
    ]
