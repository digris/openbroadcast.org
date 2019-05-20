# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '0037_relation_object_id_add_index'),
    ]

    operations = [
        migrations.AddField(
            model_name='label',
            name='ipi_code',
            field=models.CharField(max_length=32, null=True, verbose_name='IPI Code', blank=True),
        ),
        migrations.AddField(
            model_name='label',
            name='isni_code',
            field=models.CharField(max_length=32, null=True, verbose_name='ISNI Code', blank=True),
        ),
        migrations.AlterField(
            model_name='relation',
            name='service',
            field=models.CharField(default='generic', choices=[('', 'Not specified'), ('generic', 'Generic'), ('facebook', 'Facebook'), ('youtube', 'YouTube'), ('discogs', 'Discogs'), ('lastfm', 'Last.fm'), ('linkedin', 'Linked In'), ('soundcloud', 'Soundcloud'), ('twitter', 'Twitter'), ('discogs_master', 'Discogs | master-release'), ('wikipedia', 'Wikipedia'), ('musicbrainz', 'Musicbrainz'), ('bandcamp', 'Bandcamp'), ('itunes', 'iTunes'), ('wikidata', 'wikidata'), ('viaf', 'VIAF'), ('official', 'Official website')], max_length=50, blank=True, null=True, db_index=True),
        ),
    ]
