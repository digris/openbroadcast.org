# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_extensions.db.fields.json


class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '0040_clean_fields_edit_mode'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='licensetranslation',
            options={'default_permissions': (), 'managed': True},
        ),
        migrations.AlterField(
            model_name='licensetranslation',
            name='master',
            field=models.ForeignKey(related_name='translations', editable=False, to='alibrary.License'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='playlist',
            name='broadcast_status_messages',
            field=django_extensions.db.fields.json.JSONField(default=None, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='created',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='updated',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='playlistitemplaylist',
            name='created',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='playlistitemplaylist',
            name='updated',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='relation',
            name='service',
            field=models.CharField(default='generic', choices=[('', 'Not specified'), ('generic', 'Generic'), ('facebook', 'Facebook'), ('youtube', 'YouTube'), ('discogs', 'Discogs'), ('lastfm', 'Last.fm'), ('linkedin', 'Linked In'), ('soundcloud', 'Soundcloud'), ('twitter', 'Twitter'), ('discogs_master', 'Discogs | master-release'), ('wikipedia', 'Wikipedia'), ('musicbrainz', 'Musicbrainz'), ('bandcamp', 'Bandcamp'), ('itunes', 'iTunes'), ('imdb', 'IMDb'), ('wikidata', 'wikidata'), ('viaf', 'VIAF'), ('official', 'Official website'), ('vimeo', 'Vimeo'), ('instagram', 'Instagram')], max_length=50, blank=True, null=True, db_index=True),
        ),
    ]
