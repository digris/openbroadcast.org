# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '0038_auto_20171208_1951'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='playout_mode_random',
            field=models.BooleanField(default=False, help_text='If enabled the order of the tracks will be randomized for playout', verbose_name='Shuffle Playlist'),
        ),
        migrations.AlterField(
            model_name='mediaartists',
            name='join_phrase',
            field=models.CharField(default=None, choices=[(b'&', '&'), (b',', ','), (b'and', 'and'), (b'feat', 'feat.'), (b'feat.', 'feat.'), (b'presents', 'presents'), (b'meets', 'meets'), (b'with', 'with'), (b'vs', 'vs.'), (b'-', '-')], max_length=12, blank=True, null=True, verbose_name='join phrase'),
        ),
        migrations.AlterField(
            model_name='relation',
            name='service',
            field=models.CharField(default='generic', choices=[('', 'Not specified'), ('generic', 'Generic'), ('facebook', 'Facebook'), ('youtube', 'YouTube'), ('discogs', 'Discogs'), ('lastfm', 'Last.fm'), ('linkedin', 'Linked In'), ('soundcloud', 'Soundcloud'), ('twitter', 'Twitter'), ('discogs_master', 'Discogs | master-release'), ('wikipedia', 'Wikipedia'), ('musicbrainz', 'Musicbrainz'), ('bandcamp', 'Bandcamp'), ('itunes', 'iTunes'), ('imdb', 'IMDb'), ('wikidata', 'wikidata'), ('viaf', 'VIAF'), ('official', 'Official website')], max_length=50, blank=True, null=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='releasealbumartists',
            name='join_phrase',
            field=models.CharField(default=None, choices=[(b'&', '&'), (b',', ','), (b'and', 'and'), (b'feat', 'feat.'), (b'feat.', 'feat.'), (b'presents', 'presents'), (b'meets', 'meets'), (b'with', 'with'), (b'vs', 'vs.'), (b'-', '-')], max_length=12, blank=True, null=True, verbose_name='join phrase'),
        ),
    ]
