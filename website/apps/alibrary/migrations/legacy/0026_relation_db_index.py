# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '0025_auto_20160601_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relation',
            name='service',
            field=models.CharField(default='generic', choices=[('', 'Not specified'), ('generic', 'Generic'), ('facebook', 'Facebook'), ('youtube', 'YouTube'), ('discogs', 'Discogs'), ('lastfm', 'Last.fm'), ('linkedin', 'Linked In'), ('soundcloud', 'Soundcloud'), ('twitter', 'Twitter'), ('discogs_master', 'Discogs | master-release'), ('wikipedia', 'Wikipedia'), ('musicbrainz', 'Musicbrainz'), ('bandcamp', 'Bandcamp'), ('itunes', 'iTunes'), ('official', 'Official website')], max_length=50, blank=True, null=True, db_index=True),
        ),
    ]
